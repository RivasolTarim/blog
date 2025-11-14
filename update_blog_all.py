import requests
import xml.etree.ElementTree as ET
from pathlib import Path

# === AYARLAR ===
RSS_URL = "https://www.rivasol.com.tr/index.php?route=journal3/blog/feed"
README_PATH = Path("README.md")

START_TAG = "<!-- BLOG-POST-LIST:START -->"
END_TAG = "<!-- BLOG-POST-LIST:END -->"


def fetch_all_rss_items():
    """RSS içindeki TÜM <item> kayıtlarını döndürür."""
    resp = requests.get(RSS_URL, timeout=15)
    resp.raise_for_status()

    root = ET.fromstring(resp.content)

    items = []
    for item in root.findall(".//item"):
        title_el = item.find("title")
        link_el = item.find("link")
        date_el = item.find("pubDate")

        title = title_el.text.strip() if title_el is not None and title_el.text else "Başlıksız"
        link = link_el.text.strip() if link_el is not None and link_el.text else "#"
        pub_date = date_el.text.strip() if date_el is not None and date_el.text else ""

        items.append(
            {
                "title": title,
                "link": link,
                "pub_date": pub_date,
            }
        )

    return items


def build_markdown_list(items):
    """Blog yazılarını Markdown liste formatına çevirir."""
    if not items:
        return "_Şu an için listelenecek blog yazısı bulunamadı._"

    lines = []
    for i in items:
        if i["pub_date"]:
            line = f"- [{i['title']}]({i['link']})  \n  _{i['pub_date']}_"
        else:
            line = f"- [{i['title']}]({i['link']})"
        lines.append(line)

    return "\n".join(lines)


def update_readme(new_block: str):
    """README.md içindeki BLOG-POST-LIST blokunu günceller."""
    if not README_PATH.exists():
        raise SystemExit("README.md dosyası bulunamadı.")

    text = README_PATH.read_text(encoding="utf-8")

    if START_TAG not in text or END_TAG not in text:
        raise SystemExit("README içinde başlangıç/bitiş etiketleri bulunamadı.")

    start_idx = text.index(START_TAG) + len(START_TAG)
    end_idx = text.index(END_TAG)

    before = text[:start_idx]
    after = text[end_idx:]

    updated = before + "\n" + new_block + "\n" + after
    README_PATH.write_text(updated, encoding="utf-8")


def main():
    print(f"RSS okunuyor: {RSS_URL}")
    items = fetch_all_rss_items()
    print("Toplam bulunan yazı sayısı:", len(items))

    md_block = build_markdown_list(items)
    update_readme(md_block)
    print("README.md başarıyla güncellendi.")


if __name__ == "__main__":
    main()
