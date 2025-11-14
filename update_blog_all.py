import requests
import re

RSS_URL = "https://www.rivasol.com.tr/index.php?route=journal3/blog/feed"
README_FILE = "README.md"


def fetch_rss_entries():
    print(f"RSS okunuyor: {RSS_URL}")
    response = requests.get(RSS_URL, timeout=30)
    response.raise_for_status()
    content = response.text

    # RSS içinden <item> bloklarını çek
    items = re.findall(r"<item>(.*?)</item>", content, re.DOTALL)
    posts = []

    for item in items:
        # Hem CDATA'lı hem CDATA'sız title yakala
        title_match = re.search(r"<title>(?:<!

\[CDATA

\[(.*?)\]

\]

>|(.*?))</title>", item)
        link_match = re.search(r"<link>(.*?)</link>", item)

        if not title_match or not link_match:
            continue

        title = (title_match.group(1) or title_match.group(2)).strip()
        link = link_match.group(1).strip()

        posts.append((title, link))

    print(f"Toplam bulunan yazı sayısı: {len(posts)}")
    return posts


def update_readme(posts):
    with open(README_FILE, "r", encoding="utf-8") as f:
        readme = f.read()

    start_tag = "<!-- BLOG-POST-LIST:START -->"
    end_tag = "<!-- BLOG-POST-LIST:END -->"

    start_index = readme.find(start_tag)
    end_index = readme.find(end_tag)

    if start_index == -1 or end_index == -1:
        print("Uyarı: README.md içinde BLOG-POST-LIST etiketleri bulunamadı. Dosya değiştirilmedi.")
        return

    # START etiketinin SONRASINA yazacağız
    start_index += len(start_tag)

    max_posts = 20
    limited_posts = posts[:max_posts]

    new_list = "\n" + "\n".join(
        f"- [{title}]({link})" for title, link in limited_posts
    ) + "\n"

    before = readme[:start_index]
    after = readme[end_index:]
    new_content = before + new_list + after

    if new_content == readme:
        print("Uyarı: README.md içeriği değişmedi (muhtemelen aynı liste zaten vardı).")
    else:
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md başarıyla güncellendi.")


if __name__ == "__main__":
    posts = fetch_rss_entries()
    update_readme(posts)
