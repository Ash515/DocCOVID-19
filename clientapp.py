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
















  

'''
@app.route('/doclog',methods=['POST','GET']) 
def doclog():
    if 'username' in session:
        return url_for('docmain')
    if (request.method=="POST"):
        docemail=request.form.get('doc_email')
        docpassword=request.form.get('doc_psw')
        docemail_found = docemail.find_one({"docemail": docemail})
        if docemail_found:
            docemail_val=docemail_found['doc_email']
            passwordcheck=docemail_found['doc_psw']

            if bcrypt.checkpw(docpassword.encode('utf-8'),passwordcheck):
                session["docemail"]=docemail_val
                return redirect(url_for('docmain'))
            else:
                if 'docemail' in session:
                    return redirect(url_for("docmain"))
                message='Wrong password'
                return render_template('doclog.html',message=message)
        else:
            message="email not found"
            return render_template('userlog.html', message=message)
    return render_template('doclog.html')

@app.route('/docreg',methods=["GET","POST"])
def docreg():
    if request.method == 'POST':
        docuname = doctors.find_one({'docuname' : request.form['doc_uname']})
        docemail = doctors.find_one({'docemail' : request.form['doc_email']})
        if docuname is None:
            hashpass = bcrypt.hashpw(request.form['doc_psw'].encode('utf-8'), bcrypt.gensalt())
            doctors.insert({'docuname' : request.form['doc_uname'], 'doc_password' : hashpass,'docemail':docemail})
            session['docuname'] = request.form['docuname']
            return render_template('doclog.html')
        return 'That username already exists!'

    return render_template('docreg.html')
'''
            





    



    


if __name__=='__main__':
   
   

   

    app.debug = True
    app.run()
