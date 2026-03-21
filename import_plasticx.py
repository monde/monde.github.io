#!/usr/bin/env python3
"""Import plasti.cx Obtvse blog posts and Typo pages into Jekyll."""

import re
import sys
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

# --- Configuration ---

PLASTICX_DIR = Path(__file__).parent / ".." / "old-blog-content" / "websites" / "plasti.cx"
POSTS_DIR = Path(__file__).parent / "_posts"
PAGES_DIR = Path(__file__).parent / "_pages"

OBTVSE_SLUGS = [
    "distribute-scripts-as-gist-micro-gems",
    "maintaining-my-copy-of-obtvse",
    "report-resque-exceptions-to-honeybadger",
    "seattle-dot-rb-irb-presentation",
    "seattle-dot-rb-refactoring-talk",
    "switched-my-blog-to-obtvse-from-typo",
]

TYPO_PAGES = {
    "home": {"title": "About", "permalink": "/about/", "nav_order": 4},
    "carp": {"title": "Carp", "permalink": "/carp/", "nav_order": 5},
    "tp-t42": {"title": "ThinkPad T42", "permalink": "/tp-t42/", "nav_order": 6},
}

LANG_HINTS = [
    (re.compile(r"^\s*#!.*\b(python|ruby|bash|sh|perl)\b", re.M), None),
    (re.compile(r"\b(def |class |module |require |gem |puts |attr_)\b"), "ruby"),
    (re.compile(r"\birb\b.*=>"), "ruby"),
    (re.compile(r"(\$\s|^\s*#\s|apt-get|yum|emerge|sudo|cd |mkdir |chmod |chown |cp |mv |ls |cat |grep |find |tar |curl |wget |bundle )", re.M), "bash"),
    (re.compile(r"<%(=|\s)"), "erb"),
    (re.compile(r"(import\s+\w|from\s+\w+\s+import|print\()", re.M), "python"),
    (re.compile(r"(public\s+class|private\s+void|System\.out|import\s+java)", re.M), "java"),
    (re.compile(r"(CREATE TABLE|SELECT\s+\*|INSERT INTO|ALTER TABLE)", re.I | re.M), "sql"),
    (re.compile(r"(server\s*\{|location\s*/|RewriteRule|DocumentRoot|VirtualHost)", re.M), "apache"),
]


def detect_language(code_text):
    for pattern, lang in LANG_HINTS:
        m = pattern.search(code_text)
        if m:
            if lang is None:
                shebang_match = re.search(r"\b(python|ruby|bash|sh|perl)\b", m.group(0))
                return shebang_match.group(1) if shebang_match else None
            return lang
    return None


class PlasticxConverter(MarkdownConverter):
    """Converter that preserves images with fixed paths and adds language hints."""

    def convert_pre(self, el, text, parent_tags):
        # Check for <code class="lang"> inside <pre>
        code_el = el.find("code")
        lang = None
        if code_el and code_el.get("class"):
            lang = code_el["class"][0] if isinstance(code_el["class"], list) else code_el["class"]
        if not lang:
            lang = detect_language(el.get_text())
        lang_hint = lang if lang else ""
        content = el.get_text("\n").strip("\n")
        return f"\n\n```{lang_hint}\n{content}\n```\n\n"

    def convert_img(self, el, text, parent_tags):
        src = el.get("src", "")
        alt = el.get("alt", "")
        title = el.get("title", "")
        # Fix image paths
        if "./files/" in src:
            filename = src.split("./files/")[-1]
            src = f"/assets/images/{filename}"
        elif src.startswith("./files/"):
            filename = src[len("./files/"):]
            src = f"/assets/images/{filename}"
        title_part = f' "{title}"' if title else ""
        return f"![{alt}]({src}{title_part})"


def convert_with_images(html_content):
    return PlasticxConverter(
        heading_style="atx",
        bullets="-",
    ).convert(html_content)


def convert_without_images(html_content):
    return PlasticxConverter(
        heading_style="atx",
        bullets="-",
        strip=["img"],
    ).convert(html_content)


def parse_obtvse_date(time_text):
    """Parse 'Posted January 20, 2013' → '2013-01-20'"""
    time_text = time_text.replace("Posted ", "").strip()
    dt = datetime.strptime(time_text, "%B %d, %Y")
    return dt.strftime("%Y-%m-%d")


def import_obtvse_post(slug):
    filepath = PLASTICX_DIR / slug / "index.html"
    if not filepath.exists():
        print(f"  ERROR: File not found: {filepath}")
        return None

    html = filepath.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "lxml")

    # Title from <title>, strip " - Plasticx Blog"
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else slug.replace("-", " ")
    title = re.sub(r"\s*-\s*Plasticx Blog$", "", title)
    title = title.replace('"', '\\"')

    # Date from <time> element
    time_tag = soup.find("time")
    if not time_tag:
        print(f"  ERROR: No <time> element in {slug}")
        return None
    date = parse_obtvse_date(time_tag.get_text())

    # Content from section > div.post.contain
    section = soup.find("section", id=re.compile(r"^post-\d+$"))
    if not section:
        print(f"  ERROR: No post section in {slug}")
        return None

    post_div = section.find("div", class_="post")
    if not post_div:
        print(f"  ERROR: No .post div in {slug}")
        return None

    # Remove the h1 title (already in front matter)
    h1 = post_div.find("h1")
    if h1:
        h1.decompose()

    # Remove "Back to Blog" button
    for a in post_div.find_all("a", class_="button"):
        a.decompose()

    body_html = str(post_div)
    markdown_body = convert_without_images(body_html)
    markdown_body = re.sub(r"\n{3,}", "\n\n", markdown_body)
    markdown_body = markdown_body.strip()

    front_matter = f'---\ntitle: "{title}"\ndate: {date}\n---\n'
    filename = f"{date}-{slug}.md"

    return {
        "filename": filename,
        "content": f"{front_matter}\n{markdown_body}\n",
        "title": title,
        "date": date,
    }


def import_typo_page(page_slug, meta):
    filepath = PLASTICX_DIR / "pages" / page_slug / "index.html"
    if not filepath.exists():
        print(f"  ERROR: File not found: {filepath}")
        return None

    html = filepath.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "lxml")

    # Content from div#viewpage
    viewpage = soup.find("div", id="viewpage")
    if not viewpage:
        print(f"  ERROR: No #viewpage div in {page_slug}")
        return None

    # Remove the h2 title (will be in front matter)
    h2 = viewpage.find("h2")
    if h2:
        h2.decompose()

    body_html = str(viewpage)
    markdown_body = convert_with_images(body_html)
    markdown_body = re.sub(r"\n{3,}", "\n\n", markdown_body)
    markdown_body = markdown_body.strip()

    front_matter = f'---\ntitle: "{meta["title"]}"\npermalink: {meta["permalink"]}\nnav_order: {meta["nav_order"]}\n---\n'

    # Determine output filename
    if page_slug == "home":
        filename = "about.md"
    else:
        filename = f"{page_slug}.md"

    return {
        "filename": filename,
        "content": f"{front_matter}\n{markdown_body}\n",
        "title": meta["title"],
    }


def main():
    plasticx_dir = PLASTICX_DIR.resolve()
    posts_dir = POSTS_DIR.resolve()
    pages_dir = PAGES_DIR.resolve()

    if not plasticx_dir.exists():
        print(f"ERROR: plasti.cx directory not found: {plasticx_dir}")
        sys.exit(1)

    print(f"Source: {plasticx_dir}")
    print(f"Posts output: {posts_dir}")
    print(f"Pages output: {pages_dir}")
    print()

    # --- Import Obtvse blog posts ---
    print(f"=== Importing {len(OBTVSE_SLUGS)} Obtvse blog posts ===\n")
    post_count = 0
    post_errors = []

    for slug in OBTVSE_SLUGS:
        print(f"  Processing: {slug}")
        try:
            post = import_obtvse_post(slug)
            if post is None:
                post_errors.append(slug)
                continue
            out_path = posts_dir / post["filename"]
            out_path.write_text(post["content"], encoding="utf-8")
            print(f"    → {post['filename']}  ({post['title']})")
            post_count += 1
        except Exception as e:
            post_errors.append(slug)
            print(f"    ERROR: {e}")

    # --- Import Typo pages ---
    print(f"\n=== Importing {len(TYPO_PAGES)} Typo pages ===\n")
    page_count = 0
    page_errors = []

    for page_slug, meta in TYPO_PAGES.items():
        print(f"  Processing: pages/{page_slug}")
        try:
            page = import_typo_page(page_slug, meta)
            if page is None:
                page_errors.append(page_slug)
                continue
            out_path = pages_dir / page["filename"]
            out_path.write_text(page["content"], encoding="utf-8")
            print(f"    → _pages/{page['filename']}  ({page['title']})")
            page_count += 1
        except Exception as e:
            page_errors.append(page_slug)
            print(f"    ERROR: {e}")

    # --- Summary ---
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Posts converted: {post_count}/{len(OBTVSE_SLUGS)}")
    print(f"  Pages converted: {page_count}/{len(TYPO_PAGES)}")
    if post_errors:
        print(f"  Post errors: {post_errors}")
    if page_errors:
        print(f"  Page errors: {page_errors}")
    print()


if __name__ == "__main__":
    main()
