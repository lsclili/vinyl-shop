import sqlite3
import urllib.request
import json
import random 

connection = sqlite3.connect('vinyl_store.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    price REAL NOT NULL,
    image_url TEXT,
    genre TEXT,
    bpm INTEGER,
    tags TEXT
)
''')

cursor.execute('DELETE FROM records')

search_terms = ['rock', 'jazz', 'electronic', 'pop']
all_vinyls = []

# Словник тегів для різних жанрів, щоб дані виглядали реалістично
genre_tags = {
    'rock': ['guitar', 'classic', 'band', 'live', 'loud', 'vintage'],
    'jazz': ['saxophone', 'chill', 'smooth', 'instrumental', 'improvisation'],
    'electronic': ['dance', 'synth', 'club', 'bass', 'upbeat', 'techno'],
    'pop': ['vocal', 'hits', 'radio', 'catchy', 'modern', 'billboard']
}

for term in search_terms:
    url = f"https://itunes.apple.com/search?term={term}&entity=album&limit=25"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        for item in data['results']:
            title = item.get('collectionName', 'Unknown Album')
            artist = item.get('artistName', 'Unknown Artist')
            price = item.get('collectionPrice', 10.00) + 15.00
            image_url = item.get('artworkUrl100', '').replace('100x100bb', '400x400bb')
            genre = item.get('primaryGenreName', term.capitalize())
            
            # Генеруємо логічний BPM залежно від жанру
            if term == 'electronic':
                bpm = random.randint(120, 140)
            elif term == 'pop' or term == 'rock':
                bpm = random.randint(90, 125)
            else: # jazz
                bpm = random.randint(60, 100)
                
            # Вибираємо 2-3 випадкові теги для альбому
            tags = ", ".join(random.sample(genre_tags.get(term, ['music']), k=random.randint(2, 3)))
            all_vinyls.append((title, artist, round(price, 2), image_url, genre, bpm, tags))

cursor.executemany('''
INSERT INTO records (title, artist, price, image_url, genre, bpm, tags)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', all_vinyls)

connection.commit()
connection.close()

print(f"Успішно додано {len(all_vinyls)} платівок.")