from flask import Flask, render_template, request, redirect, session
import pymysql
app = Flask(__name__)
app.secret_key="###FFF77_+)(**##55hjhjfjh"

@app.route('/borrowed/lib')
def borrowed():
    if 'key' in session:
        return redirect('/login/lib')
    else:
        return redirect('/borrowed/lib')


@app.route('/edit/lib')
def edit():
    if 'key' in session:
        return redirect('/login/lib')


@app.route('/home/lib')
def home():
    if 'keyadmin' in session:
        return render_template('home.html')

    else:
        return redirect('/index/lib')



con = pymysql.connect("localhost", "root", "", "hb_db")
@app.route('/index/lib', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cr = con.cursor()
        sql = "SELECT * FROM admin WHERE username = %s AND password = %s"
        data = (username, password)

        try:
            cr.execute(sql,data)
            rows = cr.fetchall()

            if cr.rowcount==0:
                return render_template('index.html', msg7="Not Found!")

            elif cr.rowcount==1:
               session['keyadmin'] = username;
               return redirect('/home/lib')


            else:
                return render_template('index.html', msg7="Something went wrong")

        except:
            con.rollback()
            return render_template('users.html', msg5="User Entry Error!")





    else:
       return render_template('index.html')



@app.route('/login/lib', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cr = con.cursor()
        sql = "SELECT * FROM new_admn WHERE email = %s AND password = %s"
        data = (email, password)

        try:
            cr.execute(sql,data)
            rows = cr.fetchall()

            if cr.rowcount==0:
                return render_template('login.html', msg7="Not Found!")

            elif cr.rowcount==1:
                session['key'] = email;
                return redirect("/user/lib")

            else:
                return render_template('login.html', msg7="Something went wrong")

        except:
            con.rollback()
            return render_template('login.html', msg5="User Entry Error!")

    else:
       return render_template('login.html')



@app.route('/admn_form', methods=['POST', 'GET'])
def admn_form():
    if 'keyadmin' in session:

        #INSERT INTO `Admin`(`f_name`, `l_name`, `email`, `password`) VALUES ('Martin', 'Muya', 'martinmuya@gmail.com', 'modcom1238')
        if request.method=='POST':
            username = request.form['username']
            password = request.form['password']
            rpt_password = request.form['rpt_password']

            if password != rpt_password:
                return render_template('admn_form.html', msg="Please Re-enter. Passwords do not match")

            elif len(password) < 8:
                return render_template('admn_form.html', msg1="Please re-enter password. Password must have more than 8 characters")

            elif username == 0:
                return render_template('admn_form.html', msg6="Please re-enter username")



            else:
                con =  pymysql.connect("localhost", "root", "", "hb_db")
                # create a cursor to execute your sql
                cr = con.cursor()
                sql = "INSERT INTO `admin`(`username`, `password`) VALUES (%s,%s)"

                data = (username, password)

                try:
                    cr.execute(sql,data)
                    con.commit()
                    return render_template('admn_form.html', msg5="Thank you for Registering!")

                except:
                    con.rollback()
                    return render_template('admn_form.html', msg5="Failed to Register!")
        else:
            return render_template('admn_form.html')

    else:
        return redirect('/index/lib')


@app.route('/log/lib')
def log():
    if 'key' in session:
        return redirect('/login/lib')

@app.route('/profile/lib')
def profile():
    if 'key' in session:

        email = session['key']
        cr = con.cursor()
        sql = "SELECT * FROM new_admn WHERE email = %s"
        data = (email)
        try:

            cr.execute(sql, data)
            rows = cr.fetchall()

            if cr.rowcount == 0:
                return render_template('profile.html', msg6="Not Found")
            else:
                return render_template('profile.html', rows=rows)

        except:
            con.rollback()
            return render_template('profile.html', msg5="Error!")

    else:
        return redirect('/login/lib')


@app.route('/profileadm/lib')
def profileadm():
    if 'keyadmin' in session:

        username = session['keyadmin']
        cr = con.cursor()
        sql = "SELECT * FROM admin WHERE username = %s"
        data = (username)
        try:

            cr.execute(sql, data)
            rows = cr.fetchall()

            if cr.rowcount == 0:
                return render_template('profileadm.html', msg6="Not Found")
            else:
                return render_template('profileadm.html', rows=rows)

        except:
            con.rollback()
            return render_template('profileadm.html', msg5="Error!")

    else:
        return redirect('/index/lib')


@app.route('/add_user/lib', methods=['POST', 'GET'])
def add_user():
    if 'keyadmin' in session:

        # INSERT INTO `Admin`(`f_name`, `l_name`, `email`, `password`) VALUES ('Martin', 'Muya', 'martinmuya@gmail.com', 'modcom1238')
        if request.method == 'POST':
            f_name = request.form['f_name']
            l_name = request.form['l_name']
            email = request.form['email']
            password = request.form['password']
            rpt_password = request.form['rpt_password']
            role = request.form['role']


            if password != rpt_password:
                return render_template('admn_form.html', msg="Please Re-enter. Passwords do not match")

            elif len(password) < 8:
                return render_template('admn_form.html', msg1="Please re-enter password. Password must have more than 8 characters")

            elif len(f_name) == 0:
                return render_template('add_user.html', msg2="Please enter your First Name")

            elif len(l_name) == 0:
                return render_template('add_user.html', msg3="Please enter your Last Name")

            elif len(email) == 0:
                return render_template('add_user.html', msg4="Please enter your E-Mail")

            else:
                con = pymysql.connect("localhost", "root", "", "hb_db")
                # create a cursor to execute your sql
                cr = con.cursor()
                sql = "INSERT INTO `new_admn`(`f_name`, `l_name`, `email`, `password`, `role`) VALUES (%s,%s,%s,%s,%s)"

                data = (f_name, l_name, email, password, role)

                try:
                    cr.execute(sql, data)
                    con.commit()
                    return render_template('add_user.html', msg5="Thank you for Registering!")

                except:
                    con.rollback()
                    return render_template('add_user.html', msg5="Failed to Register!")
        else:
            return render_template('add_user.html')

    else:
        return redirect('/index/lib')


@app.route('/register', methods=['POST', 'GET'])
def register():
    #INSERT INTO `new_account_tbl`(`f_name`, `l_name`, `email`, `password`) VALUES ('Martin', 'Muya', 'martinmuya@gmail.com', 'modcom1238')
    if request.method=='POST':
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        email = request.form['email']
        password = request.form['password']
        rpt_password = request.form['rpt_password']

        if password != rpt_password:
            return render_template('register.html', msg="Please Re-enter. Passwords do not match")

        elif len(password) < 8:
            return render_template('register.html', msg1="Please re-enter password. Password must have more than 8 characters")

        elif len(f_name) == 0:
            return render_template('register.html', msg2="Please enter your First Name")

        elif len(l_name) == 0:
            return render_template('register.html', msg3="Please enter your Last Name")

        elif len(email) == 0:
            return render_template('register.html', msg4="Please enter yout E-Mail")

        else:

            con =  pymysql.connect("localhost", "root", "", "hb_db")
            # create a cursor to execute your sql
            cr = con.cursor()
            sql = "INSERT INTO `new_account_tbl`(`f_name`, `l_name`, `email`, `password`) VALUES (%s,%s,%s,%s)"

            data = (f_name,l_name,email,password)

            try:
                cr.execute(sql,data)
                con.commit()
                return render_template('register.html', msg5="Thank you for Registering!")

            except:
                con.rollback()
    else:
        return render_template('register.html')



@app.route('/add/lib', methods=['POST', 'GET'])
def add():
    if 'keyadmin' in session:
    #INSERT INTO `add_book_tbl`(`book_name`, `book_description`, `book_category`) VALUES('The Mic', 'Family drama', 'Novel')
        if request.method == 'POST':
            book_name = request.form['book_name']
            book_description = request.form['book_description']
            book_category = request.form['book_category']

            if len(book_name) == 0:
                return render_template('add.html', msg="You did not enter anything. Please enter valid book name.")

            elif len(book_description) == 0:
                return render_template('add.html', msg1="You did not enter anything. Please enter valid book description.")

            elif len(book_category) == 0:
                return render_template('add.html', msg2="Please enter valid book category.")

            else:
                con =  pymysql.connect("localhost", "root", "", "hb_db")
                cr = con.cursor()
                sql = "INSERT INTO `add_book_tbl`(`book_name`, `book_description`, `book_category`) VALUES (%s,%s,%s)"
                data = (book_name,book_description,book_category)
                try:
                    cr.execute(sql, data)
                    con.commit()
                    return render_template('add.html', msg5="Book added Successfully!")

                except:
                    con.rollback()
                    return render_template('add.html', msg5="Book Error!")

        else:
            return render_template('add.html')

    else:
        return redirect('/login/lib')



@app.route('/users/lib',methods=['POST', 'GET'])
def users():
    if 'keyadmin' in session:
        if request.method == 'POST':
            user_id = request.form['user_id']
            cr = con.cursor()
            sql = "SELECT * FROM borrower_tbl WHERE user_id = %s"
            data = (user_id)

            try:
                cr.execute(sql,data)
                rows = cr.fetchall()

                if cr.rowcount==0:
                    return render_template('users.html', msg7="User Not Found!")
                else:
                    return render_template('users.html', rows=rows)

            except:
                con.rollback()
                return render_template('users.html', msg5="User Entry Error!")

            return render_template('users.html')

        else:
            sql= "SELECT * FROM borrower_tbl"
            cr = con.cursor()
            try:
                cr.execute(sql)
                rows = cr.fetchall()
                return render_template('users.html', rows=rows)
            except:
                con.rollback()
                return render_template('users.html', msg5="User Entry Error!")

    else:
        return redirect('/login/lib')


con = pymysql.connect("localhost", "root", "", "hb_db")
@app.route('/rent/lib',methods=['POST', 'GET'])
def rent():
    if 'key' in session:
        if request.method == 'POST':
            book_number = request.form['book_number']

            cr = con.cursor()
            sql = "SELECT * FROM add_book_tbl WHERE book_number = %s"
            data = (book_number)
            try:

                cr.execute(sql,data)
                rows = cr.fetchall()

                if cr.rowcount==0:
                    return render_template('rent.html', msg6="Book Not Found!")
                else:
                    return render_template('rent.html', rows=rows)

            except:
                con.rollback()
                return render_template('rent.html', msg5="Book Error!")

            return render_template('rent.html')
        else:
            sql = "SELECT * FROM add_book_tbl"
            cr = con.cursor()
            try:

                cr.execute(sql)
                rows = cr.fetchall()
                return render_template('rent.html', rows=rows)

            except:
                con.rollback()
                return render_template('rent.html', msg5="Book Error!")

    else:
        return redirect('/login/lib')


@app.route('/reset/lib')
def reset():
    return render_template('reset.html')


@app.route('/returns/lib')
def returns():
    return render_template('returns.html')

@app.route('/unreturned/lib')
def unreturned():
    return render_template('unreturned.html')


@app.route('/user/lib')
def user():
    if 'key' in session:
        return render_template('user.html')

    else:
        return redirect('/login/lib')


@app.route('/rent_book/lib/<book_number>')
def rent_book(book_number):
    return render_template('rent_book.html', book_number=book_number)


@app.route('/rentb', methods=['POST','GET'])
def rentb():
    if 'key' in session:
        if request.method == 'POST':
            user_id = request.form['user_id']
            book_number = request.form['book_number']

            if book_number == "":
                return render_template('rent_book.html', msg="You did not enter anything. Please enter valid book number.")

            elif user_id == "":

                return render_template('rent_book.html', msg1="You did not enter anything. Please enter valid user id.")

            else:


                con =  pymysql.connect("localhost", "root", "", "hb_db")
                cr = con.cursor()

                # first check if that user id is present
                cr.execute("SELECT * from borrower_tbl WHERE user_id=%s ", (user_id))

                if cr.rowcount < 1:
                    return render_template('rent_book.html', msg5="User does not Exist")

                else:

                    sql = "UPDATE add_book_tbl SET user_id = %s, status=%s WHERE book_number = %s"
                    data = (user_id, "Not Available", book_number)

                    try:
                        cr.execute(sql, data)
                        con.commit()
                        return render_template('rent_book.html', msg5="Book rented Successfully!")

                    except:
                        con.rollback()
                        return render_template('rent_book.html', msg5="Request Unsuccessfull!")

        else:
            return render_template('rent_book.html')
    else:
        return redirect('/login/lib')

@app.route('/return/<book_number>')
def returnbook(book_number):
    if 'key' in session:
            con =  pymysql.connect("localhost", "root", "", "hb_db")
            cr = con.cursor()

            # first check if that user id is present
            cr.execute("SELECT * from add_book_tbl WHERE book_number=%s ", (book_number))

            if cr.rowcount < 1:
                return render_template('rent_book.html', msg5="Book does not Exist")

            else:

                sql = "UPDATE add_book_tbl SET  user_id=%s,status=%s WHERE book_number = %s"
                data = ("NULL","Available", book_number)

                try:
                    cr.execute(sql, data)
                    con.commit()
                    return render_template('rent_book.html', msg5="Book returned Successfully!")

                except:
                    con.rollback()
                    return render_template('rent_book.html', msg5="Returned Unsuccessfull!")

    else:
        return redirect('/login/lib')


@app.route('/books/lib')
def books():
    if 'keyadmin'in session:
        con = pymysql.connect("localhost", "root", "", "hb_db")
        cr = con.cursor()
        sql = "SELECT * FROM add_book_tbl"

        try:
            cr.execute(sql)
            rows = cr.fetchall()
            return render_template('books.html', rows=rows)

        except:
            con.rollback()
            return render_template('books.html', msg5="Book Error!")

    else:
        return redirect('/login/lib')


@app.route('/view/lib')
def view():
    if 'key' in session:
        con = pymysql.connect("localhost", "root", "", "hb_db")
        cr = con.cursor()
        sql = "SELECT * FROM add_book_tbl"

        try:
            cr.execute(sql)
            rows = cr.fetchall()
            return render_template('view.html', rows=rows)

        except:
            con.rollback()
            return render_template('add.html', msg5="Book Error!")

        return render_template('view.html')
    else:
        return redirect('/login/lib')


@app.route('/logout')
def logout():
    session.pop("key")
    return redirect('/login/lib')



@app.route('/logoutadmin')
def logoutadmin():
    session.pop("keyadmin")
    return redirect('/index/lib')


if __name__ == '__main__':
    app.run()
    con = pymysql.connect("localhost", "root", "", "hb_db")
    cr = con.cursor()