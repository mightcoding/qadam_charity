import sqlite3

def initialize_database():
    conn = sqlite3.connect("gifts.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS gifts")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            description TEXT NOT NULL,
            link TEXT NOT NULL
        )
    """)
    cursor.executemany("INSERT INTO gifts (name, price, description, link) VALUES (?, ?, ?, ?)", [
        ("MiDeer диапроектор Детские сказки", 8000, "Проектор для детей с волшебными сказками.", "https://kaspi.kz/shop/p/diaproektor-mideer-vosem-skazok-plastik-105179504/?c=710000000&m=30286789"),
        ("Кукла диапроектор Zabiaka", 3500, "Пластиковый диапроектор с куклой и сказками.", "https://kaspi.kz/shop/p/diaproektor-zabiaka-skazki-plastik-119480068"),
        ("Диапроектор Fisher Price Sweet Dreams Monitor", 24000, "Проектор для приятного сна от Fisher Price.", "https://kaspi.kz/shop/p/diaproektor-fisher-price-sweet-dreams-monitor-plastik-116679296"),
        ("GD растущая парта", 26500, "Удобная парта с растущей конструкцией.", "https://kaspi.kz/shop/p/gd-rastuschaja-parta-55x55x5-sm-belyi-korichnevyi-116601885"),
        ("Диапроектор радужный проектор", 31900, "Проектор с радужными эффектами для детей.", "https://kaspi.kz/shop/p/diaproektor-raduzhnyi-proektor-plastik-112639747"),
        ("Диапроектор для приятного сна", 7250, "Проектор для создания уютного детского сна.", "https://kaspi.kz/shop/p/diaproektor-aktivnyi-kroha-plastik-116840000"),
        ("Тройка джинсовый сарафан (рост 92)", 20000, "Джинсовый сарафан для девочки ростом 92 см.", ""),
        ("Кроссовки (23 размер)", 20000, "Удобные детские кроссовки размер 23.", ""),
        ("Планшет", 22900, "Детский планшет для развлечений и обучения.", "https://www.olx.kz/d/kk/obyavlenie/planshet-detskiy-podarok-1234"),
        ("Большая машинка на пульте управления", 4790, "Детская машинка на пульте с дистанционным управлением.", "https://kaspi.kz/shop/p/mashinka-na-pulte-123456"),
        ("Лего Duplo 10971", 5400, "Набор деталей Лего Duplo для детей.", "https://kaspi.kz/shop/p/lego-duplo-10971-detailei-123456")
    ])
    conn.commit()
    conn.close()

def get_gift_details(gift_id):
    conn = sqlite3.connect("gifts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, description, link FROM gifts WHERE id = ?", (gift_id,))
    gift = cursor.fetchone()
    conn.close()
    return gift

def delete_gift(gift_id):
    conn = sqlite3.connect("gifts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gifts WHERE id = ?", (gift_id,))
    conn.commit()
    conn.close()

def get_gifts_by_price(price_category):
    conn = sqlite3.connect("gifts.db")
    cursor = conn.cursor()
    if price_category == "under_15k":
        cursor.execute("SELECT id, name FROM gifts WHERE price <= 15000")
    elif price_category == "more_15k":
        cursor.execute("SELECT id, name FROM gifts WHERE price > 15000")
    gifts = cursor.fetchall()
    conn.close()
    return gifts
