# DB_Project
This is the repo for the final project of Database class

Steps to run the flask app:
1. Make sure you have python3 installed
2. cd into the `DB_Project` folder
3. Create a virtual environtment with python3 -m venv [your env name]
4. Acticate the virtual environment with `source [your env name]/bin/activate`
5. You can exit the virtual environtment with `deactivate`
6. Install the dependencies with `pip3 install -r requirements.txt`

Creating database connecting to our flask app:
1. Using mysqlWorkbench or any other application, create a database called `FlaskDemo`
2. copy the create table queries in `DB_Project/FlaskDemo.sql` folder and use them to create tables in `FlaskDemo`

Running the flask app:
- type the following commands one by one:
    `export FLASK_APP=init1.py`
    `export FLASK_ENV=development`
    `flask run`

Now the web app should be up and running at 127.0.0.1:5000

- need to be able to show images in create-recipe
- need to be able to incrementally add to to a recipe



