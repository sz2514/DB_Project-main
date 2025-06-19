from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

def creator_of_group():
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT gName FROM FlaskDemo.Group where gCreator = %s'
    cursor.execute(query, username)
    gName = cursor.fetchone()
    if gName: return gName['gName']


@app.route('/dashboard')
def dashboard():
    if not session.get('user_is_logged_in'):
        return redirect('/login')
    username = session['username']
    print(username)
    cursor = conn.cursor();
    query = 'SELECT * FROM Recipe where postedBy = %s'
    cursor.execute(query, username)
    recipes = cursor.fetchall()

    # query_detect_group = 'Select gName FROM  \
    #                      (Person JOIN GroupMembership where Person.userName = GroupMembership.memberName) as Merged \
    #                       WHERE %s = GroupMembership.memberName or %s = gCreator'

    query_detect_group = 'SELECT distinct gName, gCreator from \
                          GroupMembership \
                          WHERE %s = memberName or %s = gCreator'

    cursor.execute(query_detect_group, (username,username))
    group_name = cursor.fetchall()

    event_query = 'select * from rsvp natural join event where username=%s'
    cursor.execute(event_query, (username))
    my_events = cursor.fetchall()
    cursor.close()
   
    creator_of_gName = creator_of_group()
    # print(creator_of_gName)
    return render_template('dashboard.html', recipe_list=recipes, groups=group_name, creator_of_gName=creator_of_gName, my_events=my_events)


@app.route('/settings')
def settings():
    """
        will render a setting page that allows user to set their preference
    """
    if not session.get('user_is_logged_in'):
        return redirect('/login')
    return render_template('settings.html')

@app.route('/set_preferences', methods=['GET','POST'])
def set_preferences():
    unit = request.form['unit']
    session['unit_pref'] = unit ## either metric or imperial

    return redirect('/dashboard')


"""
    often seen units in recipes:
    https://en.wikibooks.org/wiki/Cookbook:Units_of_measurement#Volume
"""