import sqlite3
import urllib.request
import json

connection = sqlite3.connect('vinyl_store.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    price REAL NOT NULL,
    image_url TEXT,
    genre TEXT
)
''')

cursor.execute('DELETE FROM records')

search_terms = ['rock', 'jazz', 'electronic', 'pop']
all_vinyls = []

for term in search_terms:
    url = f"https://itunes.apple.com/search?term={term}&entity=album&limit=25"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        for item in data['results']:
            title = item.get('collectionName', 'Unknown Album')
            artist = item.get('artistName', 'Unknown Artist')
            # Генеруємо ціну
            price = item.get('collectionPrice', 10.00) + 15.00
            # Збільшуємо фото
            image_url = item.get('artworkUrl100', '').replace('100x100bb', '400x400bb')
            genre = item.get('primaryGenreName', term.capitalize())
            all_vinyls.append((title, artist, round(price, 2), image_url, genre))

cursor.executemany('''
INSERT INTO records (title, artist, price, image_url, genre)
VALUES (?, ?, ?, ?, ?)
''', all_vinyls)

connection.commit()
connection.close()

print(f"Успішно додано {len(all_vinyls)} платівок.")