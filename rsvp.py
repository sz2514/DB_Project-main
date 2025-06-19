from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/event_rsvp/', methods=['GET','POST'])
def event_rsvp():
    if not session.get('user_is_logged_in'):
        return redirect('/login')
    user = session['username']
    gName = request.args.get('gName')
    gCreator = request.args.get('gCreator')

    cursor = conn.cursor();
    ## list the events 'user' has not joined
    query = 'select eid from Event where gName = %s and gCreator = %s and eid not IN(select eid from RSVP where userName = %s)' 

    cursor.execute(query,(gName, gCreator, user))
    result = cursor.fetchall()
    print('---------------------------------')
    print(result)
    cursor.close()
    return render_template("event_rsvp.html",result=result)

@app.route('/rsvp/', methods=['GET','POST'])
def rsvp():
    user = session['username']
    eventID=request.args.get('eid')
    cursor = conn.cursor();
    query = 'INSERT INTO FlaskDemo.RSVP (username, eID, response) values (%s,%s,%s)' 
    cursor.execute(query,(user,eventID,'1'))
    conn.commit()
    cursor.close()
    return redirect('/dashboard')
