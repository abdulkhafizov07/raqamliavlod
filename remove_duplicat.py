import sqlite3

DB = "db.sqlite3"
TABLE = "news_news"

def remove_duplicates():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Barcha title larni olish
    cur.execute(f"SELECT id, title FROM {TABLE} ORDER BY id")
    rows = cur.fetchall()

    seen = {}
    delete_ids = []

    for item_id, title in rows:
        if title in seen:
            # oldin bor bo‘lsa → o‘chirishga belgilaymiz
            delete_ids.append(item_id)
        else:
            seen[title] = item_id  # birinchi title saqlanadi

    print(f"O'chiriladigan dublikatlar soni: {len(delete_ids)}")

    # O'chirish
    for item_id in delete_ids:
        cur.execute(f"DELETE FROM {TABLE} WHERE id = ?", (item_id,))

    conn.commit()
    conn.close()

    print("Takrorlangan title lar tozalandi! Faqat yagona objectlar qoldi.")


if __name__ == "__main__":
    remove_duplicates()
