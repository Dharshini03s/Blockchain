from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import blockChain
import re

app = Flask(__name__)

app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Panda@03'
app.config['MYSQL_DB'] = 'auction'

mysql = MySQL(app)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/buyer.html')
def buyer():
    return render_template('buyer.html')


@app.route('/seller.html')
def seller():
    return render_template('seller.html')


@app.route('/contact.html')
def contact():
    return render_template('contact.html')


@app.route('/buyerhome.html')
def buyerhome():
    return render_template('buyerhome.html')


@app.route('/sellerregister.html')
def sellerregister():
    return render_template('sellerregister.html')


@app.route('/sellerhome.html')
def sellerhome():
    return render_template('sellerhome.html')


@app.route("/blockchain.html")
def blockchain():
    return render_template('blockchain.html')


@app.route('/bregister', methods=['post', 'get'])
def bregister():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM buyer WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
            return render_template("buyer.html", msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template("buyer.html", msg=msg)
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            return render_template("buyer.html", msg=msg)
        elif not username or not password or not email or not phone:
            msg = 'Please fill out the form!'
            return render_template("buyerhome.html", msg=msg)
        else:
            msg = 'Your Data Successfully added into Blocks'
            text = username + password + email + phone
            if len(text) < 1:
                return render_template('index.html')
            try:
                make_proof = request.form['make_proof']
            except Exception:
                make_proof = False
            blockChain.write_block(text, make_proof)
            cursor.execute('INSERT INTO buyer VALUES (NULL, %s, %s, %s,%s)', (username, password, email, phone))
            mysql.connection.commit()
            return render_template('blockchain.html', msg=msg)


@app.route('/blogin', methods=['post', 'get'])
def blogin():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form["username"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM buyer WHERE username = %s AND password = %s', ([username, password]))
        account = cursor.fetchone()
        if account:
            session['logged'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            print("INN")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from stock")
            print("INN")
            data = cursor.fetchall()
            print(data)
            return render_template("buyerhome.html", data=data, username=username)
        else:
            msg = 'Incorrect username/password!'
        return render_template('buyer.html', msg=msg)


@app.route('/sellerlogin', methods=['post', 'get'])
def sellerlogin():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form["username"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM seller WHERE username = %s AND password = %s', ([username, password]))
        account = cursor.fetchone()
        if account:
            session['logged'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return render_template('sellerhome.html', username=username)
        else:
            msg = 'Incorrect username/password!'
        return render_template('seller.html', msg=msg)


@app.route('/s_register', methods=['post', 'get'])
def s_register():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM seller WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
            return render_template("sellerregister.html", msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template("sellerregister.html", msg=msg)
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            return render_template("sellerregister.html", msg=msg)
        elif not username or not password or not email or not phone:
            msg = 'Please fill out the form!'
            return render_template("sellerregister.html", msg=msg)
        else:
            msg = 'Your Data Successfully added into Blocks'
            text = username + password + email + phone
            if len(text) < 1:
                return render_template('index.html')
            try:
                make_proof = request.form['make_proof']
            except Exception:
                make_proof = False
            blockChain.write_block(text, make_proof)
            cursor.execute('INSERT INTO seller VALUES (NULL, %s, %s, %s,%s)', (username, password, email, phone))
            mysql.connection.commit()
            return render_template('blockchain.html', msg=msg)


@app.route('/check', methods=['POST'])
def integrity():
    results = blockChain.check_blocks_integrity()
    if request.method == 'POST':
        return render_template('blockchain.html', results=results)
    return render_template('index.html')


@app.route('/mining', methods=['POST'])
def mining():
    if request.method == 'POST':
        max_index = int(blockChain.get_next_block())

        for i in range(2, max_index):
            blockChain.get_POW(i)
        return render_template('blockchain.html', querry=max_index)
    return render_template('index.html')


@app.route('/addstockdata', methods=['post', 'get'])
def addstockdata():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        stockname = request.form['name']
        stockprice = request.form['price']
        stockid = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM stock WHERE stockname = %s', (stockname,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
            return render_template("sellerhome.html", msg=msg)
        elif not stockname or not stockprice or not stockid:
            msg = 'Please fill out the form!'
            return render_template("sellerhome.html", msg=msg)
        else:
            msg = 'Your Data Successfully added into Blocks'
            text = stockname + stockprice + stockid
            if len(text) < 1:
                return render_template('index.html')
            try:
                make_proof = request.form['make_proof']
            except Exception:
                make_proof = False
            blockChain.write_block(text, make_proof)
            cursor.execute('INSERT INTO stock VALUES (NULL, %s, %s, %s)', (stockname, stockprice, stockid))
            mysql.connection.commit()
            return render_template('blockchain.html', msg=msg)


@app.route('/buystock.html')
def buystock():
    return render_template('buystock.html')

@app.route('/book', methods=['post','get'])
def book():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        stockname = request.form['name']
        stockprice = request.form['price']
        stockid = request.form['id']
        if not stockname or not stockprice or not stockid:
            msg = 'Please fill out the form!'
            return render_template("buystock.html", msg=msg)
        else:
            msg = 'Your Data Successfully added into Blocks'
            text = stockname + stockprice + stockid
            if len(text) < 1:
                return render_template('index.html')
            try:
                make_proof = request.form['make_proof']
            except Exception:
                make_proof = False
            blockChain.write_block(text, make_proof)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO book VALUES (NULL, %s, %s, %s)', (stockname, stockprice, stockid))
            mysql.connection.commit()
            return render_template('blockchain.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True, port=8001, host='0.0.0.0')
