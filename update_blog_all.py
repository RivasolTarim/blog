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

    # Güçlü desen: tüm whitespace + satır sonlarını yakala
    pattern = re.compile(
        rf"{re.escape(start_tag)}[\s\S]*?{re.escape(end_tag)}",
        re.MULTILINE,
    )

    if not pattern.search(readme):
        print("UYARI: README içinde BLOG-POST-LIST etiketleri bulunamadı!")
        return

    # İstersen sadece son 50 yazıyı listele (tamamını istiyorsan [:50] kısmını sil)
    # posts_to_show = posts[:50]
    posts_to_show = posts

    new_list = "\n".join(
        f"- [{title}]({link})" for title, link in posts_to_show
    )

    replacement = f"{start_tag}\n{new_list}\n{end_tag}"

    new_content = pattern.sub(replacement, readme)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README.md başarıyla güncellendi (liste yazıldı).")


if __name__ == "__main__":
    posts = fetch_rss_entries()
    update_readme(posts)
