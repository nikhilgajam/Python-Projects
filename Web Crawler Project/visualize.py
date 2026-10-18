"""
Professional Crawler Data Analytics & Visual Dashboard
-------------------------------------------------------
Analyzes SQLite crawler database (crawler.db) and provides:
  1. Terminal summary (page statistics, keywords, downloaded file formats, and storage metrics).
  2. Interactive HTML report (report.html) with Chart.js charts and live search explorers
     for both crawled web pages and downloaded binary files (.pdf, images, .swf, media, etc.).
"""

import sqlite3
from urllib.parse import urlparse
from collections import Counter
import re
import os
import webbrowser
import json

STOPWORDS = {
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with',
    'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
    'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out',
    'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no',
    'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them',
    'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
    'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want',
    'because', 'any', 'these', 'give', 'day', 'most', 'us', 'is', 'are', 'was', 'were', 'been', 'has',
    'had', 'comments', 'comment', 'points', 'ago', 'hide', 'past', 'more'
}


def format_bytes(num_bytes):
    """
    Formats a byte size into human-readable representation (KB, MB, GB).
    """
    if not num_bytes:
        return "0 B"
    num = float(num_bytes)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f"{num:.1f} {unit}" if unit != 'B' else f"{int(num)} B"
        num /= 1024.0
    return f"{num:.2f} PB"


def analyze_crawler_data(db_path="crawler.db"):
    """
    Queries SQLite database and compiles metrics for both crawled pages and downloaded files.
    """
    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found.")
        return None

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Verify if 'pages' table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pages'")
    if not c.fetchone():
        print("Database does not contain 'pages' table.")
        conn.close()
        return None

    c.execute("SELECT id, url, title, content, status_code, crawled_at FROM pages")
    rows = c.fetchall()

    # Check for 'files' table
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files'")
    has_files_table = c.fetchone() is not None

    file_rows = []
    if has_files_table:
        c.execute("""
            SELECT id, url, file_path, file_name, file_type, file_size, mime_type, source_page, status_code, downloaded_at
            FROM files
        """)
        file_rows = c.fetchall()

    conn.close()

    if not rows and not file_rows:
        print("Database is empty. No crawled pages or files found.")
        return None

    # --- Process Pages ---
    total_pages = len(rows)
    domain_counter = Counter()
    status_counter = Counter()
    word_counter = Counter()
    total_content_length = 0
    pages_list = []

    for row in rows:
        row_id, url, title, content, status_code, crawled_at = row
        status_counter[status_code] += 1

        parsed = urlparse(url)
        domain = parsed.netloc or 'unknown'
        domain_counter[domain] += 1

        content_str = content or ""
        total_content_length += len(content_str)

        # Extract words for frequency
        words = re.findall(r'[a-zA-Z]{3,}', content_str.lower())
        for w in words:
            if w not in STOPWORDS:
                word_counter[w] += 1

        pages_list.append({
            "id": row_id,
            "url": url,
            "title": title or "(No Title)",
            "domain": domain,
            "status_code": status_code,
            "length": len(content_str),
            "snippet": (content_str[:150] + "...") if len(content_str) > 150 else content_str,
            "crawled_at": str(crawled_at)
        })

    avg_content_len = round(total_content_length / total_pages) if total_pages > 0 else 0

    # --- Process Files ---
    total_files = len(file_rows)
    file_type_counter = Counter()
    total_files_size = 0
    files_list = []

    for f_row in file_rows:
        f_id, f_url, f_path, f_name, f_type, f_size, f_mime, f_source, f_status, f_time = f_row
        size_int = f_size or 0
        total_files_size += size_int
        ftype_clean = (f_type or 'unknown').lower()
        if not ftype_clean.startswith('.') and ftype_clean != 'unknown':
            ftype_clean = '.' + ftype_clean
        file_type_counter[ftype_clean] += 1

        files_list.append({
            "id": f_id,
            "url": f_url,
            "file_name": f_name or os.path.basename(f_url),
            "file_type": ftype_clean,
            "file_path": f_path or "",
            "file_size": size_int,
            "file_size_formatted": format_bytes(size_int),
            "mime_type": f_mime or "",
            "source_page": f_source or "",
            "status_code": f_status,
            "downloaded_at": str(f_time)
        })

    return {
        "total_pages": total_pages,
        "avg_content_len": avg_content_len,
        "status_distribution": dict(status_counter),
        "domain_distribution": dict(domain_counter.most_common(10)),
        "top_keywords": word_counter.most_common(20),
        "pages": pages_list,
        # Files metrics
        "total_files": total_files,
        "total_files_size": total_files_size,
        "total_files_size_formatted": format_bytes(total_files_size),
        "file_type_distribution": dict(file_type_counter.most_common(15)),
        "files": files_list
    }


def print_terminal_summary(stats):
    """
    Prints a formatted summary report to stdout.
    """
    print("\n" + "=" * 65)
    print("                CRAWLER DATA ANALYSIS SUMMARY")
    print("=" * 65)
    print(f" Total Pages Crawled    : {stats['total_pages']}")
    print(f" Average Page Length    : {stats['avg_content_len']} characters")
    print(f" Total Files Downloaded : {stats['total_files']} ({stats['total_files_size_formatted']})")
    print("-" * 65)
    print(" HTTP Status Codes:")
    for code, count in stats['status_distribution'].items():
        print(f"   - HTTP {code}: {count} pages")

    if stats['total_files'] > 0:
        print("-" * 65)
        print(" Downloaded File Formats:")
        for ext, count in stats['file_type_distribution'].items():
            print(f"   - {ext:10s} : {count} files")

    print("-" * 65)
    print(" Top Domains Crawled:")
    for domain, count in stats['domain_distribution'].items():
        print(f"   - {domain}: {count} pages")

    if stats['top_keywords']:
        print("-" * 65)
        print(" Top 10 Keywords in Extracted Content:")
        for word, count in stats['top_keywords'][:10]:
            print(f"   - '{word}': {count} occurrences")
    print("=" * 65 + "\n")


def generate_html_report(stats, output_file="report.html"):
    """
    Builds a standalone interactive HTML dashboard using Chart.js.
    """
    labels_domains = list(stats['domain_distribution'].keys())
    counts_domains = list(stats['domain_distribution'].values())

    labels_status = [f"HTTP {k}" for k in stats['status_distribution'].keys()]
    counts_status = list(stats['status_distribution'].values())

    labels_keywords = [w[0] for w in stats['top_keywords'][:15]]
    counts_keywords = [w[1] for w in stats['top_keywords'][:15]]

    labels_files = list(stats['file_type_distribution'].keys())
    counts_files = list(stats['file_type_distribution'].values())

    pages_json = json.dumps(stats['pages'])
    files_json = json.dumps(stats['files'])

    success_pages = stats['status_distribution'].get(200, 0)
    success_rate = round(success_pages / stats['total_pages'] * 100, 1) if stats['total_pages'] > 0 else 0.0

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Crawler & File Downloader Analytics</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-darker: #121214;
            --bg-dark: #1a1a1e;
            --bg-card: #222228;
            --border: #32323a;
            --text-main: #d0d0d8;
            --text-bright: #ffffff;
            --accent: #4f80ff;
            --accent-green: #34d399;
            --accent-orange: #fbbf24;
            --accent-purple: #a78bfa;
            --accent-red: #f87171;
            --accent-cyan: #38bdf8;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg-darker);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 24px;
        }}
        .header {{
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 16px;
        }}
        h1 {{ color: var(--text-bright); font-size: 1.6rem; }}
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 18px;
        }}
        .kpi-title {{ font-size: 0.85rem; color: #888899; text-transform: uppercase; margin-bottom: 8px; }}
        .kpi-val {{ font-size: 1.8rem; font-weight: 700; color: var(--text-bright); }}
        .grid-charts {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }}
        .chart-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
            height: 380px;
            display: flex;
            flex-direction: column;
        }}
        .chart-container {{
            position: relative;
            flex: 1;
            width: 100%;
            min-height: 0;
        }}
        .chart-card h2 {{
            font-size: 1.1rem;
            margin-bottom: 16px;
            color: var(--text-bright);
        }}
        .tabs-header {{
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 8px;
        }}
        .tab-btn {{
            background: none;
            border: none;
            color: var(--text-main);
            font-size: 1.05rem;
            font-weight: 600;
            cursor: pointer;
            padding: 8px 16px;
            border-radius: 6px;
            transition: all 0.2s;
        }}
        .tab-btn.active {{
            background: var(--accent);
            color: #ffffff;
        }}
        .tab-btn:hover:not(.active) {{
            background: rgba(255,255,255,0.05);
            color: var(--text-bright);
        }}
        .table-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
            margin-bottom: 24px;
        }}
        .search-box {{
            width: 100%;
            padding: 10px 14px;
            background: var(--bg-dark);
            border: 1px solid var(--border);
            color: var(--text-bright);
            border-radius: 6px;
            margin-bottom: 16px;
            font-size: 0.95rem;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}
        th, td {{
            padding: 10px 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{
            background: var(--bg-dark);
            color: var(--text-bright);
            position: sticky;
            top: 0;
        }}
        tr:hover {{ background: rgba(255,255,255,0.03); }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .badge-200 {{ background: #064e3b; color: #6ee7b7; }}
        .badge-err {{ background: #7f1d1d; color: #fca5a5; }}
        .badge-ext {{ background: #1e1b4b; color: #a5b4fc; border: 1px solid #3730a3; }}
        a {{ color: var(--accent); text-decoration: none; word-break: break-all; }}
        a:hover {{ text-decoration: underline; }}
        .empty-state {{ text-align: center; color: #888899; padding: 30px; font-style: italic; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Crawler Analytics & Visual Dashboard</h1>
            <p style="color: #888899; margin-top: 4px;">Interactive analysis of <code>crawler.db</code></p>
        </div>
    </div>

    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-title">Total Pages Crawled</div>
            <div class="kpi-val" style="color: var(--accent);">{stats['total_pages']}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Success Rate</div>
            <div class="kpi-val" style="color: var(--accent-green);">{success_rate}%</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Files Downloaded</div>
            <div class="kpi-val" style="color: var(--accent-purple);">{stats['total_files']}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Storage Consumed</div>
            <div class="kpi-val" style="color: var(--accent-orange);">{stats['total_files_size_formatted']}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Unique Domains</div>
            <div class="kpi-val" style="color: var(--accent-cyan);">{len(stats['domain_distribution'])}</div>
        </div>
    </div>

    <div class="grid-charts">
        <div class="chart-card">
            <h2>Top Frequent Keywords in Content</h2>
            <div class="chart-container">
                <canvas id="keywordsChart"></canvas>
            </div>
        </div>
        <div class="chart-card">
            <h2>Pages Per Domain</h2>
            <div class="chart-container">
                <canvas id="domainsChart"></canvas>
            </div>
        </div>
        <div class="chart-card">
            <h2>Downloaded File Formats</h2>
            <div class="chart-container">
                <canvas id="filesChart"></canvas>
            </div>
        </div>
    </div>

    <div class="tabs-header">
        <button id="btnTabPages" class="tab-btn active" onclick="switchTab('pages')">Crawled Pages ({stats['total_pages']})</button>
        <button id="btnTabFiles" class="tab-btn" onclick="switchTab('files')">Downloaded Files ({stats['total_files']})</button>
    </div>

    <!-- Crawled Pages Section -->
    <div id="sectionPages" class="table-card">
        <h2 style="color: var(--text-bright); margin-bottom: 12px;">Crawled Pages Explorer</h2>
        <input type="text" id="searchPagesInput" class="search-box" placeholder="Filter pages by URL, Title, Domain or Content snippet...">
        <table>
            <thead>
                <tr>
                    <th style="width: 50px;">#</th>
                    <th style="width: 80px;">Status</th>
                    <th style="width: 260px;">Title</th>
                    <th>URL</th>
                    <th>Content Snippet</th>
                </tr>
            </thead>
            <tbody id="pagesTableBody"></tbody>
        </table>
    </div>

    <!-- Downloaded Files Section -->
    <div id="sectionFiles" class="table-card" style="display: none;">
        <h2 style="color: var(--text-bright); margin-bottom: 12px;">Downloaded Files Explorer</h2>
        <input type="text" id="searchFilesInput" class="search-box" placeholder="Filter files by File Name, Extension, URL or Source Page...">
        <table>
            <thead>
                <tr>
                    <th style="width: 50px;">#</th>
                    <th style="width: 80px;">Format</th>
                    <th style="width: 240px;">File Name</th>
                    <th style="width: 100px;">Size</th>
                    <th>Remote URL & Local Storage Path</th>
                    <th style="width: 220px;">Source Page</th>
                </tr>
            </thead>
            <tbody id="filesTableBody"></tbody>
        </table>
    </div>

    <script>
        const pagesData = {pages_json};
        const filesData = {files_json};

        // Render Keywords Chart
        new Chart(document.getElementById('keywordsChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(labels_keywords)},
                datasets: [{{
                    label: 'Occurrences',
                    data: {json.dumps(counts_keywords)},
                    backgroundColor: '#4f80ff',
                    borderRadius: 4
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ grid: {{ color: '#2a2a35' }}, ticks: {{ color: '#999' }} }},
                    y: {{ grid: {{ display: false }}, ticks: {{ color: '#ccc' }} }}
                }}
            }}
        }});

        // Render Domains Chart
        new Chart(document.getElementById('domainsChart'), {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(labels_domains)},
                datasets: [{{
                    data: {json.dumps(counts_domains)},
                    backgroundColor: ['#4f80ff', '#34d399', '#fbbf24', '#f87171', '#a78bfa', '#38bdf8']
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'bottom', labels: {{ color: '#ccc', boxWidth: 12 }} }}
                }}
            }}
        }});

        // Render Downloaded Files Chart
        const fileLabels = {json.dumps(labels_files)};
        const fileCounts = {json.dumps(counts_files)};
        if (fileLabels.length > 0) {{
            new Chart(document.getElementById('filesChart'), {{
                type: 'doughnut',
                data: {{
                    labels: fileLabels,
                    datasets: [{{
                        data: fileCounts,
                        backgroundColor: ['#a78bfa', '#fbbf24', '#34d399', '#f87171', '#38bdf8', '#ec4899', '#f97316']
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ color: '#ccc', boxWidth: 12 }} }}
                    }}
                }}
            }});
        }} else {{
            const canvas = document.getElementById('filesChart');
            const parent = canvas.parentElement;
            parent.innerHTML = '<div class="empty-state">No files downloaded yet.<br>Run crawler with <code>--file-types .pdf .swf images</code> to download files.</div>';
        }}

        // Tabs Logic
        function switchTab(tab) {{
            const secPages = document.getElementById('sectionPages');
            const secFiles = document.getElementById('sectionFiles');
            const btnPages = document.getElementById('btnTabPages');
            const btnFiles = document.getElementById('btnTabFiles');

            if (tab === 'pages') {{
                secPages.style.display = 'block';
                secFiles.style.display = 'none';
                btnPages.classList.add('active');
                btnFiles.classList.remove('active');
            }} else {{
                secPages.style.display = 'none';
                secFiles.style.display = 'block';
                btnFiles.classList.add('active');
                btnPages.classList.remove('active');
            }}
        }}

        function escapeHtml(text) {{
            return String(text || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
        }}

        // Render Pages Table
        const pagesTableBody = document.getElementById('pagesTableBody');
        function renderPages(data) {{
            pagesTableBody.innerHTML = '';
            if (data.length === 0) {{
                pagesTableBody.innerHTML = '<tr><td colspan="5" class="empty-state">No matching pages found</td></tr>';
                return;
            }}
            data.forEach((p, idx) => {{
                const badgeClass = p.status_code === 200 ? 'badge-200' : 'badge-err';
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${{idx + 1}}</td>
                    <td><span class="badge ${{badgeClass}}">${{p.status_code || 'ERR'}}</span></td>
                    <td><strong>${{escapeHtml(p.title)}}</strong></td>
                    <td><a href="${{escapeHtml(p.url)}}" target="_blank" rel="noopener">${{escapeHtml(p.url)}}</a></td>
                    <td style="color: #999; font-size: 0.85rem;">${{escapeHtml(p.snippet)}}</td>
                `;
                pagesTableBody.appendChild(row);
            }});
        }}

        // Render Files Table
        const filesTableBody = document.getElementById('filesTableBody');
        function renderFiles(data) {{
            filesTableBody.innerHTML = '';
            if (data.length === 0) {{
                filesTableBody.innerHTML = '<tr><td colspan="6" class="empty-state">No matching files found</td></tr>';
                return;
            }}
            data.forEach((f, idx) => {{
                const localFileUri = 'file:///' + encodeURI(f.file_path.replace(/\\\\/g, '/'));
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${{idx + 1}}</td>
                    <td><span class="badge badge-ext">${{escapeHtml(f.file_type || 'FILE')}}</span></td>
                    <td><strong>${{escapeHtml(f.file_name)}}</strong></td>
                    <td>${{escapeHtml(f.file_size_formatted)}}</td>
                    <td>
                        <div><a href="${{escapeHtml(f.url)}}" target="_blank" rel="noopener">${{escapeHtml(f.url)}}</a></div>
                        <div style="font-size: 0.8rem; color: #888899; margin-top: 4px;">
                            Local: <a href="${{localFileUri}}" target="_blank" rel="noopener" style="color: #a5b4fc;" title="Click to open local file">${{escapeHtml(f.file_path)}}</a>
                        </div>
                    </td>
                    <td>
                        ${{f.source_page ? `<a href="${{escapeHtml(f.source_page)}}" target="_blank" rel="noopener">${{escapeHtml(f.source_page)}}</a>` : '<span style="color: #666;">(Direct Seed)</span>'}}
                    </td>
                `;
                filesTableBody.appendChild(row);
            }});
        }}

        // Search Handlers
        document.getElementById('searchPagesInput').addEventListener('input', (e) => {{
            const query = e.target.value.toLowerCase();
            const filtered = pagesData.filter(p =>
                p.title.toLowerCase().includes(query) ||
                p.url.toLowerCase().includes(query) ||
                p.snippet.toLowerCase().includes(query) ||
                p.domain.toLowerCase().includes(query)
            );
            renderPages(filtered);
        }});

        document.getElementById('searchFilesInput').addEventListener('input', (e) => {{
            const query = e.target.value.toLowerCase();
            const filtered = filesData.filter(f =>
                f.file_name.toLowerCase().includes(query) ||
                f.file_type.toLowerCase().includes(query) ||
                f.url.toLowerCase().includes(query) ||
                f.source_page.toLowerCase().includes(query) ||
                f.file_path.toLowerCase().includes(query)
            );
            renderFiles(filtered);
        }});

        // Initial render
        renderPages(pagesData);
        renderFiles(filesData);
    </script>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n Visual report successfully generated: {os.path.abspath(output_file)}")
    return os.path.abspath(output_file)


if __name__ == "__main__":
    stats = analyze_crawler_data("crawler.db")
    if stats:
        print_terminal_summary(stats)
        report_path = generate_html_report(stats)
        print("Opening visual dashboard in your default browser...")
        webbrowser.open(f"file://{report_path}")
