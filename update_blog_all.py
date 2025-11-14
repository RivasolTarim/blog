import requests
import re

RSS_URL = "https://www.rivasol.com.tr/index.php?route=journal3/blog/feed"
README_FILE = "README.md"

def fetch_rss_entries():
    print("RSS okunuyor:", RSS_URL)
    response = requests.get(RSS_URL)
    response.raise_for_status()

    content = response.text

    # RSS içinden title + link çekme
    items = re.findall(r"<item>(.*?)</item>", content, re.DOTALL)
    posts = []

    for item in items:
        title_match = re.search(r"<title><!\[CDATA\[(.*?)\]\]></title>", item)
        link_match = re.search(r"<link>(.*?)</link>", item)

        if title_match and link_match:
            title = title_match.group(1).strip()
            link = link_match.group(1).strip()
            posts.append((title, link))

    print(f"Toplam bulunan yazı sayısı: {len(posts)}")
    return posts


def update_readme(posts):
    with open(README_FILE, "r", encoding="utf-8") as f:
        readme = f.read()

    start_tag = "<!-- BLOG-POST-LIST:START -->"
    end_tag = "<!-- BLOG-POST-LIST:END -->"

    new_list = "\n".join([f"- [{title}]({link})" for title, link in posts])

    new_content = re.sub(
        f"{start_tag}(.|\n)*?{end_tag}",
        f"{start_tag}\n{new_list}\n{end_tag}",
        readme
    )

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README.md başarıyla güncellendi.")


if __name__ == "__main__":
    posts = fetch_rss_entries()
    update_readme(posts)
