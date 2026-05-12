from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def add_item():
    return render_template('add_item.html')

if __name__ == '__main__':
    # debug=True automatically reloads the server when you save changes
    app.run(debug=True)