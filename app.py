import os
import pymysql

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

ENDPOINT = os.environ.get('RDS_ENDPOINT')
USR = os.environ.get('RDS_USER')
PASSWORD = os.environ.get('RDS_PASSWORD')
REGION = "us-east-1"
DBNAME = os.environ.get('RDS_DB_NAME')

try:
    conn = pymysql.connect(user=USR, password=PASSWORD, host=ENDPOINT, autocommit=True)
    cur = conn.cursor()
    cur.execute("""USE todoApp""")
    print("Database connected")
except Exception as e:
    print("Database connection failed due to {}".format(e))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        try:
            sql = '''INSERT into todo (content) VALUES ('%s')''' % task_content
            cur.execute(sql)
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        try:
            sql = '''SELECT * from todo'''
            cur.execute(sql)
            tasks = cur.fetchall()
        except:
            return 'There was an issue rendering all data'
        for task in tasks:
            print(task)
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    try:
        sql = '''DELETE from todo WHERE id=('%i')''' % id
        cur.execute(sql)
        return redirect('/')
    except:
        return 'There was a problem deleting the task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        new_content = request.form['content']
        try:
            sql = '''UPDATE todo SET content=('%s') WHERE id=('%i')''' % (new_content, id)
            cur.execute(sql)
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        try:
            sql = '''SELECT * from todo WHERE id=('%i')''' % id
            cur.execute(sql)
            selected_task = cur.fetchall()
            print(selected_task)
        except:
            return 'There was an issue fetching the selected task'
        return render_template('update.html', selected_task=selected_task[0])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
