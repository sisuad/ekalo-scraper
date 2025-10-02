import os
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.kiddoworksheets.com"
SAVE_DIR = "worksheets"
os.makedirs(SAVE_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0"}
SITEMAPS = [
    "https://www.kiddoworksheets.com/wpdmpro-sitemap.xml",
    "https://www.kiddoworksheets.com/wpdmpro-sitemap2.xml",
]
CATEGORY_SITEMAP = "https://www.kiddoworksheets.com/wpdmcategory-sitemap.xml"

# data grouped by category
data_log = {}

# 👇 toggle this flag
DOWNLOAD_PDFS = True   # True = download PDFs, False = just metadata


def get_soup(url, parser="xml"):
    """Fetch page and return BeautifulSoup object"""
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, parser)


def get_categories():
    """Get category mapping from category sitemap"""
    soup = get_soup(CATEGORY_SITEMAP)
    categories = {}
    for loc in soup.find_all("loc"):
        url = loc.text.strip()
        cat_name = url.rstrip("/").split("/")[-1].replace("-", " ").title()
        categories[url] = cat_name
    return categories


def get_worksheet_links():
    """Get all worksheet page URLs from wpdmpro sitemaps"""
    worksheet_links = []
    for sm in SITEMAPS:
        soup = get_soup(sm)
        worksheet_links += [loc.text.strip() for loc in soup.find_all("loc")]
    return worksheet_links


def is_direct_file_url(url):
    """Check if URL is a direct file link"""
    file_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.gif', '.doc', '.docx', '.zip']
    return any(url.lower().endswith(ext) for ext in file_extensions)


def process_worksheet(worksheet_url, categories):
    """Process worksheet (download if enabled, always log metadata)"""
    try:
        # Check if this is a direct file URL
        if is_direct_file_url(worksheet_url):
            # Handle direct file downloads
            filename = os.path.basename(worksheet_url).split('.')[0]  # Remove extension
            file_extension = os.path.splitext(worksheet_url)[1]  # Get original extension
            filepath = os.path.join(SAVE_DIR, f"{filename}{file_extension}")

            # Try to determine category from URL path
            category = "Direct Downloads"
            url_parts = worksheet_url.split('/')
            for part in url_parts:
                if any(keyword in part.lower() for keyword in ['math', 'reading', 'science', 'tracing', 'handwriting']):
                    category = part.replace('-', ' ').title()
                    break

            if category not in data_log:
                data_log[category] = []

            # metadata
            entry = {
                "name": filename,
                "url": worksheet_url,
                "file_path": filepath if DOWNLOAD_PDFS else None
            }

            # download file if enabled
            if DOWNLOAD_PDFS:
                resp = requests.get(worksheet_url, headers=HEADERS)
                if resp.status_code == 200:
                    with open(filepath, "wb") as f:
                        f.write(resp.content)
                    print(f"✅ Saved {filename}{file_extension} under category: {category}")
                    entry["file_path"] = filepath
                    time.sleep(2)
                else:
                    print(f"❌ Failed to download: {worksheet_url}")
            else:
                print(f"📝 Found direct file: {filename}{file_extension} in category: {category}")

            data_log[category].append(entry)
            return

        # Handle regular HTML pages with download buttons
        soup = get_soup(worksheet_url, parser="html.parser")

        # find download button
        download_btn = soup.find("a", href=lambda h: h and "wpdmdl=" in h)
        if not download_btn:
            print(f"❌ No download link: {worksheet_url}")
            return

        download_url = download_btn["href"]
        if not download_url.startswith("http"):
            download_url = urljoin(BASE_URL, download_url)

        # title for filename
        title = soup.find("h1")
        filename = title.text.strip().replace(" ", "_") if title else os.path.basename(download_url)
        filepath = os.path.join(SAVE_DIR, f"{filename}.pdf")

        # detect category
        category = "Uncategorized"
        breadcrumb = soup.select("div.breadcrumbs a[href*='/']")
        if breadcrumb:
            for b in breadcrumb:
                href = b.get("href", "")
                for cat_url, cat_name in categories.items():
                    if cat_url in href:
                        category = cat_name
                        break

        if category not in data_log:
            data_log[category] = []

        # metadata
        entry = {
            "name": filename,
            "url": worksheet_url,
            "file_path": filepath if DOWNLOAD_PDFS else None
        }

        # download file if enabled
        if DOWNLOAD_PDFS:
            resp = requests.get(download_url, headers=HEADERS)
            if resp.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(resp.content)
                print(f"✅ Saved {filename}.pdf under category: {category}")
                entry["file_path"] = filepath
                time.sleep(2)
            else:
                print(f"❌ Failed to download: {download_url}")

        data_log[category].append(entry)

    except Exception as e:
        print(f"⚠️ Error on {worksheet_url}: {e}")


def main():
    print("🔎 Fetching categories...")
    categories = get_categories()
    print(f"Found {len(categories)} categories")

    print("🔎 Fetching worksheet links...")
    worksheets = get_worksheet_links()
    print(f"Found {len(worksheets)} worksheets")

    for ws in worksheets:
        process_worksheet(ws, categories)

    # save JSON grouped by category
    with open("worksheets.json", "w", encoding="utf-8") as f:
        json.dump(data_log, f, indent=4, ensure_ascii=False)

    print("\n📄 worksheets.json created with metadata grouped by category")


if __name__ == "__main__":
    main()
