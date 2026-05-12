import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
DB_PATH = 'database.db'
UPLOAD_FOLDER = 'static/img'
app.secret_key = 'super_slepena_parole_123'
ADMIN_ACCESS_CODE = "OVG2026" # Šis ir kods, ko zinās tikai dežurants
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Inicializē datubāzi
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
        # Noklusējuma statuss, ja tabula ir tukša
        if not db.execute('SELECT 1 FROM Manta_Statuss').fetchone():
            db.execute('INSERT INTO Manta_Statuss (statuss) VALUES (?)', ("Pie Dežuranta",))
        db.commit()

init_db()

@app.route('/')
def index():
    query = request.args.get('q', '').strip()
    db = get_db()
    
    if query:
        # Meklē nosaukumā un aprakstā (izmantojot LIKE)
        items = db.execute('''
            SELECT M.*, S.statuss FROM Manta M 
            JOIN Manta_Statuss S ON M.statuss_id = S.statuss_id 
            WHERE M.nosaukums LIKE ? OR M.apraksts LIKE ?
            ORDER BY registracijas_laiks DESC
        ''', (f'%{query}%', f'%{query}%')).fetchall()
    else:
        items = db.execute('''
            SELECT M.*, S.statuss FROM Manta M 
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
            # Izveido unikālu faila nosaukumu
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

@app.route('/admin')
def admin_panel():
    # Pārbaudām, vai lietotājs ir "autorizēts" sesijā
    if not session.get('is_admin'):
        return "Piekļuve liegta. Jums nav tiesību skatīt šo lapu.", 403
    
    db = get_db()
    items = db.execute('''
        SELECT M.*, S.statuss FROM Manta M 
        JOIN Manta_Statuss S ON M.statuss_id = S.statuss_id 
        ORDER BY registracijas_laiks DESC
    ''').fetchall()
    return render_template('admin.html', items=items)

@app.route('/unlock/<string:code>')
def unlock_admin(code):
    if code == ADMIN_ACCESS_CODE:
        session['is_admin'] = True
        return redirect(url_for('admin_panel'))
    return "Nepareizs kods.", 401

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if not session.get('is_admin'):
        return "Forbidden", 403
    
    db = get_db()
    db.execute('DELETE FROM Manta WHERE manta_id = ?', (item_id,))
    db.commit()
    return redirect(url_for('admin_panel'))
if __name__ == '__main__':
    app.run(debug=True)