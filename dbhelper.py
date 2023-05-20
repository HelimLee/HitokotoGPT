import sqlite3
import random

class Database:
    def __init__(self, db_usable):
        self.conn = sqlite3.connect(db_usable)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY, usable BOOLEAN, reqres TEXT)")

    def log_request(self, usable, reqres):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO requests (usable, reqres) VALUES (?, ?)", (usable, reqres))
        self.conn.commit()

    def update_reqstat(self, systrack, usable):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE requests SET usable=? WHERE id=?", (usable, systrack))
        self.conn.commit()
    
    def random_usable(self):
        cursor = self.conn.cursor()
        # 从 requests 表中随机抽取一行 usable 值为 true 的数据
        cursor.execute("""(SELECT * FROM requests WHERE usable=true ORDER BY RANDOM() LIMIT 1)
                      UNION ALL
                      (SELECT * FROM requests ORDER BY RANDOM() LIMIT 1)
                      LIMIT 1""")# 获取查询结果
        result = cursor.fetchone()
        if result:
            return {"err":False,"result":result}
        else:
            return {"err":True,"result":"no reusable resource found"}
    def random_anything(self):
        cursor = self.conn.cursor()
        # 从 requests 表中随机抽取一行 usable 值为 true 的数据
        cursor.execute("SELECT * FROM requests ORDER BY RANDOM() LIMIT 1")
        # 获取查询结果
        result = cursor.fetchone()
        if result:
            return {"err":False,"result":result}
        else:
            return {"err":True,"result":"no avaliable resource found"}
    def close(self):
        self.conn.close()
