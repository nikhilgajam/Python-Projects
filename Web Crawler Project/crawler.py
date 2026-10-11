"""
Professional Multi-Threaded Web Crawler with SQLite Storage
-----------------------------------------------------------
This module implements an efficient, polite, and resumable web crawler in Python.
It crawls web pages starting from seed URLs, extracts textual content and hyperlinks,
and stores metadata persistently into an SQLite database (crawler.db).
"""

import sqlite3                      # For local, zero-config relational database storage
import requests                     # For executing HTTP GET requests to fetch web pages
from bs4 import BeautifulSoup       # For parsing HTML and extracting clean text and links
from urllib.parse import urljoin, urlparse  # For URL normalization and relative link resolution
import time                         # For politeness rate-limiting delays
import concurrent.futures           # For multi-threaded asynchronous concurrency
import threading                    # For thread synchronization locks
import logging                      # For structured informational and error logging
import sys                          # For command-line argument processing

# ---------------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------------
# Configures a standardized timestamped logging format across all threads
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (Thread %(threadName)s) %(message)s'
)


class WebCrawler:
    """
    A multi-threaded web crawler designed for robustness, politeness, and persistence.
    """

    def __init__(self, db_path="crawler.db", max_workers=5, max_pages=100, delay=0.5):
        """
        Initialize the crawler with configurable limits and database connection.

        Parameters:
        -----------
        db_path : str
            File system path to the SQLite database file.
        max_workers : int
            Maximum number of concurrent worker threads running in the pool.
        max_pages : int
            Safety cap on total pages to crawl in a single execution session.
        delay : float
            Politeness delay in seconds applied before each network fetch.
        """
        self.db_path = db_path
        self.max_workers = max_workers
        self.max_pages = max_pages
        self.delay = delay

        # In-memory set of visited URLs to avoid visiting the same URL twice in O(1) time
        self.visited = set()

        # Thread lock to guarantee atomic, thread-safe updates to shared state (self.visited, queues)
        self.lock = threading.Lock()
        
        # Step 1: Ensure database schema exists
        self._init_db()

        # Step 2: Load already-crawled URLs from existing SQLite database so we never re-crawl them
        self._load_visited_from_db()

    def _init_db(self):
        """
        Creates the SQLite database and the 'pages' table if they do not exist yet.
        Using a schema with UNIQUE(url) prevents duplicate storage at the DB layer.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS pages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,                           -- Unique normalized URL
                    title TEXT,                                -- Extracted HTML <title>
                    content TEXT,                              -- Clean text stripped of HTML/scripts
                    status_code INTEGER,                       -- HTTP status code (e.g. 200, 404, 500)
                    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Automatic ISO timestamp
                )
            ''')
            conn.commit()

    def _load_visited_from_db(self):
        """
        Populates self.visited with all URLs already stored in the database.
        This enables 'Session Resumption'—if you stop and restart the crawler,
        it seamlessly continues without re-crawling previous pages.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT url FROM pages')
            for row in c.fetchall():
                self.visited.add(row[0])
        logging.info(f"Loaded {len(self.visited)} previously crawled URLs from database.")

    def _save_to_db(self, url, title, content, status_code):
        """
        Persists an individual crawled page's data into SQLite.
        Uses INSERT OR REPLACE to update existing entries if re-visited.
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
            logging.error(f"Failed to save {url} to DB: {e}")

    def crawl_page(self, url):
        """
        Worker function executed by threads in the ThreadPoolExecutor.
        Performs the following steps:
          1. Respects politeness delay.
          2. Sends HTTP GET request with a descriptive User-Agent.
          3. Checks HTTP status code.
          4. Parses HTML, removing <script>, <style>, and <noscript> tags.
          5. Extracts pure readable text and page title.
          6. Saves page metadata to SQLite.
          7. Discovers, normalizes, and filters valid out-going HTTP/HTTPS links.

        Returns:
        --------
        tuple (url, list_of_discovered_urls)
        """
        try:
            # 1. Politeness Delay: Sleep briefly to avoid overwhelming target servers
            time.sleep(self.delay)

            # 2. HTTP Request: Use custom User-Agent and a 10s timeout to avoid hanging threads
            headers = {'User-Agent': 'ProfessionalCrawler/1.0 (Educational/Analytical Crawler)'}
            response = requests.get(url, timeout=10, headers=headers)
            status_code = response.status_code
            
            # If the HTTP status is not 200 OK (e.g., 404, 403, 500), log the code and stop traversal here
            if status_code != 200:
                self._save_to_db(url, "", "", status_code)
                return url, []

            # 3. HTML Parsing using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract document title, defaulting to empty string if tag is missing
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            
            # 4. Clean Content Extraction:
            # Remove non-visible or script elements to retain only meaningful text
            for script in soup(["script", "style", "noscript", "svg", "header", "footer"]):
                script.extract()
            
            # Extract text separated by single spaces
            content = soup.get_text(separator=' ', strip=True)
            
            # 5. Persist to Database:
            # Stores the clean textual content in SQLite
            self._save_to_db(url, title, content, status_code)
            
            # 6. Hyperlink Extraction & Normalization:
            links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                
                # Convert relative links (e.g., '/about') to absolute (e.g., 'https://example.com/about')
                full_url = urljoin(url, href)
                
                # Parse URL structure to validate and clean
                parsed = urlparse(full_url)
                
                # Filter: Only follow HTTP and HTTPS web schemes (ignore mailto:, tel:, javascript:)
                if parsed.scheme in ['http', 'https']:
                    # Normalize: Discard URL fragments (#section) because they point to the same page
                    clean_url = parsed.scheme + "://" + parsed.netloc + parsed.path
                    
                    # Preserve query parameters if present (e.g., ?id=123)
                    if parsed.query:
                        clean_url += "?" + parsed.query
                        
                    links.append(clean_url)
                    
            logging.info(f"Crawled: {url} (Status: {status_code}) -> Discovered {len(links)} links")
            return url, links
            
        except requests.RequestException as e:
            # Catch network timeouts, DNS resolution failures, and connection drops
            logging.error(f"Network error on {url}: {e}")
            self._save_to_db(url, "", str(e), 0)
            return url, []
        except Exception as e:
            # Catch unexpected parsing or runtime errors
            logging.error(f"Unexpected error on {url}: {e}")
            return url, []

    def start_crawling(self, seed_urls):
        """
        Main crawling coordinator.
        Manages the dynamic thread pool, scheduling new tasks as links are discovered
        until either no URLs remain or self.max_pages limit is reached.
        """
        # Filter initial seed URLs against previously crawled history
        urls_to_crawl = []
        for url in seed_urls:
            if url not in self.visited:
                urls_to_crawl.append(url)
                self.visited.add(url)
                
        crawled_count = 0
        
        # ThreadPoolExecutor manages worker threads concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Map of {Future: URL} tracking currently active running tasks
            futures = {executor.submit(self.crawl_page, url): url for url in urls_to_crawl}
            
            # Dynamic crawling loop: continues while tasks are running and limit is not exceeded
            while futures and crawled_count < self.max_pages:
                # Wait for the first worker thread to finish its page
                done, _ = concurrent.futures.wait(
                    futures,
                    return_when=concurrent.futures.FIRST_COMPLETED
                )
                
                for future in done:
                    orig_url = futures.pop(future)  # Remove completed task from tracking map
                    try:
                        _, new_links = future.result()
                        crawled_count += 1
                        
                        # Thread-safe dispatch of newly discovered URLs
                        with self.lock:
                            for link in new_links:
                                # Only schedule if unvisited and total capacity is below max_pages
                                if link not in self.visited and (len(futures) + crawled_count) < self.max_pages:
                                    self.visited.add(link)
                                    futures[executor.submit(self.crawl_page, link)] = link
                                    
                    except Exception as e:
                        logging.error(f"Task error on {orig_url}: {e}")

        logging.info(f"Crawling completed! Total pages crawled this session: {crawled_count}")


# ---------------------------------------------------------------------------
# CLI Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Default starting seed URL if none is supplied via CLI arguments
    seed = ["https://news.ycombinator.com/"]
    
    # Read custom seed URLs from command line arguments if provided
    if len(sys.argv) > 1:
        seed = sys.argv[1:]
        
    logging.info(f"Initializing crawler with seed URL(s): {seed}")
    
    # Instantiate and start the crawler
    # max_workers=5 : 5 concurrent threads
    # max_pages=100 : crawl up to 100 pages per session
    # delay=0.5     : 0.5s politeness delay per thread request
    crawler = WebCrawler(
        db_path="crawler.db",
        max_workers=5,
        max_pages=100,
        delay=0.5
    )
    
    crawler.start_crawling(seed_urls=seed)
