from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/newberichtsheft')
def newberichtsheft():
    return render_template('newberichtsheft.html')

@app.route('/userpage')
def userpage():
    return render_template('userpage.html')

@app.route('/tab2')
def tab2():
    return render_template('tab2.html')

if __name__ == '__main__':
    app.run(debug=True) 