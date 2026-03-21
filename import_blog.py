#!/usr/bin/env python3
"""Import old Typo blog posts into Jekyll-compatible markdown files."""

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Comment
from markdownify import markdownify as md, MarkdownConverter

# --- Configuration ---

ARTICLES_DIR = Path(__file__).parent / ".." / "old-blog-content" / "websites" / "blog.mondragon.cc" / "articles"
OUTPUT_DIR = Path(__file__).parent / "_posts"
PATH_PATTERN = re.compile(r"(\d{4})/(\d{2})/(\d{2})/([a-zA-Z0-9_-]+)/index\.html$")

# Language detection heuristics for code blocks
LANG_HINTS = [
    (re.compile(r"^\s*#!.*\b(python|ruby|bash|sh|perl)\b", re.M), None),  # shebang
    (re.compile(r"\b(def |class |module |require |gem |puts |attr_)\b"), "ruby"),
    (re.compile(r"\birb\b.*=>"), "ruby"),
    (re.compile(r"(\$\s|^\s*#\s|apt-get|yum|emerge|sudo|cd |mkdir |chmod |chown |cp |mv |ls |cat |grep |find |tar |curl |wget )", re.M), "bash"),
    (re.compile(r"<%(=|\s)"), "erb"),
    (re.compile(r"(import\s+\w|from\s+\w+\s+import|print\()", re.M), "python"),
    (re.compile(r"(public\s+class|private\s+void|System\.out|import\s+java)", re.M), "java"),
    (re.compile(r"(<\w+>|</\w+>|xmlns)", re.M), "html"),
    (re.compile(r"(CREATE TABLE|SELECT\s+\*|INSERT INTO|ALTER TABLE)", re.I | re.M), "sql"),
    (re.compile(r"(server\s*\{|location\s*/|RewriteRule|DocumentRoot|VirtualHost)", re.M), "apache"),
]


def detect_language(code_text):
    """Try to detect the programming language of a code block."""
    for pattern, lang in LANG_HINTS:
        m = pattern.search(code_text)
        if m:
            if lang is None:
                # Shebang — extract language from it
                shebang_match = re.search(r"\b(python|ruby|bash|sh|perl)\b", m.group(0))
                return shebang_match.group(1) if shebang_match else None
            return lang
    return None


class BlogConverter(MarkdownConverter):
    """Custom converter that adds language hints to code blocks."""

    def convert_pre(self, el, text, parent_tags):
        code_text = el.get_text()
        lang = detect_language(code_text)
        lang_hint = lang if lang else ""

        # Clean up the text content
        content = el.get_text("\n")
        # Remove leading/trailing blank lines
        content = content.strip("\n")

        return f"\n\n```{lang_hint}\n{content}\n```\n\n"


def convert_html_to_markdown(html_content):
    """Convert HTML to markdown using our custom converter."""
    return BlogConverter(
        heading_style="atx",
        bullets="-",
        strip=["img"],  # strip images with broken relative paths
    ).convert(html_content)


def extract_post(filepath, rel_path):
    """Extract post data from an old Typo blog HTML file."""
    match = PATH_PATTERN.search(rel_path)
    if not match:
        return None

    year, month, day, slug = match.groups()
    date = f"{year}-{month}-{day}"

    html = filepath.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "lxml")

    # --- Title ---
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else slug.replace("-", " ").title()
    # Escape quotes in title for YAML
    title = title.replace('"', '\\"')

    # --- Categories ---
    categories = []
    cat_li = soup.find("li", class_="categories")
    if cat_li:
        for a in cat_li.find_all("a"):
            categories.append(a.get_text(strip=True))

    # --- Tags ---
    tags = []
    tag_li = soup.find("li", class_="tags")
    if tag_li:
        for a in tag_li.find_all("a"):
            tags.append(a.get_text(strip=True))

    # --- Content ---
    article_div = soup.find("div", class_="atomentry")
    if not article_div:
        print(f"  WARNING: No .atomentry div found in {rel_path}")
        return None

    # Get the content div(s)
    content_div = article_div.find("div", class_="content")
    extended_div = article_div.find("div", class_="extended")

    if not content_div:
        print(f"  WARNING: No .content div found in {rel_path}")
        return None

    # Remove elements we don't want before converting
    for element in content_div.find_all("span", class_="typo_notable_line"):
        element.decompose()
    for element in content_div.find_all("span", class_="typo_notable"):
        element.decompose()

    # Convert content to markdown
    body_html = str(content_div)
    if extended_div:
        # Clean notable from extended too
        for element in extended_div.find_all("span", class_="typo_notable_line"):
            element.decompose()
        for element in extended_div.find_all("span", class_="typo_notable"):
            element.decompose()
        body_html += "\n" + str(extended_div)

    markdown_body = convert_html_to_markdown(body_html)

    # Clean up: remove the wrapping div tags that markdownify may leave
    # Remove excessive blank lines (3+ → 2)
    markdown_body = re.sub(r"\n{3,}", "\n\n", markdown_body)
    markdown_body = markdown_body.strip()

    # --- Build front matter ---
    front_matter = f'---\ntitle: "{title}"\ndate: {date}\n'
    if categories:
        front_matter += f"categories: [{', '.join(categories)}]\n"
    if tags:
        front_matter += f"tags: [{', '.join(tags)}]\n"
    front_matter += "---\n"

    return {
        "filename": f"{date}-{slug}.md",
        "content": f"{front_matter}\n{markdown_body}\n",
        "title": title,
        "date": date,
        "slug": slug,
    }


def main():
    articles_dir = ARTICLES_DIR.resolve()
    output_dir = OUTPUT_DIR.resolve()

    if not articles_dir.exists():
        print(f"ERROR: Articles directory not found: {articles_dir}")
        sys.exit(1)

    print(f"Source: {articles_dir}")
    print(f"Output: {output_dir}")
    print()

    # Discover files
    found = []
    for f in sorted(articles_dir.rglob("index.html")):
        rel = str(f.relative_to(articles_dir))
        if PATH_PATTERN.search(rel) and "#" not in rel:
            found.append((f, rel))

    print(f"Found {len(found)} blog posts to import.\n")

    converted = 0
    skipped = 0
    errors = []

    for filepath, rel_path in found:
        print(f"  Processing: {rel_path}")
        try:
            post = extract_post(filepath, rel_path)
            if post is None:
                skipped += 1
                continue

            out_path = output_dir / post["filename"]
            out_path.write_text(post["content"], encoding="utf-8")
            print(f"    → {post['filename']}  ({post['title']})")
            converted += 1
        except Exception as e:
            errors.append((rel_path, str(e)))
            print(f"    ERROR: {e}")

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Found:     {len(found)}")
    print(f"  Converted: {converted}")
    print(f"  Skipped:   {skipped}")
    print(f"  Errors:    {len(errors)}")
    if errors:
        print("\nErrors:")
        for path, err in errors:
            print(f"  {path}: {err}")
    print()


if __name__ == "__main__":
    main()
