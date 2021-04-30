from flask import Flask, render_template,url_for,redirect,flash, request, redirect,session
from  pymongo import MongoClient
import bcrypt
app=Flask(__name__,template_folder='templates')
client=MongoClient("mongodb://127.0.0.1:27017")
db=client.covid
patients=db.patients
doctors=db.doctors

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/userlog',methods=["GET","POST"])
def userlogin():
    message = 'Please login to your account'
    if "username" in session:
        return redirect(url_for("main"))
    if request.method == "POST":
        username= request.form.get("user_uname")
        password = request.form.get("user_psw")
        username_found = patients.find_one({"username": username})
        if username_found:
            username_val = username_found['username']
            passwordcheck = username_found['password']
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["username"] = username_val
                return redirect(url_for('main'))
            else:
                if "username" in session:
                    return redirect(url_for("main"))
                message = 'Wrong password'
                return render_template('userlog.html', message=message)
        else:
            message = 'Email not found'
            return render_template('userlog.html', message=message)
    return render_template('userlog.html', message=message)

@app.route('/userreg',methods=["GET","POST"])
def userregister():
    if request.method == 'POST':
        existing_user = patients.find_one({'username' : request.form['username']})
        email = patients.find_one({'email' : request.form['email']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['user_psw'].encode('utf-8'), bcrypt.gensalt())
            patients.insert({'username' : request.form['username'], 'password' : hashpass,'email':email})
            session['username'] = request.form['username']
            return render_template('userlog.html')
        return 'That username already exists!'

    return render_template('userreg.html')

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

            





    



    


if __name__=='__main__':
    app.run(debug=True)
