import sqlite3

DB_NAME = 'bot_database.db'

def init_db():
    with sqlite3.connect(DB_NAME) as con:
        con.execute('''create table if not exists Users(
            Id integer primary key autoincrement, 
            UserId integer unique not null, 
            Name text not null, 
            Age integer not null, 
            CreatedAt datetime default CURRENT_TIMESTAMP
        )''')
        con.commit()

def save_user(user_id, name, age):
    with sqlite3.connect(DB_NAME) as con:
        con.execute(
            '''insert or replace into Users (UserId, Name, Age)
            values (?, ?, ?)''',
            (user_id, name, age)
        )
        con.commit()

def get_user_info(user_id):
    with sqlite3.connect(DB_NAME) as con:
        con.row_factory = sqlite3.Row
        cursor = con.execute(
            'select * from Users where UserId=?',
            (user_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

def is_user_exists(user_id):
    return get_user_info(user_id) is not None