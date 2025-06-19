from app import app, conn
from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_bcrypt import Bcrypt



bcrypt = Bcrypt(app)
#Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')
#Logs user out
@app.route('/logoutAuth', methods=['GET', 'POST'])
def logoutAuth():
    session['user_is_logged_in'] = False
    return redirect("/")

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE userName = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    
    if(data and bcrypt.check_password_hash(data['password'],password)):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        session['user_is_logged_in'] = True
        return redirect("/dashboard")
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)


#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    fname = request.form['firstName']
    lname = request.form['lastName']
    email = request.form['emailAddress']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    # userName in the Person table
    query = 'SELECT * FROM Person WHERE email = %s'
    cursor.execute(query, (email))
    #stores the results in a variable
    # If this email address is already registered, then throw an error
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO Person (userName, password,fName, lName, email) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, hashed_password, fname, lname, email))
        conn.commit()
        cursor.close()
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')