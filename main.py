import pandas as pd
from flask import Flask,render_template,request
from fileinput import filename
import mysql.connector

app = Flask(__name__) 

@app.get('/')
def upload():
    return render_template('index.html')

def insert_into_database(id_list,name_list,dept_list,cgpa_list):
    my_db = mysql.connector.connect (
        host = "localhost",
        user = "root",
        password = "root@123",
        port = 3306,
        database = "myschema"
    )

    mycursor = my_db.cursor()

    sql = "INSERT INTO Student(id,name,dept,cgpa) VALUES (%s,%s,%s,%s)"
    val = combined_list = list(zip(id_list, name_list, dept_list, cgpa_list))

    mycursor.executemany(sql,val)
    my_db.commit()

def function_extract(dataframe):
    id_column = dataframe['id']
    id_list = id_column.tolist()
    name_column = dataframe['name']
    name_list = name_column.tolist()
    dept_column = dataframe['dept']
    dept_list = dept_column.tolist()
    cgpa_column = dataframe['cgpa']
    cgpa_list = cgpa_column.tolist()
    insert_into_database(id_list,name_list,dept_list,cgpa_list)


@app.post('/view')
def view():
    file = request.files['file']
    file.save(file.filename)
    data = pd.read_excel(file)
    function_extract(data)
    return "<h2>Data has been inserted into your DB successfully.<h2>"
    

if __name__ == '__main__':
    app.run(debug=1)
