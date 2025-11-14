import requests
import re
import html

RSS_URL = "https://www.rivasol.com.tr/index.php?route=journal3/blog/feed"
README_FILE = "README.md"


def fetch_rss_entries():
    print("RSS okunuyor:", RSS_URL)

    response = requests.get(RSS_URL, timeout=30)
    response.raise_for_status()

    content = response.text

    # RSS içindeki <item> bloklarını al
    items = re.findall(r"<item>(.*?)</item>", content, re.DOTALL)
    posts = []

    for item in items:
        title_match = re.search(r"<title><!\[CDATA\[(.*?)\]\]></title>", item)
        link_match = re.search(r"<link>(.*?)</link>", item)

        if title_match and link_match:
            raw_title = title_match.group(1).strip()
            link = link_match.group(1).strip()

            # HTML entity’leri çöz (örn. &amp;)
            title = html.unescape(raw_title)

            posts.append((title, link))

    print(f"Toplam bulunan yazı sayısı: {len(posts)}")

    # Çok uzun olmasın diye ilk 30 yazıyı al istersen:
    # return posts[:30]
    return posts


def update_readme(posts):
    with open(README_FILE, "r", encoding="utf-8") as f:
        readme = f.read()

    start_tag = "<!-- BLOG-POST-LIST:START -->"
    end_tag = "<!-- BLOG-POST-LIST:END -->"

    if start_tag not in readme or end_tag not in readme:
        print("README içinde RSS için START/END satırları bulunamadı. Dosya değiştirilmedi.")
        return

    # START ve END tag’lerinin pozisyonlarını bul
    start_index = readme.index(start_tag)
    end_index = readme.index(end_tag)

    # START satırına kadar olan kısmı koru (START dahil)
    before = readme[: start_index + len(start_tag)]
    # END tag’inden SONRASINI koru (END hariç)
    after = readme[end_index + len(end_tag) :]

    if posts:
        list_lines = "\n" + "\n".join(
            f"- [{title}]({link})" for title, link in posts
        )
    else:
        list_lines = "\nLoading..."

    # Yeni README: before + liste + END tag + after
    new_readme = before + list_lines + "\n" + end_tag + after

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("README.md başarıyla güncellendi.")


if __name__ == "__main__":
    posts = fetch_rss_entries()
    update_readme(posts)
