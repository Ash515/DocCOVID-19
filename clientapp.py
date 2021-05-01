from flask import Flask, render_template,url_for,redirect,flash, request, redirect,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt
import re
app=Flask(__name__,template_folder='templates')

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='coviddetection'
mysql=MySQL(app)


@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/userlog',methods=["GET","POST"])
def userlogin():
    msg = ''
    if request.method == 'post':
        useremail = request.form['user_email']
        userpassword = request.form['user_psw']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM patients WHERE pemail = % s AND ppassword = % s', (useremail, userpassword, ))
        paccount = cursor.fetchone()
        if paccount:
            session['loggedin'] = True
            
            session['useremail'] = paccount['pemail']
            msg = 'Logged in successfully !'
            return render_template('main.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('userlog.html', msg = msg)

@app.route('/userreg',methods=["GET","POST"])
def userregistration():
    msg=''
    if request.method == 'POST':
        username = request.form['user_name']
        useremail = request.form['user_email']
        userpassword=request.form['user_psw']
        cursor = mysql.connection.cursor()
        exists=cursor.execute('''SELECT pemail FROM patients WHERE pemail = % s''', (useremail,))
        if exists:
            msg="Sorry mail id already exists ..."
        else:
            cursor.execute(''' INSERT INTO patients VALUES(%s,%s,%s)''',(username,useremail,userpassword))
            mysql.connection.commit()
            cursor.close()
            msg="Successfully registered !"
    return render_template('userreg.html',msg = msg)















  

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
    app.run(debug=True)
    app.secret_key = 'your secret key'
