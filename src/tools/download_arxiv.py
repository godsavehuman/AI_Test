import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_arxiv_html(paper_id: str, output_dir: str = "./papers"):
    """
    Download an arXiv paper's HTML version and clean it.
    - Keeps only <section id="ltx_page_content"> (or full page if missing)
    - Keeps original images (no downloading)
    - Rewrites all relative `src="extracted/..."` to full arxiv.org URLs
    """
    base_url = f"https://arxiv.org/html/{paper_id}/"

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{paper_id}.html")

    print(f"Fetching HTML from {base_url} ...")
    r = requests.get(base_url)
    if r.status_code != 200:
        raise Exception(f"Failed to fetch {base_url}: HTTP {r.status_code}")

    soup = BeautifulSoup(r.text, "html.parser")

    # Extract main section or fallback
    main_section = soup.find("section", id="ltx_page_content")
    if main_section:
        print("✅ Found ltx_page_content section.")
        content = main_section
    else:
        print("⚠️ No ltx_page_content found — saving full page instead.")
        content = soup.body or soup

    # Fix relative src paths (images, scripts, etc.)
    for tag in content.find_all(src=True):
        src = tag["src"]
        # Only rewrite those starting with "extracted/"
        if src.startswith("extracted/"):
            full_src = urljoin(base_url, src)
            tag["src"] = full_src
            print(f"🔗 Rewrote src: {src} → {full_src}")

    # Remove unnecessary scripts and styles
    for tag in content.find_all(["script", "style"]):
        tag.decompose()

    # Save cleaned HTML
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(content))

    print(f"✅ Saved cleaned paper HTML to {output_file}")


if __name__ == "__main__":
    # Example usage
    download_arxiv_html("2507.03254v1")
