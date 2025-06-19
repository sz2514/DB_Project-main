from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn



@app.route('/join_group')
def join_group():
    if not session.get('user_is_logged_in'):
        return redirect('/login')
    user = session['username']
    cursor = conn.cursor()
    query ='select gName from FlaskDemo.`Group`\
        where gName not in \
            (select gName from FlaskDemo.GroupMembership\
                where %s = memberName or %s = gCreator)'
    cursor.execute(query,(user,user))
    data = cursor.fetchall()
    return render_template('join_group.html', groups=data)

@app.route('/add_group',methods=['GET', 'POST'])
def add_group():
    gName = request.form['gName']
    user = session['username']
    
    cursor = conn.cursor()
    query = 'SELECT gName, gCreator FROM FlaskDemo.Group WHERE gName = %s and gCreator != %s'
    cursor.execute(query, (gName,user))
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    cursor.close()
    if not(data):
        #print('aaaaaaaaaaaaaaaaaa')
        #If the previous query returns data, then user exists
        error = "Sorry, you cannot join this group. Or chek if there is any typos in your inputs"
        return redirect('/join_group')
    else:
        cursor = conn.cursor()
        #print("eeeeeeeeeeeeeeeee")
        ins = 'INSERT INTO FlaskDemo.GroupMembership (memberName,gName,gCreator) VALUES (%s, %s, %s)'
        cursor.execute(ins, (user, data['gName'], data['gCreator']))
        conn.commit()
        cursor.close()
        return redirect('/dashboard')


    