from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/review/')
def review():
    # getting args from URL: https://stackoverflow.com/questions/40369016/using-request-args-in-flask-for-a-variable-url
    recipeID = request.args.get('recipeId')
    title = request.args.get('title')
    username = session.get('username')
    # when rendering this page, should display a list of existing reviews

    cursor = conn.cursor();
    query = 'SELECT * FROM Review NATURAL LEFT JOIN reviewPicture WHERE recipeID = %s'
    cursor.execute(query, (int(recipeID)))
    reviews = cursor.fetchall()

    query_2 = 'select * from Review where recipeID = %s and username = %s'
    cursor.execute(query_2, (int(recipeID), username))
    reviewed = cursor.fetchone()
    cursor.close()
    return render_template('review.html', recipeID=recipeID, title=title, reviews=reviews, reviewed=reviewed)

@app.route('/review_recipe', methods=['POST', 'GET'])
def review_recipe():
    user = session['username']
    recipeID = request.form['recipeID']
    rev_title = request.form['rev_title']
    stars = request.form['stars']
    rev_desc = request.form['rev_desc']
    img_url = request.form['review_img_url']

    cursor = conn.cursor();
    query = 'INSERT INTO Review (userName, recipeID, revTitle, revDesc, stars) \
            values (%s, %s, %s, %s, %s) '
    cursor.execute(query, (user, recipeID, rev_title, rev_desc, stars))
    insert_img_query = 'INSERT INTO ReviewPicture (userName, recipeID, pictureURL) values (%s, %s, %s)'

    cursor.execute(insert_img_query, (user, recipeID, img_url))
    conn.commit()
    cursor.close()
    return redirect(url_for('dashboard'))