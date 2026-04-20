from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__) # This is needed to begin creating this Flask API with a database.  Here, we create an instance of Flask. Note: app is a variable.

DB_NAME = "budget_manager.db" # This is a constant (this is why it's in uppercase) This is the name of a database.  This is a constant variable. In Python, there's no const keyword. We create this const variable to avoid using the actual DB name because if we mistype the name, we will be unintentionally creating another database--that would be a major problem.


def init_db(): # This is a Python function that is used all the time with DB's (it is part of the "basic Flask API DB structure").  This function allows us to create a table in our DB.
    connection = sqlite3.connect(DB_NAME) # This is the way to open a connection to the D.B. named "budget_manager.db"  Connection is merely a variable.  Here, we are connecting the DB engine with our database.  
    cursor = connection.cursor() # Creates a curser/tool that lets you send SQL commands(SELECT, INSERT ...) to the D.B. Note: That here we are again creating a variable (it acts as a function with lots of logic behind the scenes). On the right side, cursor() is a method.  So, from the connection of the DB engine and the DB, we want to use a metho that lets you send requests to the DB.
# Question: In the code below, why is "users" used instead of DB_NAME? Bc there are two different names--a DB name and a table name. The DB is a file with the db extension.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users ( 
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT UNIQUE NOT NULL,
          password TEXT NOT NULL
        )
    """)
  # In the code directly above, the words in small text are the words than can change, depending on your particular DB (its name and its properties).  That is where SQL commands are inserted. Note: It can be written in one long line--but that's hard for us to read visually.  This is why we use triple double quotes--to write in shorter lines of code. Note: "IF NOT EXISTS" is a validation that is added here (but it's not absolutely necessary--it just helps us avoid a servious problem). 
    connection.commit() # Save changes to the D.B. This is also part of the basic structure of a Flask-DB API. This step is not needed when you are reading/selecting data.
    connection.close() # Close the connection to the D.B.  This is also part of the basic structure of a Flask-DB API. 
# Note: The following commented-out lines of code are an alternatve way of creating an endpoint, such as the one below it (only the first code line is different).
# @app.route('/api/health' , methods=["GET"])
# def health_check():
 #   return jsonify({
 #       "status": "ok"
  #  }), 200

@app.get('/api/health') # The only disadvantage of this syntax is that we cannot use multiple methods together--we can only use one method for each endpoint that uses this syntax. Note: The purpose of this endpoint is merely to check if the API is running correctly. 
def health_check():
    return jsonify({
        "status": "ok"
    }), 200

# ----- USERS  ENDPOINT-----This is where we add values/data to our DB table we already created, but is empty.
@app.post('/api/users')
def register():
    new_user = request.get_json() # The user is gonna send us update info/data through our ThunderClient (we will get it as an object in JSON format). How do we get it?  First we can create a variable to hold that data. The Flask method that we use to get the user data is request.get_json(), API (the back-end) is returning a response. The user is sending us a request in ThunderClient.
    print(new_user) # This displays in the cp terminal.
# The following seven lines of code have to do with adding values to our table properties (rows).
    username = new_user["username"] # This is how we get the values input from the user.  Then we store them in a variable.  Here, the individual values are separated from the object.
    password = new_user["password"]
# Now we will place that data in our DB table:
    connection = sqlite3.connect(DB_NAME) # Open a connection to the D.B. named "budget_manager.db"
    cursor = connection.cursor()  # Creates a curser/tool that lets you send SQL commands(SELECT, INSERT ...) to the D.B.
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password)) # Executes SQL Statement (username, password) refers to the table properties/columnNames.  The two question marks serve as placeholders. Then we pass that info as a python tuple. The last set of parentheses contains the two variables we created above.
    connection.commit() # Save changes to the D.B.
    connection.close() # Close the connection to the D.B.

    return jsonify({
        "success": True, 
        "message": "Data added successfully!"
    }), 201

if __name__ == "__main__": # This is the code needed to run this application/file. This code is always placed at the end of the file. This tells the API to only execute this file when we are in it, but not when we're in a different file or if and when we are importing this as a module.
    init_db() # Here we are executing the function to create the DB table.
    app.run(debug=True) # This helps us with Hot Reload, so we don't need to stop and rerun the terminal.