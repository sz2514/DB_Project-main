from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/post_recipe')
def post_recipe():
    return render_template('create_recipe.html')

@app.route('/create_recipe')
def create_recipe():
    if not session.get('user_is_logged_in'):
        return redirect('/login')
    username = session['username']
    # cursor = conn.cursor();
    # query = 'SELECT * FROM Recipe where postedBy = %s'
    # cursor.execute(query, username)
    # recipes = cursor.fetchall()
    # cursor.close()
    return render_template('create_recipe.html')

#Authenticates the register
@app.route('/createRecipe', methods=['GET', 'POST'])
def createRecipe():
    error = None
    username = session['username']
    title = request.form['title']
    numServings = request.form['numServings']
    # check if numServings is positive integer!!!!
    if numServings.isnumeric() == False:
        error = "Please input a positive integer for numServings section! "
        return render_template('create_recipe.html', error = error)
    if int(numServings) < 1:
        error = "Please input a positive integer for numServings section! "
        return render_template('create_recipe.html', error = error)

    numDietRestr = request.form['numDietaryRestrictions']
    recipeTags = request.form['recipeTags']
    numSteps = request.form['numSteps']
    step_detail_map = dict()
    for i in range(0, int(numSteps)):
        curr_desc = "step_desc" + str(i)
        step_detail_map[i] = [request.form[curr_desc]]

    restrictions_detail_map = dict()
    for i in range(0, int(numDietRestr)):
        curr_rst = "name_rst" + str(i);
        curr_desc = "desc_rst" + str(i);
        restrictions_detail_map[i] = [request.form[curr_rst], request.form[curr_desc]]

    allowed_unit_names = ['ml', 'fl oz', 'g', 'oz', 'mm', 'inch']
    numOfIng = request.form['numIngredients']
    ingr_detail_map = dict()
    flag_invalid_input = False
    for i in range(0, int(numOfIng)):
        # ingr_detail_map would have entries like:
        #   { 1 : ['strawberry', 'gram', 10 ],
        #     2 : ['banana', 'gram', 10 ], }
        curr_ing_name = "name_ing" + str(i);
        curr_unit_name = "unitName_ing" + str(i);
        curr_amount = "amount_ing" + str(i);
        curr_purchase_link = "purchase_link_ing" + str(i);
        ingr_detail_map[i] = [request.form[curr_ing_name], request.form[curr_unit_name], 
        request.form[curr_amount], request.form[curr_purchase_link]]
        
        if request.form[curr_unit_name] not in allowed_unit_names:
            flag_invalid_input = True
        # Check if Amount is a POSITIVE INTEGER
        if request.form[curr_amount].isnumeric() == False:
            flag_invalid_input = True
        else:
            if int(request.form[curr_amount]) < 1:
                flag_invalid_input = True

    if flag_invalid_input == True:
        error = "Please input a valid input in the Add Ingredients section! "
        return render_template('create_recipe.html', error = error)

    
    cursor = conn.cursor()
    query = 'SELECT * FROM Recipe WHERE title = %s'
    cursor.execute(query, (title))
    data = cursor.fetchone()

    if(data):
        # if recipe with same title exists in DB, stop them from creating the recipe.
        error = "This recipe already exists"
        return render_template('create_recipe.html', error = error)
    else:
        query = 'SELECT'
        ins = 'INSERT INTO Recipe (title, numServings, postedBy) VALUES (%s, %s, %s)'
        cursor.execute(ins, (title, int(numServings), username))
        conn.commit()
        currRecipeID = cursor.lastrowid #Fetch the most recently added ID
        
        ###### RecipeTag table ########
        # example input for recipe tags: "French, Italian, Dessert"
        splittedArr = recipeTags.split(",")
        for i in splittedArr:
            ins = 'INSERT INTO RecipeTag (recipeID, tagText) VALUES (%s, %s)'
            cursor.execute(ins, (currRecipeID, i))
            conn.commit()

        # check if any of these ingredients are already found in the Ingredient DB.
        for key, val in ingr_detail_map.items():
            # ingr_detail_map looks like: key is 0 and value is ['strawberry', 'Gram', '3']
            # For each ingredient:
            # 1. Insert a new entry into Ingredient table if not already in DB.
            ######### Ingredient Table #########
            query = 'SELECT * FROM Ingredient WHERE iName = %s'
            cursor.execute(query, (val[0]))
            data = cursor.fetchone()
            ingredientName = val[0]
            if not data:
                ins = 'INSERT INTO Ingredient (iName, purchaseLink) VALUES (%s, %s)'
                cursor.execute(ins, (ingredientName, val[3]))

            ######### Unit Table #########
            query = 'SELECT * FROM Unit WHERE unitName = %s'
            cursor.execute(query, (val[1]))
            data = cursor.fetchone()
            unitName = val[1]
            if not data:
                ins = 'INSERT INTO Unit (unitName) VALUES (%s)'
                cursor.execute(ins, (unitName))

            
            # 2. Add an entry into RecipeIngredient Table
            ######### RecipeIngredient Table #########
            ins = 'INSERT INTO RecipeIngredient (recipeID, iName, unitName, amount) VALUES (%s, %s, %s, %s)'
            cursor.execute(ins, (currRecipeID, ingredientName, val[1],int(val[2])))
            conn.commit()


        ###### Restrictions table ########
        for key, val in restrictions_detail_map.items():
            query = 'SELECT * FROM Ingredient WHERE iName = %s'
            cursor.execute(query, val[0])
            data = cursor.fetchone()
            if data:
                # Only add an entry to Restrictions table ONLY IF ingredient exists. 

                #Another restriction - check if duplicate PK exists, same name and same desc.
                query2 = 'SELECT * FROM Restrictions WHERE iName = %s and restrictionDesc = %s'
                cursor.execute(query2, (val[0], val[1]))
                data2 = cursor.fetchone()
                if not data2:
                    ins = 'INSERT INTO Restrictions (iName, restrictionDesc) VALUES (%s, %s)'
                    cursor.execute(ins, (val[0], val[1]))
                    conn.commit()

        ####### Step Table #########
        for key, val in step_detail_map.items():
            #  map = {0 : "Cut Chicken.", 1: "Bring the heat to medium", 2: "Put oil", }
            ins = 'INSERT INTO Step (stepNo, recipeID, sDesc) VALUES (%s, %s, %s)'
            cursor.execute(ins, (str(key), currRecipeID, val[0]))
            conn.commit()
        
        ### upload image URL ###
        img_url = request.form['recipe_img_url']
        insert_img_query = 'INSERT INTO RecipePicture (recipeID, pictureURL) values (%s, %s)'
        cursor.execute(insert_img_query, (currRecipeID, img_url))

        conn.commit()
        cursor.close()
        return redirect('/dashboard')

# def get_unit_conversions():
#     """
#         do a query to get all possible conversions
#         store them in the form of {source: ratio}
#     """
#     query


@app.route('/recipeInfo/')
def recipeInfo():
    if not session.get('user_is_logged_in'):
        return redirect('/login')
    rId = request.args.get('recipeId')
    unit_pref = session.get('unit_pref') ## could be "metric" or "imperial"
    metric_units = set(['ml', 'mm', 'g'])
    imperial_units = set(['fl oz', 'oz', 'inch'])
    unit_hashmap = {'metric': metric_units, 'imperial': imperial_units}


    cursor = conn.cursor()
    query = 'SELECT * FROM Recipe WHERE recipeID = %s'
    cursor.execute(query, (int(rId)))
    foundRecipe = cursor.fetchone()
    error = None
    
    if foundRecipe:
        ## all of the ingredients that this recipe uses
        query = 'SELECT * FROM RecipeIngredient where recipeID = %s'
        cursor.execute(query, rId)
        foundRecipeIng = cursor.fetchall()

        # for every recipeIngredient, search in Ingredient table and Restrictions table.
        listIngredients = []
        listRestrictions = []
        for i in range(len(foundRecipeIng)):
            ingred = foundRecipeIng[i]
            query = 'SELECT * FROM Ingredient where iName = %s'
            cursor.execute(query, ingred["iName"])
            foundIng = cursor.fetchone()
            listIngredients.append(foundIng)
            query = 'SELECT * FROM Restrictions where iName = %s'
            cursor.execute(query, ingred["iName"])
            foundRestr = cursor.fetchone()
            if foundRestr is not None:
                listRestrictions.append(foundRestr)
            
            #if not unit_hashmap[unit_pref]: continue
            if not session.get('unit_pref'): continue
            if ingred['unitName'] not in unit_hashmap[unit_pref]: ## if unitName does not match the pref of user
                query = 'SELECT destinationUnit, ratio FROM UnitConversion \
                        WHERE sourceUnit = %s'
                cursor.execute(query, ingred['unitName'])
                dest_ratio = cursor.fetchone()
                destinationUnit = dest_ratio.get('destinationUnit')
                ratio = dest_ratio.get('ratio')
                
                foundRecipeIng[i]['amount'] = round((float(foundRecipeIng[i]['amount']) * float(ratio)), 2) ## need to be converted to float to work in python
                foundRecipeIng[i]['unitName'] = destinationUnit
    

        # print(float(foundRecipeIng[0]['amount']))
        # foundRecipeIng[0]['amount'] = 20
        # print(float(foundRecipeIng[0]['amount']))
        # if unit_pref: ## if the user has set a unit preference

            
            

        query = 'SELECT * FROM RecipeTag where recipeID = %s'
        cursor.execute(query, rId)
        foundRecipeTags = cursor.fetchall()
        
        query = 'SELECT * FROM Step where recipeID = %s'
        cursor.execute(query, rId)
        foundSteps = cursor.fetchall()

        img_query = 'SELECT * FROM Recipe NATURAL LEFT JOIN recipePicture WHERE recipeID = %s'
        cursor.execute(img_query, rId)
        results = cursor.fetchone()
        recipe_img = results['pictureURL']
        print(recipe_img)

        cursor.close()
        return render_template('recipeInfo.html', recipe=foundRecipe, recipeIngred = foundRecipeIng,
        recipeTags = foundRecipeTags, listIngredients = listIngredients, listRestrictions = listRestrictions,
        steps=foundSteps, recipe_img=recipe_img)
    else:
        cursor.close()
        error = 'Invalid Recipe ID.'
        return render_template('dashboard.html', error=error)