from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Rutas de la aplicación
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM obtain")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar todos los datos
@app.route('/kwok', methods=['POST'])
def addData():
    item = request.form['item']
    quantity = request.form['quantity']
    value = request.form['value']

    if item and quantity and value:
        cursor = db.database.cursor()
        sql = "INSERT INTO obtain (item, quantity, value) VALUES (%s, %s, %s)"
        data = (item, quantity, value)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM obtain WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    item = request.form['item']
    quantity = request.form['quantity']
    value = request.form['value']

    if item and quantity and value:
        cursor = db.database.cursor()
        sql = "UPDATE obtain SET item = %s, quantity = %s, value = %s WHERE id = %s"
        data = (item, quantity, value, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)