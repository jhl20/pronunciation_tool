# import sqlite3
#
# class Database:
#     def __init__(self, db):
#         self.conn = sqlite3.connect(db)
#         self.c = self.conn.cursor()
#         self.c.execute("CREATE TABLE IF NOT EXISTS terms (filename TEXT PRIMARY KEY, name TEXT, category TEXT)")
#         self.conn.commit()
#
#     def fetch(self, name=''):
#         self.c.execute("SELECT * FROM terms WHERE name LIKE ?", ('%'+name+'%',))
#         rows = self.c.fetchall()
#         return rows
#
#     def fetch2(self, query):
#         self.c.execute(query)
#         rows = self.c.fetchall()
#         return rows
#
#     def insert(self, filename, name, category):
#         self.c.execute("INSERT INTO terms VALUES (NULL, ?, ?, ?, ?)",(filename, name, category))
#         self.conn.commit()
#
#     def remove(self, id):
#         self.c.execute("DELETE FROM terms WHERE id=?", (id,))
#         self.conn.commit()
#
#     def update(self, id, name, category):
#         self.c.execute("UPDATE terms SET name = ?, category = ? WHERE id = ?",(name, category, id))
#         self.conn.commit()
#
#     def __del__(self):
#         self.conn.close()
