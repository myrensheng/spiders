import datetime
import sqlite3
import time
from flask import Flask, render_template, jsonify
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
db = "./test.db"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/function1")
def function1():
    # 连接数据
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    insert_sql = """
    insert into test (timestamp,msg) values ('{0}','{1}')
    """
    # 清空数据
    delete_sql = """
    delete from test
    """
    cursor.execute(delete_sql)
    conn.commit()
    # 写入数据
    for i in range(5):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # msg = "".join(random.choices(string.ascii_lowercase, k=5))
        msg = str(i)
        cursor.execute(insert_sql.format(timestamp, msg))
        conn.commit()
        time.sleep(1)
    conn.close()
    return jsonify({"status": 200, "msg": "ok"})


@app.route("/function2")
def function2():
    # 读取数据
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    select_sql = """
    select * from test
    """
    result = cursor.execute(select_sql)
    msg_list = []
    for msg in result:
        msg_dict = {
            "timestamp": msg[0],
            "content": msg[1]
        }
        msg_list.append(msg_dict)
    conn.close()
    return jsonify({"status": 200, "msg": "ok", "activites": msg_list})


@app.route("/function3")
def function3():
    # 连接数据
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # 清空数据
    delete_sql = """
        delete from test
        """
    cursor.execute(delete_sql)
    conn.commit()
    conn.close()
    return jsonify({"status": 200, "msg": "ok"})


if __name__ == '__main__':
    app.run(debug=False)
