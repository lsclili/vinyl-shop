import sqlite3
import json
from sentence_transformers import SentenceTransformer

print("Завантаження AI-моделі...")
# Використовуємо багатомовну модель, щоб вона розуміла і українську, і англійську
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

conn = sqlite3.connect('vinyl_store.db')
cursor = conn.cursor()

# Додаємо колонку для векторів, якщо її ще немає
try:
    cursor.execute('ALTER TABLE records ADD COLUMN embedding TEXT')
except sqlite3.OperationalError:
    pass

print("Генерація векторів для товарів...")
cursor.execute('SELECT id, title, artist, genre, tags, bpm FROM records')
records = cursor.fetchall()

for row in records:
    record_id, title, artist, genre, tags, bpm = row
    text_to_vectorize = f"{title} {artist} {genre} {tags} {bpm} bpm"
    vector = model.encode(text_to_vectorize)
    vector_json = json.dumps(vector.tolist())
    
    cursor.execute('UPDATE records SET embedding = ? WHERE id = ?', (vector_json, record_id))

conn.commit()
conn.close()
print("Вектори успішно збережено в базу даних!")