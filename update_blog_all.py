import requests
import re

RSS_URL = "https://www.rivasol.com.tr/index.php?route=journal3/blog/feed"
README_FILE = "README.md"


def fetch_rss_entries():
    print(f"RSS okunuyor: {RSS_URL}")
    response = requests.get(RSS_URL, timeout=30)
    response.raise_for_status()

    content = response.text

    # <item> bloklarını al
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

    # Etiketleri boşluklara toleranslı yakalayalım
    pattern = (
        r"(<!--\s*BLOG-POST-LIST:START\s*-->)"
        r"([\s\S]*?)"
        r"(<!--\s*BLOG-POST-LIST:END\s*-->)"
    )

    new_list = "\n".join(f"- [{title}]({link})" for title, link in posts)

    def replacer(match):
        start_tag = match.group(1)
        end_tag = match.group(3)
        return f"{start_tag}\n{new_list}\n{end_tag}"

    new_content, count = re.subn(pattern, replacer, readme)

    if count == 0:
        print("UYARI: README içinde BLOG-POST-LIST bloğu bulunamadı. Etiketleri kontrol et.")
    else:
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"README.md başarıyla güncellendi. Güncellenen blok sayısı: {count}")


if __name__ == "__main__":
    posts = fetch_rss_entries()
    update_readme(posts)
