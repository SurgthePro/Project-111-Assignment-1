from flask import Flask, jsonify, request
import sqlite3

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
    connection.commit() # Save changes to the D.B. This is also part of the basic structure of a Flask-DB API. This step is not needed when you are reading/selecting data.
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
    }), 201 # created (status code)

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

if __name__ == "__main__": # This is the code needed to run this application/file. This code is always placed at the end of the file. This tells the API to only execute this file when we are in it, but not when we're in a different file or if and when we are importing this as a module. This essentially is a validation.
    init_db() # Here we are executing the function to create the DB table.
    app.run(debug=True) # This helps us with Hot Reload, so we don't need to stop and rerun the terminal.