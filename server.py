from flask import Flask, jsonify, request, render_template
import sqlite3 # Note: This is imported here (it's not installed in our computer).  We could also install (and download) it to get more tools to work with, such as using our terminal to interact with our database (sqlite.org).  But here, we are using VS code to work with that database engine.

app = Flask(__name__) # This is needed to begin creating this Flask API with a database.  Here, we create an instance of Flask. Note: app is a variable.

DB_NAME = "budget_manager.db" # This is a constant (this is why it's in uppercase) This is the name of a database.  This is a constant variable. In Python, there's no const keyword. We create this const variable to avoid using the actual DB name because if we mistype the name, we will be unintentionally creating another database--that would be a major problem.


def init_db(): # This is a Python function that is used all the time with DB's (it is part of the "basic Flask API DB structure").  This function allows us to create a table in our DB. This is the only place in our code file where we can create new tables in the same database (all within the same function). But here we do not add or manipulate data in any way.
    connection = sqlite3.connect(DB_NAME) # This is the way to open a connection to the D.B. named "budget_manager.db"  Connection is merely a variable.  Here, we are connecting the DB engine with our database.  
    cursor = connection.cursor() # Creates a curser/tool that lets you send SQL commands(SELECT, INSERT ...) to the D.B. Note: That here we are again creating a variable (it acts as a function with lots of logic behind the scenes). On the right side, cursor() is a method.  So, from the connection of the DB engine and the DB, we want to use a metho that lets you send requests to the DB.
# Question: In the code below, why is "users" used instead of DB_NAME? Bc there are two different names--a DB name and a table name. The DB is a file with the db extension. Note: In this section is where all tables are created. In the code below, after naming our db table, we begin naming the columns/fields from left to right--each one on a separate code line inside the curly braces. Note: The triple double-quotes are used to indicate that we will be breaking up an entire code line into several (only for visual viewing purposes).
# With the table creation, as shown below, use the following structure: A) Each line of code pertains to each column label (field name). B) From left to right in each code line, first write the field_name (all in lowercase), then skip a space: second, wirte the data TYPE (all in uppercase letters), then skip a space; third, write any CONSTRAINTS (in all uppercase letters); fourth, if you're including the following constaints, add additional instructions: DEFAULT # or string, CHECK(condition). Also, note that in the last code line, FOREIGN KEY and REFERENCES are placed on the same line.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users ( 
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT UNIQUE NOT NULL,
          password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           title TEXT,
           description TEXT NOT NULL, 
           amount INTEGER NOT NULL,
           date TEXT NOT NULL,
           category TEXT NOT NULL,
           user_id INTEGER,
           FOREIGN KEY(user_id) REFERENCES users(id)
        )           
    """ )
  # In the code directly above, the words in small text are the words than can change, depending on your particular DB (its name and its properties).  That is where SQL commands are inserted. Note: It can be written in one long line--but that's hard for us to read visually.  This is why we use triple double quotes--to write in shorter lines of code. Note: "IF NOT EXISTS" is a validation that is added here (but it's not absolutely necessary--it just helps us avoid a servious problem). 
    connection.commit() # Save changes to the D.B. This is also part of the basic structure of a Flask-DB API. This step is not needed when you are reading/selecting/getting data.
    connection.close() # Close the connection to the D.B.  This is also part of the basic structure of a Flask-DB API. 
# Note: The following commented-out lines of code are an alternatve way of creating an endpoint, such as the one below it (only the first code line is different).
# @app.route('/api/health' , methods=["GET"])
# def health_check():
 #   return jsonify({
 #       "status": "ok"
  #  }), 200
# In th following code, we are merely checking to see if the server is up and running (and not down for some unrelated reason).
@app.get('/api/health') # The only disadvantage of this syntax is that we cannot use multiple methods together--we can only use one method for each endpoint that uses this syntax. Note: The purpose of this endpoint is merely to check if the API is running correctly. 
def health_check():
    return jsonify({
        "status": "ok"
    }), 200

# ----- USERS  ENDPOINT-----This is where we add values/data to our DB table we already created, but is empty.
@app.post('/api/users')
def register():
    new_user = request.get_json() # The user is gonna send us update info/data through our ThunderClient (we will get it as an object in JSON format). How do we get it?  First we can create a variable to hold that data. The Flask method that we use to get the user data is request.get_json(), API (the back-end) is returning a response. The user is sending us a request in ThunderClient. Request is a method from Flask, therefore we need to import it from Flask (at the top of our file). get_json() is a function that we're executing. This is the way to get info from the client.
    print(new_user) # This displays in the cp terminal (the info we get from the user is printed out here).
# The following seven lines of code have to do with adding values to our table properties (rows).
    username = new_user["username"] # This is how we get the values input from the user.  Then we store them in a variable.  Here, the individual values are separated from the object.
    password = new_user["password"]
# Now we will place that data in our DB table (here, we are opening the connection again):
    connection = sqlite3.connect(DB_NAME) # Open a connection to the D.B. named "budget_manager.db"
    cursor = connection.cursor()  # Creates a curser/tool that lets you send SQL commands(SELECT, INSERT ...) to the D.B.
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password)) # Executes SQL Statement (username, password) refers to the table properties/columnNames (not our variables); the order that we place them in the set of parentheses is important.  The two question marks serve as placeholders (used by Python & Flask framework). Then we pass that info as a python tuple  (passed by user iput); a python tuple is similar to a pyton list, but it is immutable and often used for heterogeneous data that function as a single record--such as a row in a database table. The last set of parentheses contains the two variables we created above.
    connection.commit() # Save changes to the D.B.
    connection.close() # Close the connection to the D.B.
# Now we are returning the following in JSON format.
    return jsonify({
        "success": True, 
        "message": "Data added successfully!"
    }), 201 # created (status code)'

 # GET http:/127.0.0.1:5000/api/users/# Note: Here, since this URL can be tailored/customized to any number/user we may choose, we therefore need a path parameter ('/api/table_name/<type:table_primary_key_name>').
@app.get('/api/users/<int:user_id>')
def get_user_by_id(user_id):
    #logic goes here:
    connection = sqlite3.connect(DB_NAME) # To work with the database, this is Step # 1.
    connection.row_factory = sqlite3.Row #  This code line is only needed when we are accessing/reading data (only); allows column's values to be retrieved by name, row=["username"], so this syntax helps us access and read info/data that we indicate. We have already been introduced to the syntax for accessing a value from a dictionary (where we use square brackets, double quotes, and then the property).  If we don't have this line, we are not going to be able to work with square brackets.  In that case, we would need to use parentheses, and then work with SQLite objects and tuples, and numbers (integers).  With only a few columns, it's fairly easy to remember them, but if you're dealing with a much larger number of columns, this method will become very difficult to manage.  Column names are much easier to recall, therefore this approach is better.
    cursor = connection.cursor() # This enables the cursor tool to send the various types of requests.
    cursor.execute("SELECT id, * FROM users WHERE id=?", (user_id,)) # users is our DB table name; id is our designated primary key (id--identifier); username is a column name (field name), if you want to select all the table columns, use * (which means all columns); if you want to select more than one column, you need to separate every column by a comma (username, password); since we have path parameters, we are using WHERE (a keyword) to specify the ID (WHERE id=?", (user_id,) ) from the id column the id= the one that we are getting from that path parameter (user_id is the path parameter). Note: When working with tuples, it's necessary to include a comma at the end when there is only one tuple element. Also note: In most cases, you want to return almost everything--except a password (for security reasons).
    row = cursor.fetchone() # Here, we are creating a variable called row to hold the value of one row.  Here, we are saying, once I have the value I want from the database, I need to unwrap the value (just like a box--we need to open it and take the value--that record). If you're getting a single value, you use "fetchone."  But if you're getting many values, then you use "fetchall."
    print(dict(row)) # After accessing that value, we can now print out the dictionary row. This will display all the values in the dictionary row (Python only uses dictionaries--not objects).
    user_information = dict(row) # Here we are creating a variable to hold/store our retrieved values.
    connection.close()
    # Next basic part of an endpoint:
    return jsonify({
        "success": True,
        "message": "User retrieved successfully!",
        "data": user_information # This will allow the table data we requested to be displayed in ThunderClient.  

    }), 200 #  OK 
# GET http://127.0.0.1:5000/api/users
@app.get('/api/users')
def get_users():
    # logic goes here:
    connection = sqlite3.connect(DB_NAME) # Here, we start/open our connection with our database.
    connection.row_factory = sqlite3.Row # Here, we use this code to make it easier for us to use column names instead of column integer numbers--this code is only needed for the GET request/query.
    cursor = connection.cursor() # Here, we activate the cursor tool that helps us make requests to the database.
    cursor.execute("SELECT id, username FROM users") # Here, we actually send SQL commands to the API, that connects to our database.
    rows = cursor.fetchall() # fetchall() is used when we are getting many values--many rows of values.
    print(rows) # Now we can display the values we got in our cp terminal.  However, rows is not easy to read.
    connection.close() # Now we close our connection to our database.

    users = [] # This block of code will make the retrieved data easier to read-- bc this is better formatting.
    for row in rows:
        print(dict(row))
        users.append(dict(row))

    # users = []
    #for row in rows:
    #   user = {
    #     "id": row["id"],
    #     "username": row["username"],
    #     "password": row["password"]
    #   }
    #   users.append(user)

    return jsonify({
        "success": True,
        "message": "Users retrieved successfully!",
        "data": users
    }), 200 # OK

# PUT -- Update a Single Record
# PUT http://127.0.0.1:5000/api/users/#
@app.put('/api/users/<int:user_id>')
def update_user(user_id):
    updated_user = request.get_json() # This line of code is used to get info/data from the client/user.
    username = updated_user["username"] # This is one of the two properties of data the client/user will submit. This is where the data requested is separated into individual properties (column names).
    password = updated_user["password"] # This is the other one of two properties of data the client/user will submit.
    # logic here:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    # validation code goes here (this is done as the last step--these lines of code up to "}), 404 # Not found" are inserted in between the code previously created.) It's a good idea to test this code without the validation first--makes troubleshooting easier:
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,)) # When you have one proptery, you need to use a comma at the end.
    row = cursor.fetchone() # fetchone() is used here bc we are getting one value.

    if not row: # If row is empty, do the following:
        connection.close()
        return jsonify({
            "success": False,
        "message": "User not found!"
        }), 404 #No Found
    # Otherwise, do the following:
    cursor.execute("UPDATE users SET username= ?, password=? WHERE id=?", (username, password, user_id)) # Here, we are only updating/modifying two properties (values of two column/field names). The username = ? means that the new username is whatever the user/client inputs; the new password is gonna be whatever the client/user inputs.  The last set of parentheses contains a Python tuple--last property of the tuple comes from the path parameter, the other two variables were defined in the previous codelines. The condition in this codeline is: WHERE id=?
    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "User updated successfully!"
    }), 200 # OK

# DELETE
# http://127.0.0.1:5000/api/users/#
@app.delete('/api/users/<int:user_id>')
def delete_user(user_id):
    # logic here
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    # validation code goes here (this is done as the last step--these lines of code up to "}), 404 # Not found" are inserted in between the code previously created.) It's a good idea to test this code without the validation first--makes troubleshooting easier:
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,)) # When you have one proptery, you need to use a comma at the end.
    row = cursor.fetchone() # fetchone() is used here bc we are getting one value.

    if not row: # If row is empty, do the following:
        connection.close()
        return jsonify({
            "success": False,
        "message": "User not found!"
        }), 404 #No Found
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "User deleted successfully!"

    }), 204 # No content left


# ----- EXPENSES ENDPOINT-----Here is where data is posted/created in its respective table.
# The first general step is to create the basic structure of an endpoint, which is the following: the decorator with the request method and the path parameter; the function name; the return statement, which is basic with only adjustments made for the type of request method.
# http://127.0.0.1:5000/api/expenses
@app.post('/api/expenses')
def create_expense():
    # Logic goes here (can be done/added last--fourth step):
    # if user does not send us data print("You need to fill out the entire form in order to submit it.")
    # otherwise, continue with the following steps:

    # This step is the second general step:
    new_expense = request.get_json() # Here, we get info from the user; we do it my using the request method from Flask (it is always connected to the get_json() method, which is used to transmit the data in JSON format.  Then we store that data in a variable we create/define here.
    print(new_expense) # Here, we display that input/data in our cp terminal. We can test the code here before adding more code to see that so far it works.  We do so by running it in the terminal and then with ThunderClient--do not include the FOREIGN KEY AND REFERENCES.  
    # Note: The following variables were created to avoid making the code long on line 93. 
    title = new_expense["title"]
    description = new_expense["description"]
    amount = new_expense["amount"]
    date = new_expense["date"]
    category = new_expense["category"]
    user_id = new_expense["user_id"]
    # Note: The following section of code of the endpoint is the third general step:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
       INSERT INTO expenses (title, description, amount, date, category, user_id)
       VALUES (?, ?, ?, ?, ?, ?)""", (title, description, amount, date, category, user_id) )  # Note: FOREIGN KEY and REFERENCES are not included here. Note: The comma needs to be placed after the triple-double quotes, or else the system will complain. The last pair of parentheses is where the tuple goes that was sent by the user (but here we are replacing those with the variables we assigned to them above).
    connection.commit() # Save changes to the D.B.
    connection.close() # Close the connection to the D.B.

# Note: The following section of code is almost the same for every endpoint created:
    return jsonify({
        "success": True,
        "message": "Expense created successfully!"
    }), 201

# GET ALL EXPENSES:
@app.get('/api/expenses')
def get_expenses():

    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, description, amount, date, category FROM expenses")
    rows = cursor.fetchall()
    print(rows)
    connection.close()

    return jsonify({
        "success": True,
        "message": "Expenses retrieved successfully!",
        "data": expenses
    }), 200 # OK

# GET a SINGLE EXPENSE BY ID:
# GET http://127.0.0.1:5000/api/expenses/#
@app.get('/api/expenses/<int:expense_id>')
def get_expense_by_id(expense_id):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, description, amount, date, category  FROM expenses WHERE id=?", (expense_id,))
    row = cursor.fetchone()
    if not row:
        connection.close()
        return jsonify({
            "success": False,
        "message": "Expense not found!"
        }), 404 # Not Found
    print(dict(row))
    expense_information = dict(row)
    connection.close()

    return jsonify({
        "success": True,
        "message": "Expense retrieved successfully!",
        "data": expense_information
    }), 200 # OK

# UPDATE AN EXISTING EXPENSE:
# PUT http://127.0.0.1:5000/api/expenses/#
@app.put('/api/expenses/<int:expense_id>')
def update_expense_by_id(expense_id):
    updated_expense = request.get_json()
    title = updated_expense["title"]
    description = updated_expense["description"]
    amount = updated_expense["amount"]
    date = updated_expense["date"]
    category = updated_expense["category"]
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id=?", (expense_id,))
    row = cursor.fetchone()
    
    if not row:
        connection.close()
        return jsonify({
            "success": False,
        "message": "Expense not found!"
        }), 404 #No Found
    
    if category != "Food" and category != "Education" and category != "Entertainment":
        connection.close()
        return jsonify({
            "success": False,
        "message": "Expense not found!"
        }), 404 #Not Found 
    cursor.execute("UPDATE expenses SET title=?, description=?, amount=?, date=?, category=? WHERE id=?", (title, description, amount, date, category, expense_id))
    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Update expense successfully!"
    }), 200 # OK

# DELETE A SPECIFIED EXPENSE:
# DELETE http://127.0.0.1:5000/api/expenses/#
@app.delete('/api/expenses/<int:expense_id>')
def delete_expense_by_id(expense_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id=?", (expense_id,))
    row = cursor.fetchone()
    if not row:
        connection.close()
        return jsonify({
            "success": False,
        "message": "Expense not found!"
        }), 404 #No Found
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    connection.commit()
    connection.close()

    return jsonify({
        "success": "True",
        "message": "Deleted expense successfully!"
    }), 204 # No Content

# ----- FRONTEND (with Flask & Jinga)-----Session 4 Project 111 (Here is when we add the following files (about, index--in the templates folder) in additon to the base.html file).
# We need to create endpoint (with the same prior five steps that are needed for the creation of an endpoint: the decorator, the method, the path, the function name, and the return statement).
# http://127.0.0.1:5000/home Note: Below, in order to get different URL endings to work (to render the same webpage), in the same endpoint, create different paths as shown below in the code:
@app.get('/') # We are including a decorator, method we use is GET, the path is a forward slash home. When the user is visiting slash home, we want to render HTML. Note: Later we remove the word "home." Perhaps we could open ThunderClient and insert this URL there--you could do that, but remember that front-end has to do with the browser. Therefore, we need to open this URL by entering it in our browser URL window because we want to see a website page. So in your browser window, just open a new tab and enter the following in the URL window: http://127.0.0.1z:5000/home  So now, we are rendering html (by only using Flask, Python, and Jinja).
@app.get('/index') 
@app.get('/home')
def home(): # The function name is home and it will return something: return ""
    # logic here
    my_name = "Snicker" # This shows how we can use logic to send data to an html file/page by using the code on this line and in the following line. Context refers to those variables we make available in the template. The context can be any data type. This will be in the second parameter in the render_template function below. Note: In the process of doing this, we are using essentially two different variables: the second one (referred to as the identifier) is used in the html file/page and in the second parameter of the render_template() function.
    return render_template("index.html", name= my_name)   # The function will return an "html file" Python work with indentation--not curly braces, so indentation is important. If we want to return/render html, we need to use a special function: render_template()  Then we need to insert as a parameter what we want to render (an html file).  Therefore, we also need to create an html file to add to our project. But first, we need to create a folder named templates in which that file will be placed. Jinja will be working with files inside of the templates folder all the time.  It is a common practice to name that folder: templates (but it could have a different name--but you need to use additional steps to do so). Here, you don't need to provide both parameters (two parameters).

# about.html should render <h1>about page</h1>

# @app.get("/about")
# def about():
#     message = "This is the about page."
#     return render_template("about.html", message= message) #"working on it"

# send to the specified html page, a dictionary with your name, cohort, and year.
@app.get('/about')
def about():
    # The data type we are sending now is a python dictionary:
    student_data= {
        "name": "Sergio",
        "cohort": 65,
        "year": 2026
    }
    return render_template("about.html", student_data=student_data)

@app.get('/contact')
def contact():

    contact_info= {
        "email": "contactpage123@flask.edu",
        "phone": "(999)222-3333",
        "mailing_address": "PO Box 555, Toledo Ohio, OH 55555"
    }
    # Note: To update this data, it's all done on this file and right here at this location.
    return render_template("contact.html",contact_info= contact_info ) # Note: To access a value of an attribute in a dictionary, you can either use square brackets or a period/dot in the templates html page.
if __name__ == "__main__": # This is the code needed to run this application/file. This code is always placed at the end of the file. This tells the API to only execute this file when we are in it, but not when we're in a different file or if and when we are importing this as a module. This essentially is a validation.
    init_db() # Here we are executing the function to create the DB table.
    app.run(debug=True) # This helps us with Hot Reload, so we don't need to stop and rerun the terminal.