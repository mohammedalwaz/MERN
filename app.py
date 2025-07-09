from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('photos.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS photos (id INTEGER PRIMARY KEY, name TEXT, image BLOB)''')
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM photos")
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', photos=data)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['photo']
        name = file.filename
        img = file.read()

        conn = sqlite3.connect('photos.db')
        conn.execute("INSERT INTO photos (name, image) VALUES (?, ?)", (name, img))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('upload.html')

@app.route('/photo/<int:photo_id>')
def photo(photo_id):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT image FROM photos WHERE id=?", (photo_id,))
    data = cursor.fetchone()[0]
    conn.close()
    return data, 200, {'Content-Type': 'image/jpeg'}

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
