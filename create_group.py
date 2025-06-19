#group membership and group table

from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/create_group', methods=['GET','POST'])
def create_group():
    if not session.get('user_is_logged_in'):
        return redirect('/login')
    return render_template('create_group.html')

@app.route('/group_detail', methods=['GET','POST'])
def group_detail():
    user = session['username']
    GroupName = request.form['GroupName']
    description=request.form['description']

    cursor = conn.cursor();
    query_1 = 'INSERT INTO FlaskDemo.Group (gName, gCreator, gDesc) values (%s, %s, %s) '
    cursor.execute(query_1, (GroupName, user, description))
    conn.commit()
    
    query_2= 'INSERT INTO FlaskDemo.GroupMembership (memberName, gName, gCreator) values (%s, %s, %s) '
    cursor.execute(query_2, (user, GroupName, user))
    conn.commit()
    cursor.close()

    return redirect('/dashboard')