import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
DB_PATH = 'database.db'
# Norāde uz jūsu esošo mapi
UPLOAD_FOLDER = 'static/img'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Inicializējam datubāzi pēc dokumentācijā norādītā ER modeļa
def init_db():
    with get_db() as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS Manta_Statuss (
                statuss_id INTEGER PRIMARY KEY AUTOINCREMENT,
                statuss TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS Manta (
                manta_id INTEGER PRIMARY KEY AUTOINCREMENT,
                nosaukums TEXT NOT NULL,
                apraksts TEXT NOT NULL,
                bilde_url TEXT NOT NULL,
                registracijas_laiks TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                statuss_id INTEGER DEFAULT 1,
                FOREIGN KEY (statuss_id) REFERENCES Manta_Statuss (statuss_id)
            );
        ''')
        # Pievienojam noklusējuma statusu, ja tabula ir tukša
        if not db.execute('SELECT 1 FROM Manta_Statuss').fetchone():
            db.execute('INSERT INTO Manta_Statuss (statuss) VALUES (?)', ("Pie Dežuranta",))
        db.commit()

init_db()

@app.route('/')
def index():
    db = get_db()
    # Atlasām mantas kopā ar to statusu no datubāzes
    items = db.execute('''
        SELECT M.*, S.statuss 
        FROM Manta M 
        JOIN Manta_Statuss S ON M.statuss_id = S.statuss_id 
        ORDER BY registracijas_laiks DESC
    ''').fetchall()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        file = request.files['photo']
        
        if file and title and desc:
            # Izveidojam unikālu faila nosaukumu
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            db = get_db()
            db.execute(
                'INSERT INTO Manta (nosaukums, apraksts, bilde_url) VALUES (?, ?, ?)',
                (title, desc, filename)
            )
            db.commit()
            return redirect(url_for('index'))
            
    return render_template('add_item.html')

if __name__ == '__main__':
    app.run(debug=True)