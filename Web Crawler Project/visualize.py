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

def analyze_crawler_data(db_path="crawler.db"):
    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found.")
        return None

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT id, url, title, content, status_code, crawled_at FROM pages")
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("Database is empty. No crawled pages found.")
        return None

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

    return {
        "total_pages": total_pages,
        "avg_content_len": avg_content_len,
        "status_distribution": dict(status_counter),
        "domain_distribution": dict(domain_counter.most_common(10)),
        "top_keywords": word_counter.most_common(20),
        "pages": pages_list
    }

def print_terminal_summary(stats):
    print("\n" + "=" * 60)
    print("           CRAWLER DATA ANALYSIS SUMMARY")
    print("=" * 60)
    print(f" Total Pages Crawled : {stats['total_pages']}")
    print(f" Average Page Length : {stats['avg_content_len']} characters")
    print("-" * 60)
    print(" HTTP Status Codes:")
    for code, count in stats['status_distribution'].items():
        print(f"   - HTTP {code}: {count} pages")
    print("-" * 60)
    print(" Top Domains Crawled:")
    for domain, count in stats['domain_distribution'].items():
        print(f"   - {domain}: {count} pages")
    print("-" * 60)
    print(" Top 10 Keywords in Extracted Content:")
    for word, count in stats['top_keywords'][:10]:
        print(f"   - '{word}': {count} occurrences")
    print("=" * 60 + "\n")

def generate_html_report(stats, output_file="report.html"):
    labels_domains = list(stats['domain_distribution'].keys())
    counts_domains = list(stats['domain_distribution'].values())

    labels_status = [f"HTTP {k}" for k in stats['status_distribution'].keys()]
    counts_status = list(stats['status_distribution'].values())

    labels_keywords = [w[0] for w in stats['top_keywords'][:15]]
    counts_keywords = [w[1] for w in stats['top_keywords'][:15]]

    pages_json = json.dumps(stats['pages'])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Crawler Data Visualization</title>
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
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }}
        @media (max-width: 900px) {{
            .grid-2 {{ grid-template-columns: 1fr; }}
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
        .table-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
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
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .badge-200 {{ background: #064e3b; color: #6ee7b7; }}
        .badge-err {{ background: #7f1d1d; color: #fca5a5; }}
        a {{ color: var(--accent); text-decoration: none; word-break: break-all; }}
        a:hover {{ text-decoration: underline; }}
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
            <div class="kpi-val" style="color: var(--accent-green);">{round(stats['status_distribution'].get(200, 0) / stats['total_pages'] * 100, 1)}%</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Unique Domains</div>
            <div class="kpi-val" style="color: var(--accent-orange);">{len(stats['domain_distribution'])}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Avg Content Size</div>
            <div class="kpi-val">{stats['avg_content_len']} <span style="font-size: 0.9rem; font-weight: normal; color: #888;">chars</span></div>
        </div>
    </div>

    <div class="grid-2">
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
    </div>

    <div class="table-card">
        <h2 style="color: var(--text-bright); margin-bottom: 12px;">Crawled Pages Explorer</h2>
        <input type="text" id="searchInput" class="search-box" placeholder="Filter by URL, Title, Domain or Content snippet...">
        <table>
            <thead>
                <tr>
                    <th style="width: 50px;">#</th>
                    <th style="width: 80px;">Status</th>
                    <th style="width: 250px;">Title</th>
                    <th>URL</th>
                    <th>Content Snippet</th>
                </tr>
            </thead>
            <tbody id="pagesTableBody"></tbody>
        </table>
    </div>

    <script>
        const pagesData = {pages_json};

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
                    legend: {{ position: 'bottom', labels: {{ color: '#ccc', boxWidth: 14 }} }}
                }}
            }}
        }});

        // Populate Table with Search
        const tableBody = document.getElementById('pagesTableBody');
        const searchInput = document.getElementById('searchInput');

        function renderTable(data) {{
            tableBody.innerHTML = '';
            if (data.length === 0) {{
                tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #888; padding: 20px;">No matching pages found</td></tr>';
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
                tableBody.appendChild(row);
            }});
        }}

        function escapeHtml(text) {{
            return String(text || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
        }}

        searchInput.addEventListener('input', (e) => {{
            const query = e.target.value.toLowerCase();
            const filtered = pagesData.filter(p => 
                p.title.toLowerCase().includes(query) ||
                p.url.toLowerCase().includes(query) ||
                p.snippet.toLowerCase().includes(query) ||
                p.domain.toLowerCase().includes(query)
            );
            renderTable(filtered);
        }});

        renderTable(pagesData);
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
