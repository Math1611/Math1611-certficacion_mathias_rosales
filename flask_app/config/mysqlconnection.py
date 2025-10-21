import pymysql.cursors

 
class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='4mtp',
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, data)
            if query.lower().strip().startswith("select"):
                return cursor.fetchall()
            if query.lower().strip().startswith(("insert", "update", "delete")):
                return cursor.lastrowid
        return None


def connectToMySQL(db):
    return MySQLConnection(db)


