import sqlite3


class Db:

    def __init__(self, database):
        self.database_name = database
        self.conn = sqlite3.connect(self.database_name)

    def connect(self):
        self.conn = sqlite3.connect(self.database_name)

    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS Job (
        company char not null
        title char not null,
        categoty char not null,
        location char,
        description text ,
        salary int ,
        experience char ,
        major char,
        education char,
        other text
        );
        ''')
        self.conn.commit()

    def insert(self, title, desc, salary, experience):
        self.conn.execute("insert into Job values (?, ?, ?, ?)", (title, desc, salary, experience))
        self.conn.commit()

    def close(self):
        self.conn.close()
if __name__ == '__main__':
    db = Db('jobs.db')
    db.create_table()
    db.insert('engineer', 'happy', 85000, 'not bad')
    db.close()