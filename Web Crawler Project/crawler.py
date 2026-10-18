"""
Multi-Threaded Web Crawler with SQLite Storage & File Downloader
-----------------------------------------------------------------------------
This module implements an efficient, polite, and resumable web crawler in Python.
It crawls web pages starting from seed URLs, extracts textual content and hyperlinks,
and downloads specified file formats (such as .pdf, image formats, .swf, docs, archives,
media, or any custom extension).

Metadata for crawled pages and downloaded files are persistently stored in an SQLite
database (crawler.db), while binary files are saved into an organized directory structure.
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import time
import concurrent.futures
import threading
import logging
import sys
import os
import re
import argparse
import mimetypes
import hashlib

# Initialize mimetypes database
mimetypes.init()

# Supplemental MIME type mapping for formats that might be absent or non-standard in default OS registries
EXTRA_MIME_TYPES = {
    'application/x-shockwave-flash': '.swf',
    'application/futuresplash': '.spl',
    'application/pdf': '.pdf',
    'image/webp': '.webp',
    'image/avif': '.avif',
    'image/svg+xml': '.svg',
    'image/png': '.png',
    'image/jpeg': '.jpg',
    'image/gif': '.gif',
    'audio/mpeg': '.mp3',
    'audio/wav': '.wav',
    'video/mp4': '.mp4',
    'application/zip': '.zip',
    'application/x-zip-compressed': '.zip',
}

# Pre-defined convenience presets for common file categories
FILE_TYPE_PRESETS = {
    'images': {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.ico', '.tiff', '.avif'},
    'documents': {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf', '.csv'},
    'docs': {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf', '.csv'},
    'flash': {'.swf', '.flv', '.spl'},
    'media': {'.mp3', '.mp4', '.wav', '.avi', '.mov', '.mkv', '.ogg', '.webm', '.flac'},
    'archives': {'.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.xz'},
}

# Web page extensions that should not be classified as standalone downloadable binary files when using wildcard '*'
HTML_PAGE_EXTENSIONS = {'.html', '.htm', '.php', '.asp', '.aspx', '.jsp', '.cgi', '.shtml', ''}

# Default crawler configuration values
DEFAULT_DB_PATH = "crawler.db"
DEFAULT_MAX_WORKERS = 5
DEFAULT_MAX_PAGES = 100
DEFAULT_DELAY = 0.5
DEFAULT_DOWNLOAD_DIR = "downloads"
DEFAULT_SEED_URLS = ["https://news.ycombinator.com/"]
DEFAULT_FILE_TYPES = "all"

# ---------------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (Thread %(threadName)s) %(message)s'
)


def sanitize_filename(filename, max_length=150):
    """
    Sanitizes a string to make it safe for use as a filename across Windows, macOS, and Linux.
    Replaces illegal characters, handles Windows reserved names (CON, PRN, etc.), and truncates safely.
    """
    invalid_chars = {'<', '>', ':', '"', '/', '\\', '|', '?', '*'} | {chr(i) for i in range(32)}
    cleaned = ''.join('_' if c in invalid_chars else c for c in filename)
    cleaned = cleaned.strip('. ')
    if not cleaned:
        cleaned = "unnamed_file"

    base, ext = os.path.splitext(cleaned)
    windows_reserved = {
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }
    if base.upper() in windows_reserved:
        cleaned = f"_{cleaned}"

    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length - len(ext)] + ext

    return cleaned


def parse_file_types(types_input):
    """
    Parses a string, list, or set of file extensions / presets into a set of normalized extensions.
    Supports individual extensions (e.g., '.pdf', 'swf', 'png'), convenience presets ('images', 'docs'),
    and the wildcard 'all' or '*'.
    """
    if not types_input:
        return set()

    if isinstance(types_input, str):
        raw_items = [item.strip() for item in types_input.replace(',', ' ').split()]
    else:
        raw_items = []
        for entry in types_input:
            if isinstance(entry, str):
                raw_items.extend([item.strip() for item in entry.replace(',', ' ').split()])
            else:
                raw_items.append(str(entry).strip())

    normalized = set()
    for item in raw_items:
        clean = item.lower().strip()
        if not clean:
            continue
        if clean in ('none', 'text', 'off', 'disable', 'disabled'):
            continue
        if clean in ('all', '*'):
            return {'*'}
        if clean in FILE_TYPE_PRESETS:
            normalized.update(FILE_TYPE_PRESETS[clean])
        else:
            if not clean.startswith('.'):
                clean = '.' + clean
            normalized.add(clean)

    return normalized


def extract_file_extension(url_or_path, allowed_custom_types=None):
    """
    Extracts a normalized, valid file extension (e.g. '.pdf', '.png') from a URL or file path.
    A genuine file extension:
      - Appears after the final period in the last path segment (basename).
      - Starts with a dot followed by 1 to 8 alphanumeric characters.
      - Contains at least one letter (to avoid misidentifying version numbers like 1.0 or specs like 6.3 as extensions).
      - Does not contain hyphens, underscores, slashes, or query symbols.
    Returns the lowercased extension (e.g. '.pdf') or '' if no valid extension is found.
    """
    if not url_or_path:
        return ''

    parsed = urlparse(str(url_or_path))
    path = unquote(parsed.path)
    filename = os.path.basename(path.rstrip('/'))
    if not filename:
        return ''

    # If matching any custom allowed types explicitly configured (e.g. multi-dot '.tar.gz')
    if allowed_custom_types:
        for custom_ext in allowed_custom_types:
            if custom_ext != '*' and filename.lower().endswith(custom_ext):
                return custom_ext

    base, ext = os.path.splitext(filename)
    if not ext:
        return ''

    ext = ext.lower()
    # Genuine file extension pattern: 1-8 alphanumeric chars containing at least one letter
    if len(ext) <= 9 and re.match(r'^\.[a-zA-Z0-9]*[a-zA-Z][a-zA-Z0-9]*$', ext):
        return ext

    return ''


class WebCrawler:
    """
    A multi-threaded web crawler with support for:
      - Clean textual page content extraction
      - Persistent SQLite storage for both pages and files
      - Politeness rate-limiting and session resumption
      - Multi-format file downloading (.pdf, images, .swf, media, archives, etc.)
    """

    def __init__(self, args=None, db_path=None, max_workers=None, max_pages=None, delay=None,
                 allowed_file_types=None, download_dir=None, max_files=None):
        """
        Initialize the crawler with configurable limits, storage options, and file filters.
        All arguments are optional and will safely fall back to sensible defaults.

        Supported initialization patterns:
          1. Default initialization (zero arguments):
             crawler = WebCrawler()
          2. Pass an argparse.Namespace object directly:
             crawler = WebCrawler(args)
          3. Pass a dictionary of settings:
             crawler = WebCrawler({'max_workers': 8, 'allowed_file_types': ['.pdf']})
          4. Pass keyword arguments (any subset or all):
             crawler = WebCrawler(max_workers=5, download_dir="my_downloads")

        Parameters:
        -----------
        args : argparse.Namespace | dict | None
            Parsed CLI arguments or configuration dictionary.
        db_path : str | None
            File system path to the SQLite database file (default: 'crawler.db').
        max_workers : int | None
            Maximum concurrent worker threads running in the pool (default: 5).
        max_pages : int | None
            Safety cap on total HTML pages to crawl in a session (default: 100).
        delay : float | None
            Politeness delay in seconds applied before each network fetch (default: 0.5).
        allowed_file_types : list | set | str | None
            File extensions or presets to download (e.g. ['.pdf', '.swf', 'images']).
            Defaults to DEFAULT_FILE_TYPES ('all'). Use 'none' or [] for text-only mode.
        download_dir : str | None
            Directory on disk where downloaded files will be stored (default: 'downloads').
        max_files : int | None
            Maximum number of files to download per session (default: None / uncapped).
        """
        # If args object (from argparse or custom class) or dict is passed, extract attributes
        if args is not None:
            if hasattr(args, '__dict__') or hasattr(args, 'db_path'):
                db_path = db_path if db_path is not None else getattr(args, 'db_path', None)
                max_workers = max_workers if max_workers is not None else getattr(args, 'max_workers', None)
                max_pages = max_pages if max_pages is not None else getattr(args, 'max_pages', None)
                max_files = max_files if max_files is not None else getattr(args, 'max_files', None)
                delay = delay if delay is not None else getattr(args, 'delay', None)
                allowed_file_types = allowed_file_types if allowed_file_types is not None else getattr(args, 'file_types', None)
                download_dir = download_dir if download_dir is not None else getattr(args, 'download_dir', None)
            elif isinstance(args, dict):
                db_path = db_path if db_path is not None else args.get('db_path')
                max_workers = max_workers if max_workers is not None else args.get('max_workers')
                max_pages = max_pages if max_pages is not None else args.get('max_pages')
                max_files = max_files if max_files is not None else args.get('max_files')
                delay = delay if delay is not None else args.get('delay')
                allowed_file_types = allowed_file_types if allowed_file_types is not None else args.get('file_types', args.get('allowed_file_types'))
                download_dir = download_dir if download_dir is not None else args.get('download_dir')

        # Fall back to defaults if any parameter was omitted or passed as None
        self.db_path = db_path if db_path is not None else DEFAULT_DB_PATH
        self.max_workers = int(max_workers) if max_workers is not None else DEFAULT_MAX_WORKERS
        self.max_pages = int(max_pages) if max_pages is not None else DEFAULT_MAX_PAGES
        self.max_files = int(max_files) if max_files is not None else None
        self.delay = float(delay) if delay is not None else DEFAULT_DELAY
        self.download_dir = download_dir if download_dir is not None else DEFAULT_DOWNLOAD_DIR
        allowed_file_types = allowed_file_types if allowed_file_types is not None else DEFAULT_FILE_TYPES
        self.allowed_file_types = parse_file_types(allowed_file_types)

        # In-memory sets to deduplicate URLs in O(1) time
        self.visited = set()         # Crawled HTML pages
        self.visited_files = set()   # Downloaded files

        # Thread lock to guarantee atomic, thread-safe updates to shared state
        self.lock = threading.Lock()

        # Step 1: Ensure database schema exists (creates pages and files tables)
        self._init_db()

        # Step 2: Load already-crawled URLs from existing SQLite database for session resumption
        self._load_visited_from_db()

    def _init_db(self):
        """
        Creates the SQLite database and necessary tables ('pages' and 'files') if they do not exist.
        Using UNIQUE(url) constraints prevents duplicate storage at the DB layer.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            # Table for textual HTML pages
            c.execute('''
                CREATE TABLE IF NOT EXISTS pages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,                           -- Unique normalized page URL
                    title TEXT,                                -- Extracted HTML <title>
                    content TEXT,                              -- Clean text stripped of HTML/scripts
                    status_code INTEGER,                       -- HTTP status code (e.g. 200, 404, 500)
                    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Automatic ISO timestamp
                )
            ''')
            # Table for downloaded binary files (.pdf, images, .swf, etc.)
            c.execute('''
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,                           -- Unique file URL
                    file_path TEXT,                            -- Local file path on disk
                    file_name TEXT,                            -- Clean filename
                    file_type TEXT,                            -- File extension (e.g. .pdf, .swf, .png)
                    file_size INTEGER,                         -- Size in bytes
                    mime_type TEXT,                            -- Content-Type reported by server
                    source_page TEXT,                          -- Webpage URL where file was discovered
                    status_code INTEGER,                       -- HTTP status code
                    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Performance indexes
            c.execute('CREATE INDEX IF NOT EXISTS idx_pages_url ON pages(url)')
            c.execute('CREATE INDEX IF NOT EXISTS idx_files_url ON files(url)')
            c.execute('CREATE INDEX IF NOT EXISTS idx_files_file_type ON files(file_type)')
            conn.commit()

    def _load_visited_from_db(self):
        """
        Populates self.visited and self.visited_files with URLs already in the database.
        Enables seamless 'Session Resumption' across crawler restarts.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT url FROM pages')
            for row in c.fetchall():
                self.visited.add(row[0])

            c.execute('SELECT url FROM files')
            for row in c.fetchall():
                self.visited_files.add(row[0])

        logging.info(
            f"Session Resumption: Loaded {len(self.visited)} crawled pages "
            f"and {len(self.visited_files)} downloaded files from database."
        )

    def _save_to_db(self, url, title, content, status_code):
        """
        Persists an individual crawled page's textual data into SQLite.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT OR REPLACE INTO pages (url, title, content, status_code)
                    VALUES (?, ?, ?, ?)
                ''', (url, title, content, status_code))
                conn.commit()
        except Exception as e:
            logging.error(f"Failed to save page {url} to DB: {e}")

    def _save_file_to_db(self, url, file_path, file_name, file_type, file_size, mime_type, source_page, status_code):
        """
        Persists downloaded file metadata into the 'files' table in SQLite.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT OR REPLACE INTO files (url, file_path, file_name, file_type, file_size, mime_type, source_page, status_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (url, file_path, file_name, file_type, file_size, mime_type, source_page, status_code))
                conn.commit()
        except Exception as e:
            logging.error(f"Failed to save file metadata for {url} to DB: {e}")

    def _normalize_url(self, base_url, href):
        """
        Resolves relative URLs against base_url, removes fragments, and ensures HTTP/HTTPS scheme.
        """
        if not href or href.strip().startswith(('javascript:', 'mailto:', 'tel:', 'data:#')):
            return None

        full_url = urljoin(base_url, href.strip())
        parsed = urlparse(full_url)
        if parsed.scheme not in ('http', 'https'):
            return None

        # Discard fragments (#section)
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if parsed.query:
            clean_url += f"?{parsed.query}"

        return clean_url

    def is_file_allowed(self, url, content_type=None):
        """
        Determines whether a given URL or Content-Type matches the allowed file extensions/presets.
        """
        if not self.allowed_file_types:
            return False

        ext = extract_file_extension(url, self.allowed_file_types)

        # Wildcard match: accept all non-HTML web page resources
        if '*' in self.allowed_file_types:
            if ext and ext not in HTML_PAGE_EXTENSIONS:
                return True
            if content_type:
                mime = content_type.split(';')[0].strip().lower()
                if mime not in ('text/html', 'application/xhtml+xml', 'text/plain'):
                    return True
            return False

        # Specific extension matching
        if ext and ext in self.allowed_file_types:
            return True

        # Check for query parameters hinting at filename (e.g. ?file=document.pdf)
        parsed = urlparse(url)
        if not ext and parsed.query:
            match = re.search(r'[\w\-.]+\.([a-zA-Z0-9]{2,5})', parsed.query)
            if match:
                query_ext = '.' + match.group(1).lower()
                if query_ext in self.allowed_file_types or '*' in self.allowed_file_types:
                    if query_ext not in HTML_PAGE_EXTENSIONS:
                        return True

        # Check MIME type against allowed extensions
        if content_type:
            mime = content_type.split(';')[0].strip().lower()
            guessed_ext = EXTRA_MIME_TYPES.get(mime) or mimetypes.guess_extension(mime)
            if guessed_ext:
                guessed_clean = guessed_ext.lower()
                if '*' in self.allowed_file_types or guessed_clean in self.allowed_file_types:
                    if guessed_clean not in HTML_PAGE_EXTENSIONS:
                        return True

        return False

    def is_file_url(self, url):
        """
        Checks whether a URL's path directly ends with an allowed file extension.
        """
        if not self.allowed_file_types:
            return False
        ext = extract_file_extension(url, self.allowed_file_types)
        if not ext:
            return False
        if '*' in self.allowed_file_types:
            return ext not in HTML_PAGE_EXTENSIONS
        return ext in self.allowed_file_types

    def is_page_url(self, url):
        """
        Checks whether a URL represents an HTML/navigable web page rather than a binary file.
        """
        ext = extract_file_extension(url, self.allowed_file_types)
        return ext in HTML_PAGE_EXTENSIONS

    def download_file(self, url, source_page=None):
        """
        Streams and saves a remote file to disk, updating the SQLite 'files' table.
        Safe against collisions, memory bloat, and path traversal vulnerabilities.
        """
        try:
            time.sleep(self.delay)
            headers = {'User-Agent': 'ProfessionalCrawler/1.0 (File & Web Crawler)'}
            response = requests.get(url, stream=True, timeout=25, headers=headers)
            status_code = response.status_code

            if status_code != 200:
                self._save_file_to_db(url, None, "", "", 0, "", source_page, status_code)
                logging.warning(f"File download failed for {url} (Status: {status_code})")
                return None

            content_type = response.headers.get('Content-Type', '').split(';')[0].strip().lower()

            # Guard against downloading HTML pages when binary files are expected
            is_html_type = content_type in ('text/html', 'application/xhtml+xml')
            explicit_html = self.allowed_file_types and any(h in self.allowed_file_types for h in ('.html', '.htm'))
            if is_html_type and not explicit_html:
                logging.info(f"Skipping binary download for {url}: server returned '{content_type}' (web page, not a file)")
                return None

            # Determine file extension and base name
            # Check Content-Disposition header first (e.g. filename="document.pdf")
            content_disposition = response.headers.get('Content-Disposition', '')
            cd_filename = ""
            if content_disposition:
                cd_match = re.search(r'filename\*?=(?:UTF-8\'\')?["\']?([^";\r\n]+)["\']?', content_disposition, re.IGNORECASE)
                if cd_match:
                    cd_filename = os.path.basename(unquote(cd_match.group(1).strip()))

            parsed = urlparse(url)
            path = unquote(parsed.path)
            raw_filename = cd_filename or os.path.basename(path.rstrip('/'))

            ext = extract_file_extension(raw_filename, self.allowed_file_types)
            if ext:
                name_stem = raw_filename[:-len(ext)]
            else:
                name_stem = raw_filename
                if content_type:
                    ext = EXTRA_MIME_TYPES.get(content_type) or mimetypes.guess_extension(content_type) or ''

            if not name_stem or name_stem == ext:
                url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:8]
                name_stem = f"file_{url_hash}"

            safe_name = sanitize_filename(f"{name_stem}{ext}")

            # Organize downloads into per-domain subfolders
            domain = sanitize_filename(parsed.netloc or 'misc_downloads')
            target_dir = os.path.join(self.download_dir, domain)
            os.makedirs(target_dir, exist_ok=True)

            target_path = os.path.join(target_dir, safe_name)

            # Prevent file overwriting when different URLs have the exact same filename
            final_ext = extract_file_extension(safe_name, self.allowed_file_types) or os.path.splitext(safe_name)[1]
            stem = safe_name[:-len(final_ext)] if final_ext else safe_name
            counter = 1
            while os.path.exists(target_path):
                target_path = os.path.join(target_dir, f"{stem}_{counter}{final_ext}")
                counter += 1

            # Stream download in 64KB chunks to protect RAM
            total_bytes = 0
            with open(target_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=65536):
                    if chunk:
                        f.write(chunk)
                        total_bytes += len(chunk)

            final_file_name = os.path.basename(target_path)
            detected_type = extract_file_extension(final_file_name, self.allowed_file_types) or ext

            # Persist to SQLite
            self._save_file_to_db(
                url=url,
                file_path=os.path.abspath(target_path),
                file_name=final_file_name,
                file_type=detected_type,
                file_size=total_bytes,
                mime_type=content_type,
                source_page=source_page or "",
                status_code=status_code
            )

            logging.info(f"Downloaded: {url} -> {target_path} ({total_bytes} bytes)")
            return {
                'url': url,
                'file_path': os.path.abspath(target_path),
                'file_name': final_file_name,
                'file_type': detected_type,
                'file_size': total_bytes,
                'status_code': status_code
            }

        except requests.RequestException as e:
            logging.error(f"Network error downloading file {url}: {e}")
            self._save_file_to_db(url, None, "", "", 0, "", source_page, 0)
            return None
        except Exception as e:
            logging.error(f"Unexpected error downloading file {url}: {e}")
            return None

    def crawl_page(self, url):
        """
        Worker function executed by threads in the ThreadPoolExecutor.
        Performs the following steps:
          1. Respects politeness delay.
          2. Sends HTTP GET request with User-Agent and timeout.
          3. Inspects Content-Type: if it is a binary file matching allowed types, downloads it.
          4. If HTML: strips script/style tags, extracts title and clean body text into SQLite.
          5. Extracts outgoing page hyperlinks for BFS navigation.
          6. Extracts embedded media/file references (<img src>, <embed src>, <object data>,
             <source src>, <video>, <audio>, <iframe>, <link>, etc.) for file downloading.

        Returns:
        --------
        tuple: (url, list_of_discovered_pages, list_of_discovered_files)
        """
        try:
            # 1. Politeness Delay
            time.sleep(self.delay)

            # 2. HTTP Request with stream=True so headers can be inspected before downloading large bodies
            headers = {'User-Agent': 'ProfessionalCrawler/1.0 (Educational/Analytical Crawler)'}
            response = requests.get(url, timeout=12, headers=headers)
            status_code = response.status_code

            if status_code != 200:
                self._save_to_db(url, "", "", status_code)
                return url, [], []

            # 3. Content-Type Check: Detect dynamic binary file downloads
            content_type = response.headers.get('Content-Type', '').split(';')[0].strip().lower()
            if content_type and content_type not in ('text/html', 'application/xhtml+xml', 'text/plain'):
                if self.is_file_allowed(url, content_type):
                    # URL served a binary file directly! Stream to disk instead of HTML parser
                    self.download_file(url, source_page=url)
                    return url, [], []
                else:
                    # Non-HTML content not requested by user
                    return url, [], []

            # 4. HTML Parsing using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract document title
            title = soup.title.string.strip() if soup.title and soup.title.string else ""

            # Extract Clean Body Text
            for tag in soup(["script", "style", "noscript", "svg", "header", "footer"]):
                tag.extract()

            content = soup.get_text(separator=' ', strip=True)

            # 5. Persist Clean Text to Database
            self._save_to_db(url, title, content, status_code)

            # 6. Hyperlink & File Discovery
            discovered_pages = []
            discovered_files = []

            # A) Standard hyperlinks: <a href="...">
            for a_tag in soup.find_all('a', href=True):
                full_url = self._normalize_url(url, a_tag['href'])
                if not full_url:
                    continue

                if self.is_file_allowed(full_url):
                    discovered_files.append(full_url)
                elif self.is_page_url(full_url):
                    discovered_pages.append(full_url)
                # Else: Non-matching binary file (e.g. .png when user requested only .pdf) -> ignore

            # B) Images: <img src="..." data-src="..."> and <picture><source srcset="...">
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src') or img.get('data-original')
                if src:
                    full_url = self._normalize_url(url, src)
                    if full_url and self.is_file_allowed(full_url):
                        discovered_files.append(full_url)

            # C) Flash & Plugins: <embed src="..."> and <object data="..."> (Common for .swf, media)
            for embed in soup.find_all('embed', src=True):
                full_url = self._normalize_url(url, embed['src'])
                if full_url and self.is_file_allowed(full_url):
                    discovered_files.append(full_url)

            for obj in soup.find_all('object'):
                data = obj.get('data')
                if data:
                    full_url = self._normalize_url(url, data)
                    if full_url and self.is_file_allowed(full_url):
                        discovered_files.append(full_url)
                # Check <param name="movie" value="..."> used heavily in Flash .swf embeds
                for param in obj.find_all('param'):
                    param_name = param.get('name', '').lower()
                    if param_name in ('movie', 'src', 'data', 'filename') and param.get('value'):
                        full_url = self._normalize_url(url, param['value'])
                        if full_url and self.is_file_allowed(full_url):
                            discovered_files.append(full_url)

            # D) Media & Streaming: <source src="...">, <video src="...">, <audio src="...">
            for source in soup.find_all('source', src=True):
                full_url = self._normalize_url(url, source['src'])
                if full_url and self.is_file_allowed(full_url):
                    discovered_files.append(full_url)

            for media_tag in soup.find_all(['video', 'audio', 'iframe'], src=True):
                full_url = self._normalize_url(url, media_tag['src'])
                if full_url and self.is_file_allowed(full_url):
                    discovered_files.append(full_url)

            # Deduplicate discovered items while preserving order
            discovered_pages = list(dict.fromkeys(discovered_pages))
            discovered_files = list(dict.fromkeys(discovered_files))

            logging.info(
                f"Crawled: {url} (Status: {status_code}) -> "
                f"Discovered {len(discovered_pages)} links, {len(discovered_files)} matching files"
            )
            return url, discovered_pages, discovered_files

        except requests.RequestException as e:
            logging.error(f"Network error on {url}: {e}")
            self._save_to_db(url, "", str(e), 0)
            return url, [], []
        except Exception as e:
            logging.error(f"Unexpected error on {url}: {e}")
            return url, [], []

    def start_crawling(self, seed_urls=None):
        """
        Main crawling coordinator.
        Manages the concurrent ThreadPoolExecutor for both HTML pages and file downloads.
        Dynamically queues newly discovered pages and files until limits are reached.

        If seed_urls is omitted or None, falls back to DEFAULT_SEED_URLS.
        """
        if not seed_urls:
            seed_urls = DEFAULT_SEED_URLS
        elif isinstance(seed_urls, str):
            seed_urls = [seed_urls]

        crawled_pages_count = 0
        downloaded_files_count = 0
        active_page_tasks = 0
        active_file_tasks = 0

        # Futures mapping: {Future: (task_type, target_url, source_url)}
        # task_type is either 'page' or 'file'
        futures = {}

        logging.info("Starting crawl session...")
        if self.allowed_file_types:
            types_repr = ', '.join(sorted(self.allowed_file_types))
            logging.info(f"Target file formats enabled: [{types_repr}] -> saving to '{self.download_dir}/'")
        else:
            logging.info("File downloading is disabled (text-only crawl mode).")

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Dispatch initial seed URLs
                for seed in seed_urls:
                    if self.is_file_url(seed) or self.is_file_allowed(seed):
                        if seed not in self.visited_files:
                            self.visited_files.add(seed)
                            fut = executor.submit(self.download_file, seed, None)
                            futures[fut] = ('file', seed, None)
                            active_file_tasks += 1
                    else:
                        if seed not in self.visited:
                            self.visited.add(seed)
                            fut = executor.submit(self.crawl_page, seed)
                            futures[fut] = ('page', seed, None)
                            active_page_tasks += 1

                # Dynamic execution loop
                while futures:
                    done, _ = concurrent.futures.wait(
                        futures,
                        return_when=concurrent.futures.FIRST_COMPLETED
                    )

                    for future in done:
                        task_type, item_url, source_url = futures.pop(future)

                        try:
                            if task_type == 'page':
                                active_page_tasks -= 1
                                crawled_pages_count += 1
                                _, new_pages, new_files = future.result()

                                with self.lock:
                                    # Schedule newly discovered HTML pages (if capacity allows)
                                    for page_link in new_pages:
                                        if (page_link not in self.visited and
                                                (crawled_pages_count + active_page_tasks) < self.max_pages):
                                            self.visited.add(page_link)
                                            fut = executor.submit(self.crawl_page, page_link)
                                            futures[fut] = ('page', page_link, item_url)
                                            active_page_tasks += 1

                                    # Schedule newly discovered files (if file types enabled and under max_files)
                                    if self.allowed_file_types:
                                        for file_link in new_files:
                                            if file_link not in self.visited_files:
                                                can_download = (
                                                    self.max_files is None or
                                                    (downloaded_files_count + active_file_tasks) < self.max_files
                                                )
                                                if can_download:
                                                    self.visited_files.add(file_link)
                                                    fut = executor.submit(self.download_file, file_link, item_url)
                                                    futures[fut] = ('file', file_link, item_url)
                                                    active_file_tasks += 1

                            elif task_type == 'file':
                                active_file_tasks -= 1
                                file_result = future.result()
                                if file_result and file_result.get('status_code') == 200:
                                    downloaded_files_count += 1

                        except Exception as e:
                            logging.error(f"Error processing task for {item_url}: {e}")

        except KeyboardInterrupt:
            logging.warning("\nCrawl manually interrupted by user (Ctrl+C). Saving completed state...")

        logging.info("=" * 60)
        logging.info(
            f"Crawl session completed!\n"
            f"  - Pages Crawled This Session : {crawled_pages_count}\n"
            f"  - Files Downloaded           : {downloaded_files_count}\n"
            f"  - Storage Directory          : {os.path.abspath(self.download_dir)}"
        )
        logging.info("=" * 60)


# ---------------------------------------------------------------------------
# CLI Argument Parser & Entrypoint
# ---------------------------------------------------------------------------
def build_cli_parser():
    """
    Builds the command-line interface argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Professional Multi-Threaded Web Crawler & File Downloader with SQLite Storage.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic text crawl with default seed:
  python crawler.py

  # Crawl specific seeds and download .pdf and .swf files:
  python crawler.py https://example.com --file-types .pdf .swf

  # Download all image formats and .pdf files to a custom folder:
  python crawler.py https://example.com -f images,pdf -o my_downloads

  # Download any file format encountered (wildcard):
  python crawler.py https://example.com -f all --max-pages 50 --max-files 100

Available file presets:
  images    : .jpg, .jpeg, .png, .gif, .webp, .svg, .bmp, .ico, .tiff, .avif
  docs      : .pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx, .txt, .rtf, .csv
  flash     : .swf, .flv, .spl
  media     : .mp3, .mp4, .wav, .avi, .mov, .mkv, .ogg, .webm, .flac
  archives  : .zip, .tar, .gz, .rar, .7z, .bz2, .xz
  all / *   : Any non-HTML file format
        """
    )
    parser.add_argument(
        'seeds',
        nargs='*',
        default=[],
        help="One or more seed URLs to start crawling from."
    )
    parser.add_argument(
        '--file-types', '-f',
        nargs='+',
        default=None,
        help="File extensions or presets to download (e.g. .pdf .swf .png, or presets: images, docs, flash, all)."
    )
    parser.add_argument(
        '--download-dir', '-o',
        default="downloads",
        help="Directory to store downloaded files (default: 'downloads')."
    )
    parser.add_argument(
        '--max-pages',
        type=int,
        default=100,
        help="Maximum HTML pages to crawl per session (default: 100)."
    )
    parser.add_argument(
        '--max-files',
        type=int,
        default=None,
        help="Maximum files to download per session (default: unlimited)."
    )
    parser.add_argument(
        '--max-workers', '-w',
        type=int,
        default=5,
        help="Number of concurrent worker threads (default: 5)."
    )
    parser.add_argument(
        '--delay', '-d',
        type=float,
        default=0.5,
        help="Politeness delay in seconds between network requests (default: 0.5)."
    )
    parser.add_argument(
        '--db-path',
        default="crawler.db",
        help="Path to SQLite database file (default: 'crawler.db')."
    )
    parser.add_argument(
        '--non-interactive',
        action='store_true',
        help="Disable interactive format selection prompt when running in a terminal."
    )
    return parser


def prompt_file_types_interactive():
    """
    Presents an interactive terminal menu allowing the user to select which file format(s)
    to crawl and download (e.g. all, only PDF, only Images, only SWF, only Docs, or custom).
    """
    print("\n" + "=" * 65)
    print("                 FILE FORMAT DOWNLOAD SELECTION")
    print("=" * 65)
    print(" Choose which files the crawler should discover & download:")
    print("   [1] ALL Formats    - Download EVERYTHING (PDFs, Images, SWF, Docs, Media) [DEFAULT]")
    print("   [2] Only PDFs      - Download ONLY .pdf documents")
    print("   [3] Only Images    - Download ONLY images (.jpg, .png, .gif, .webp, .svg)")
    print("   [4] Only Flash SWF - Download ONLY .swf Flash files")
    print("   [5] Only Documents - Download ONLY documents (.pdf, .docx, .xlsx, .txt)")
    print("   [6] Only Media     - Download ONLY media (.mp3, .mp4, .wav, etc.)")
    print("   [7] Custom Format  - Specify custom extension(s) (e.g. .pdf or .pdf,.swf)")
    print("   [0] Text Only      - Do not download files (crawls HTML text only)")
    print("=" * 65)

    try:
        choice = input("Select an option [0-7] (Press Enter for [1] ALL Formats): ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return DEFAULT_FILE_TYPES

    if choice == '' or choice == '1':
        print("-> Selected: ALL formats (everything will be downloaded)\n")
        return DEFAULT_FILE_TYPES
    elif choice == '2':
        print("-> Selected: Only PDFs (.pdf)\n")
        return ['.pdf']
    elif choice == '3':
        print("-> Selected: Only Images (jpg, png, gif, webp, svg, etc.)\n")
        return 'images'
    elif choice == '4':
        print("-> Selected: Only Flash (.swf)\n")
        return ['.swf']
    elif choice == '5':
        print("-> Selected: Only Documents (pdf, docx, xlsx, txt, etc.)\n")
        return 'docs'
    elif choice == '6':
        print("-> Selected: Only Media (mp3, mp4, wav, etc.)\n")
        return 'media'
    elif choice == '7':
        try:
            custom = input("Enter format(s) separated by commas (e.g. .pdf or .pdf,.swf): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return DEFAULT_FILE_TYPES
        if custom:
            print(f"-> Selected custom format(s): {custom}\n")
            return custom
        else:
            print(f"-> No custom extension entered. Defaulting to: ALL formats\n")
            return DEFAULT_FILE_TYPES
    elif choice == '0':
        print("-> Selected: Text Only (no files will be downloaded)\n")
        return 'none'
    else:
        print("-> Selected: ALL formats\n")
        return DEFAULT_FILE_TYPES


if __name__ == "__main__":
    parser = build_cli_parser()
    args = parser.parse_args()

    # Determine seed URLs: fallback to default seed if none provided
    seed_urls = args.seeds if args.seeds else DEFAULT_SEED_URLS

    # If --file-types was not explicitly passed on the command line and running in an interactive terminal,
    # prompt the user to choose which format to crawl:
    if args.file_types is None and sys.stdin.isatty() and not args.non_interactive:
        args.file_types = prompt_file_types_interactive()

    logging.info(f"Initializing crawler with seed URL(s): {seed_urls}")

    # Initialize WebCrawler with args (or with no arguments: WebCrawler())
    # All settings safely fall back to defaults if not specified
    crawler = WebCrawler(args)

    crawler.start_crawling(seed_urls=seed_urls)
