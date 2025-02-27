from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db_connection, create_table

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # استخدم مفتاحًا سريًا قويًا

USERNAME = "mansoor"
PASSWORDS = {
    "1234": "index",
    "5566": "top1"
}

# إنشاء الجدول عند تشغيل التطبيق
create_table()

@app.route('/')
def login():
    if 'logged_in' in session:
        return redirect(url_for(session.get('redirect_page', 'index')))  
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    
    if username == USERNAME and password in PASSWORDS:
        session['logged_in'] = True
        session['redirect_page'] = PASSWORDS[password]
        return redirect(url_for(session['redirect_page']))  
    else:
        return render_template('login.html', error="اسم المستخدم أو كلمة المرور غير صحيحة")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('redirect_page', None)
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))  

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Mass")
    apartments = cursor.fetchall()
    conn.close()
    return render_template("index.html", apartments=apartments)

@app.route('/top1')
def top1():
    if 'logged_in' not in session:
        return redirect(url_for('login'))  

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Mass")
    apartments = cursor.fetchall()
    conn.close()
    return render_template("top1.html", apartments=apartments)

@app.route('/add', methods=['POST'])
def add_apartment():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

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

    flash("تمت إضافة الشقة بنجاح!", "success")
    return redirect(url_for('index'))

@app.route('/delete/<int:apartment_id>')
def delete_apartment(apartment_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Mass WHERE id = ?", (apartment_id,))
    conn.commit()
    conn.close()

    flash("تم حذف الشقة بنجاح!", "danger")
    return redirect(url_for('index'))

@app.route('/edit/<int:apartment_id>')
def edit_apartment(apartment_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Mass WHERE id = ?", (apartment_id,))
    apartment = cursor.fetchone()
    conn.close()
    
    return render_template("edit.html", apartment=apartment)

@app.route('/update/<int:apartment_id>', methods=['POST'])
def update_apartment(apartment_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

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

    flash("تم تعديل بيانات الشقة بنجاح!", "success")
    return redirect(url_for('index'))

@app.route("/top1", methods=["GET", "POST"])
def search_by_phone():
    result = None
    message = ""

    if request.method == "POST":
        phone_number = request.form.get("phone_number", "").strip()

        if phone_number:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Mass WHERE phone_number = ?", (phone_number,))
            result = cursor.fetchone()
            conn.close()

            if not result:
                message = "لا يوجد ساكن مسجل بهذا الرقم."
        else:
            message = "يرجى إدخال رقم جوال للبحث."

    return render_template("top1.html", result=result, message=message)

if __name__ == '__main__':
    app.run(debug=True)