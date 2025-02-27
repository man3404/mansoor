from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection, create_table

app = Flask(__name__)

# إنشاء الجدول عند تشغيل التطبيق
create_table()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Mass")
    apartments = cursor.fetchall()
    conn.close()
    return render_template("index.html", apartments=apartments)

@app.route('/add', methods=['POST'])
def add_apartment():
    apartment_number = request.form['apartment_number']
    apartment_type = request.form['apartment_type']
    building_name = request.form['building_name']
    tenant_name = request.form['tenant_name']
    rent_amount = request.form['rent_amount']
    rent_type = request.form['rent_type']
    rent_date = request.form['rent_date']
    payment_date = request.form['payment_date']
    phone_number = request.form['phone_number']
    notes = request.form['notes']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Mass (apartment_number, apartment_type, building_name, tenant_name, rent_amount, rent_type, rent_date, payment_date, phone_number, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (apartment_number, apartment_type, building_name, tenant_name, rent_amount, rent_type, rent_date, payment_date, phone_number, notes))
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:apartment_id>')
def delete_apartment(apartment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Mass WHERE id = ?", (apartment_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:apartment_id>')
def edit_apartment(apartment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Mass WHERE id = ?", (apartment_id,))
    apartment = cursor.fetchone()
    conn.close()
    return render_template("edit.html", apartment=apartment)
@app.route('/update/<int:apartment_id>', methods=['POST'])
def update_apartment(apartment_id):
    apartment_number = request.form['apartment_number']
    apartment_type = request.form['apartment_type']
    building_name = request.form['building_name']
    tenant_name = request.form['tenant_name']
    rent_amount = request.form['rent_amount']
    rent_type = request.form['rent_type']
    rent_date = request.form['rent_date']
    payment_date = request.form['payment_date']
    phone_number = request.form['phone_number']
    notes = request.form['notes']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Mass SET apartment_number=?, apartment_type=?, building_name=?, tenant_name=?, rent_amount=?, rent_type=?, rent_date=?, payment_date=?, phone_number=?, notes=?
        WHERE id=?
    ''', (apartment_number, apartment_type, building_name, tenant_name, rent_amount, rent_type, rent_date, payment_date, phone_number, notes, apartment_id))
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)