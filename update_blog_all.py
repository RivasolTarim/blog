import requests
import re

RSS_URL = "https://www.rivasol.com.tr/index.php?route=journal3/blog/feed"
README_FILE = "README.md"

def fetch_rss_entries():
    response = requests.get(RSS_URL)
    response.raise_for_status()
    content = response.text

    items = re.findall(r"<item>(.*?)</item>", content, re.DOTALL)
    posts = []

    for item in items:
        title_match = re.search(r"<title><!\[CDATA\[(.*?)\]\]></title>", item)
        link_match = re.search(r"<link>(.*?)</link>", item)

        if title_match and link_match:
            title = title_match.group(1).strip()
            link = link_match.group(1).strip()
            posts.append((title, link))
    
    print("Toplam bulunan yazı sayısı:", len(posts))
    return posts


def update_readme(posts):
    with open(README_FILE, "r", encoding="utf-8") as f:
        readme = f.read()

    start_tag = "<!-- BLOG-POST-LIST:START -->"
    end_tag = "<!-- BLOG-POST-LIST:END -->"

    # Güçlü multiline eşleşmesi
    pattern = re.compile(
        start_tag + r"(.*?)" + end_tag,
        re.DOTALL
    )

    # Yeni içerik
    list_text = "\n".join([f"- [{title}]({link})" for title, link in posts])

    new_block = f"{start_tag}\n{list_text}\n{end_tag}"

    updated = pattern.sub(new_block, readme)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated)

    print("README.md başarıyla güncellendi.")


if __name__ == "__main__":
    posts = fetch_rss_entries()
    update_readme(posts)
