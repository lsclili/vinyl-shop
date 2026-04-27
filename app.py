from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('vinyl_store.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/records', methods=['GET'])
def get_records():
    conn = get_db_connection()
    records = conn.execute('SELECT * FROM records').fetchall()
    conn.close()
    
    output = []
    for row in records:
        output.append({
            'id': row['id'],
            'title': row['title'],
            'artist': row['artist'],
            'price': row['price'],
            'image_url': row['image_url'],
            'genre': row['genre']
        })
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True, port=5000)