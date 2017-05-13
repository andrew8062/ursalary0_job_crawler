import sqlite3


class Db:

    def __init__(self, database):
        self.database_name = database
        self.conn = sqlite3.connect(self.database_name)

    def connect(self):
        self.conn = sqlite3.connect(self.database_name)

    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS Jobs (
        id INT NOT NULL PRIMARY KEY,
        company char not null,
        title char not null,
        categoty char not null,
        location char,
        salary int ,
        experience char ,
        education char,
        major char,
        hire time,
        description text 
        );
        ''')
        self.conn.commit()

        self.conn.execute('''CREATE TABLE IF NOT EXISTS Comments (
        id NOT NULL ,
        created_time DATETIME,
        comment text
        );
        ''')
        self.conn.commit()

    def insert_job(self, job_info):
        try:
            self.conn.execute("insert into Jobs values (?,?,?,?,?,?,?,?,?,?,?)",
                              job_info)
        except sqlite3.IntegrityError:
            print("{} {} is already exist".format(job_info[0], job_info[1]))
        except sqlite3.OperationalError:
            print("{} cause some problem".format(job_info))
            raise
        self.conn.commit()

    def insert_comment(self, comment):
        try:
            self.conn.executemany("insert into comments values (?,?,?)", comment)
        except sqlite3.OperationalError:
            print("{} cause some problem".format(comment))
            raise

        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    db = Db('jobs.db')
    db.create_table()
    db.insert_job(['1','普泉股份有限公司薪資', '技術員', '其它', '中部', '31000', '2 ~ 3年', '高中畢業', '', '2013-03', '\n                    \t年薪:\r\n上下班時間: \r\n年終: \r\n認股: \r\n獎金:\r\n工作內容: 負責廠內機台運作，上班12小時，輪休\r\n心得: 優點:三節獎金，年終\r\n          缺點:老闆脾氣古怪，逼走過不少的員工.....                    '])
    db.insert_comment([['305', '2017-05-12 21:39:51', ' 看起來真恐怖，果然要這網站吔，免得人家白做事。                    ']])
    db.close()