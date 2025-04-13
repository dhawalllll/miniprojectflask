from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = "secret_key"

def get_db_connection():
    con = sqlite3.connect('society.db')
    con.row_factory = sqlite3.Row
    return con

@app.route('/')
def home():
    return render_template('base.html')
    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/add_entry', methods=['GET','POST'])
def add_entry():
    if request.method == 'POST':
        flat_no = request.form['flat_no']
        owner_name = request.form['owner_name']
        contact = request.form['contact']
        alt_contact = request.form['alt_contact']
        con = get_db_connection()
        cur = con.cursor()
        cur.execute('INSERT INTO flats (flat_no, owner_name, contact, alt_contact) VALUES (?,?,?,?)',(flat_no, owner_name, contact, alt_contact))
        con.commit()
        con.close()
        return redirect(url_for('dashboard'))
    return render_template('add_entry.html')


@app.route('/view_entries')
def view_entries():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute('SELECT * FROM flats')
    flats = cur.fetchall()
    con.commit()
    con.close()
    return render_template('view_entries.html', flats=flats)

@app.route('/add_maintenance', methods=['GET','POST'])
def add_maintenance():
    if request.method == 'POST':
        flat_no = request.form['flat_no']
        month = request.form['month']
        amount = request.form['amount']
        if flat_no and month and amount:
            con = get_db_connection()
            cur = con.cursor()
            cur.execute('INSERT INTO maintenance (flat_no, month, amount) VALUES (?,?,?)',(flat_no,month,amount))
            con.commit()
            con.close()
            flash('Maintenance added successfully!')
        else:
            flash('All fields are required.')
    return render_template('add_maintenance.html')



@app.route('/add_expense', methods=['GET','POST'])
def add_expense():
    if request.method == 'POST':
        month = request.form['month']
        description = request.form['description']
        amount = request.form['amount']
        con = get_db_connection()
        cur = con.cursor()
        cur.execute('INSERT INTO extra_expenses (month,description,amount) VALUES (?,?,?)',(month,description,amount))
        cur.commit()
        cur.close()
        return redirect(url_for('dashboard'))
    return render_template('add_expense.html')

@app.route('/search',methods=['GET','POST'])
def search():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM flats WHERE flat_no LIKE ? OR owner_name LIKE ?", ('%' + keyword + '%','%' + keyword + '%'))
        results = cur.fetchall()
        con.close()
    return render_template('search.html',results=results)


@app.route('/report', methods=['GET','POST'])
def report():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT month, SUM(amount) as total FROM maintenance GROUP BY month")
    monthly = cur.fetchall()
    con.execute("SELECT SUBSTR(month, -4) as year, SUM(amount) as total FROM maintenance GROUP BY year")
    yearly = cur.fetchall()
    con.close()
    return render_template('report.html',monthly=monthly, yearly=yearly)
    




if __name__ == '__main__':
    app.run(debug=True)


    