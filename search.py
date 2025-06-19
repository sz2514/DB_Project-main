from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search_recipes', methods=["POST", "GET"])
def search_recipes():
    if not session.get('user_is_logged_in'):
        return redirect('/login')
    search_input = request.form['search_input']
    tag = request.form['tag']
    stars = request.form['stars']
    search_filter = request.form['filter']


    cursor = conn.cursor();
    if stars == "any":
        results = any_stars(search_input, tag, search_filter)
    else:
        results = stars_specified(search_input, tag, stars, search_filter)
    return render_template('search.html', results=results)




def any_stars(search_input, tag, search_filter):
    cursor = conn.cursor();
    if search_filter == 'alphabetical':
        query = "select distinct recipeID, title, IFNULL(avg(stars), 'N/A') as avg \
                from Recipe NATURAL JOIN RecipeTag natural left JOIN Review \
                WHERE title like %s and tagText like %s \
                group by recipeID, title \
                order by title"
    else:
        query = "select distinct recipeID, title, IFNULL(avg(stars), 'N/A') as avg \
                from Recipe NATURAL JOIN RecipeTag natural left JOIN Review \
                WHERE title like %s and tagText like %s \
                group by recipeID, title \
                order by avg"
    search_input = '%{}%'.format(search_input)
    tag = '%{}%'.format(tag)
    cursor.execute(query, (search_input, tag))       

    results = cursor.fetchall()
    cursor.close()
    return results

def stars_specified(search_input, tag, stars, search_filter):
    cursor = conn.cursor();
    if search_filter == 'alphabetical':
        query = 'select DISTINCT recipeID, title, postedBy, AVG(stars) as avg \
                from Recipe NATURAL JOIN RecipeTag NATURAL JOIN Review \
                WHERE title like %s and tagText like %s \
                group by recipeID, title, postedBy \
                having AVG(stars) >= %s \
                order by title'
    else:
        query = 'select DISTINCT recipeID, title, postedBy, AVG(stars) as avg \
                from Recipe NATURAL JOIN RecipeTag NATURAL JOIN Review \
                WHERE title like %s and tagText like %s \
                group by recipeID, title, postedBy \
                having AVG(stars) >= %s \
                order by avg'

    search_input = '%{}%'.format(search_input)
    tag = '%{}%'.format(tag)
    cursor.execute(query, (search_input, tag, stars))       

    results = cursor.fetchall()
    cursor.close()
    return results