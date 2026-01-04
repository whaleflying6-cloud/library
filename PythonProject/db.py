import pymysql

def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='YT20050823qwe',
        database='library_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
