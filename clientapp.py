from MySQLdb import connections
from flask import Flask, render_template,url_for,redirect,flash, request, redirect,session
from flask.wrappers import Response
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
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctors')
        # Fetch one record and return result
        hospdata= cursor.fetchall()
        return render_template('main.html', useremail=session['user_email'],hospdata=hospdata)
    # User is not loggedin redirect to login page
     return redirect(url_for('userlogin'))

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

@app.route('/userprofile',methods=['GET','POST'])
def userprofile():

    if request.method == 'POST':
        profilename=request.form['pro_name']
        profileemail=request.form['pro_email']
        profileage=request.form['pro_age']
        profiledob=request.form['pro_dob']
        profilegender=request.form['pro_gender']
        profilebg=request.form['pro_bg']
        profilepno=request.form['pro_pnumber']
        profileaddr=request.form['pro_address']
        Chestpain=request.form['chest_pain']
        Breathe=request.form['breathe']
        Fatigue=request.form['fatigue']
        Fever=request.form['fever']
        Lowappetite=request.form['low_appetite']
        Musclepain=request.form['muscle_pain']
        profiledate=request.form['pro_date']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO profiles VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (profilename, profileemail, profileage,profiledob,profilegender,profilebg,profilepno,profileaddr,Chestpain,Breathe,Fatigue,Fever,Lowappetite,Musclepain,profiledate))
        mysql.connection.commit()
        return redirect(url_for('main'))
    else:
        return render_template('profile.html')

'''
@app.route('/usernotification')
def usernotifications():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM results')
    resdata = cursor.fetchall() #data from database
    return render_template("usernotification.html", resdata=resdata)

   

@app.route('/message:<id>')
def message(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM results WHERE rmail=%s',(id,))
    docdata = cursor.fetchall() #data from database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM patients')
    patdata = cursor.fetchall()
 

    
    return render_template("message.html",patdata=patdata,docdata=docdata)
'''

'''
@app.route('/usernotification')
def usernotification():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM results WHERE rmail= ')
    docdata = cursor.fetchall() #data from database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM patients')
    patientsdata = cursor.fetchall() #data from database

    return render_template("usernotification.html", patientsdata= patientsdata, docdata= docdata )

@app.route('/message')
def message():
    return render_template('message.html')
'''
@app.route('/usernotification')
def usernotification():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM results')
    docdata = cursor.fetchall() #data from database
    return render_template("usernotification.html",  docdata= docdata )


 










@app.route('/docmain')
def docmain():
    if 'docloggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM profiles')
        # Fetch one record and return result
        patientnotify= cursor.fetchall()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM doctors')
        doctorlog=cur.fetchall()
        return render_template('docmain.html', docemail=session['doc_email'],patientnotify=patientnotify,doctorlog=doctorlog)
    # User is not loggedin redirect to login page
    return redirect(url_for('doclogin'))

@app.route('/doclog',methods=['POST','GET']) 
def doclog():
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    message=""
    if request.method == 'POST' and 'doc_email' in request.form and 'doc_psw' in request.form:
        # Create variables for easy access
        docemail = request.form['doc_email']
        docpassword = request.form['doc_psw']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctors WHERE dmail = %s AND dpassword = %s', (docemail, docpassword))
        # Fetch one record and return result
        doctor= cursor.fetchone()
                # If account exists in patients table in out database
        if doctor:
            # Create session data, we can access this data in other routes
            session['docloggedin'] = True
            session['doc_psw'] = doctor['dpassword']
            session['doc_email'] = doctor['dmail']
            # Redirect to home page
            return redirect(url_for('docmain'))
        else:
            # Account doesnt exist or username/password incorrect
            message = 'Incorrect username/password!'
    return render_template('doclog.html', message='')

@app.route('/docreg',methods=["GET","POST"])
def doctorregistration():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'doc_uname' in request.form and 'doc_email' in request.form and 'hosp_name' in request.form  and 'doc_psw' in request.form and 'doc_conpsw' in request.form:
        # Create variables for easy access
        docname = request.form['doc_uname']
        docemail = request.form['doc_email']
        dochospital= request.form['hosp_name']
        dochospitaladdress= request.form['hosp_addr']
        dochospitalweb= request.form['hosp_web']
        docpassword = request.form['doc_psw']
        docconpassword = request.form['doc_conpsw']
     
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctors WHERE dhospital = %s', (dochospital,))
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
        elif not docname or not docpassword or not docemail or not dochospital:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO doctors VALUES (%s, %s, %s,%s,%s,%s)', (docname, docemail,dochospital,dochospitalweb,dochospitaladdress, docpassword))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            #after successfully inserted redirect to loginpage
            return render_template('doclog.html')  
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('docreg.html', msg=msg)

@app.route('/doctorlogout', methods = ['GET'])
def doctorlogout():
    session.pop('doc_email')
    return redirect(url_for('index'))

@app.route('/notifications/<id>')
def notifications(id):
  
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM profiles WHERE email= %s',(id,))
    profiledata = cursor.fetchall() #data from database
    
    return render_template("notifications.html", profiledata=profiledata)

@app.route('/results',methods=['POST'])
def results():
    if request.method=='POST':
        resultimage=request.form['res_file']
        doctorresult=request.form['doc_res']
        mlresult=request.form['ml_res']
        resultmail=request.form['res_mail']
        fresult=request.form['f_res']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO results VALUES (%s,%s,%s,%s,%s)',(resultmail,resultimage,doctorresult,mlresult,fresult))
        mysql.connection.commit()
    return redirect(url_for('docmain'))
    



if __name__=='__main__':
    app.debug = True
    app.run()
