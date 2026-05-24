from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Завантажуємо модель глобально при старті сервера
print("Ініціалізація AI-моделі...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def get_db_connection():
    conn = sqlite3.connect('vinyl_store.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/records', methods=['GET'])
def get_records():
    conn = get_db_connection()
    records = conn.execute('SELECT id, title, artist, price, image_url, genre, tags, bpm FROM records').fetchall()
    conn.close()
    return jsonify([dict(row) for row in records])

@app.route('/api/search', methods=['GET'])
def smart_search():
    query = request.args.get('q', '').strip()
    
    # Якщо пошук порожній, повертаємо всі товари
    if not query:
        return get_records()
    
    conn = get_db_connection()
    records = conn.execute('SELECT * FROM records WHERE embedding IS NOT NULL').fetchall()
    conn.close()

    # Перетворюємо запит користувача на вектор
    query_vector = model.encode([query])

    # Витягуємо вектори товарів з бази
    product_vectors = []
    product_list = []
    
    for row in records:
        product_list.append(dict(row))
        product_vectors.append(json.loads(row['embedding']))
    product_vectors = np.array(product_vectors)

    # Обчислюємо косинусну подібність
    similarities = cosine_similarity(query_vector, product_vectors)[0]

    # Додаємо оцінку подібності до кожного товару
    for i, product in enumerate(product_list):
        product['similarity'] = float(similarities[i])
        del product['embedding'] 

    # Сортуємо результати від найбільш схожих до найменш
    results = [p for p in product_list if p['similarity'] > 0.1]
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)