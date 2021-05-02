from flask import Flask, render_template,url_for,redirect,flash, request, redirect,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt
import re
app=Flask(__name__,template_folder='templates')

app.secret_key = "super secret key"
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='coviddetection'
mysql=MySQL(app)


@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/main')
def main():
     if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('main.html', useremail=session['user_email'])
    # User is not loggedin redirect to login page
     return redirect(url_for('userlogin'))

@app.route('/docmain')
def docmain():
    return render_template('docmain.html')

@app.route('/userlog',methods=["GET","POST"])
def userlogin():
    message = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'user_email' in request.form and 'user_psw' in request.form:
        # Create variables for easy access
        useremail = request.form['user_email']
        userpassword = request.form['user_psw']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM patients WHERE pemail = %s AND ppassword = %s', (useremail, userpassword))
        # Fetch one record and return result
        patient= cursor.fetchone()
                # If account exists in patients table in out database
        if patient:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['user_psw'] = patient['ppassword']
            session['user_email'] = patient['pemail']
            # Redirect to home page
            return redirect(url_for('main'))
        else:
            # Account doesnt exist or username/password incorrect
            message = 'Incorrect username/password!'
    return render_template('userlog.html', message='')
   
@app.route('/userreg',methods=["GET","POST"])
def userregistration():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'user_name' in request.form and 'user_email' in request.form and 'user_psw' in request.form:
        # Create variables for easy access
        username = request.form['user_name']
        useremail = request.form['user_email']
        userpassword = request.form['user_psw']
     
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM patients WHERE pemail = %s', (useremail,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', useremail):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not userpassword or not useremail:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO patients VALUES (%s, %s, %s)', (username, useremail, userpassword))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            #after successfully inserted redirect to loginpage
            return render_template('userlog.html')  
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('userreg.html', msg=msg)

@app.route('/userlogout', methods = ['GET'])
def userlogout():
    session.pop('user_email')
    return redirect(url_for('index'))
@app.route('/userforgot')
def userforgot():
    return render_template('userpassword.html')
















  


@app.route('/doclog',methods=['POST','GET']) 
def doclog():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'doc_email' in request.form and 'doc_psw' in request.form:
        # Create variables for easy access
        docemail = request.form['doc_email']
        docpassword = request.form['doc_psw']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctors WHERE demail = %s AND dpassword = %s', (docemail, docpassword))
        # Fetch one record and return result
        doctor= cursor.fetchone()
                # If account exists in patients table in out database
        if doctor:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['doc_psw'] = doctor['dpassword']
            session['doc_email'] = doctor['demail']
            # Redirect to home page
            return redirect(url_for('docmain'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('doclog.html', msg='')

@app.route('/docreg',methods=["GET","POST"])
def doctorregistration():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'doc_uname' in request.form and 'doc_email' in request.form and 'doc_psw' in request.form and 'doc_conpsw' in request.form:
        # Create variables for easy access
        docname = request.form['doc_uname']
        docemail = request.form['doc_email']
        docpassword = request.form['doc_psw']
        docconpassword = request.form['doc_conpsw']
     
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctors WHERE demail = %s', (docemail,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',docemail):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', docname):
            msg = 'Username must contain only characters and numbers!'
        elif docpassword!=docconpassword:
            msg="Password mismatch with confirm password"
        elif not docname or not docpassword or not docemail:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO doctors VALUES (%s, %s, %s)', (docname, docemail, docpassword))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            #after successfully inserted redirect to loginpage
            return render_template('doclog.html')  
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('docreg.html', msg=msg)

if __name__=='__main__':
    app.debug = True
    app.run()
