import sqlite3

table_dict={
    'tasks':'''CREATE TABLE tasks( 
            ID INTEGER PRIMARY KEY  AUTOINCREMENT NOT NULL,
            NAME TEXT NOT NULL,
            DESC TEXT,
            TIM TEXT NOT NULL,
            DDMMYYYY TEXT NOT NULL);''',
    'finished_tasks':'''CREATE TABLE finished_tasks( 
                        ID INTEGER PRIMARY KEY  AUTOINCREMENT NOT NULL,
                        NAME TEXT NOT NULL,
                        DESC TEXT,
                        TIM TEXT NOT NULL,
                        DDMMYYYY TEXT NOT NULL,
                        Finished_On TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);'''
}

ADD_TASK='''INSERT INTO tasks (NAME,DESC,TIM,DDMMYYYY) VALUES (?,?,?,?);'''
ADD_TASK_FINISHED='''INSERT INTO finished_tasks (NAME,DESC,TIM,DDMMYYYY) VALUES (?,?,?,?);'''
GET_TASK='''SELECT NAME,DESC,TIM,DDMMYYYY FROM tasks WHERE NAME = (?)'''
GET_TASK_ALL='''SELECT NAME,DESC,TIM,DDMMYYYY FROM tasks'''
DELETE_TASK='''DELETE FROM tasks WHERE NAME=(?)''' #under development
EXTEND_DATE='''UPDATE tasks SET TIM=(?),DDMMYYYY=(?) WHERE NAME=(?) '''
GET_DONE_TASKS='''SELECT * FROM finished_tasks'''

def create_tables(database):
    with sqlite3.connect(database) as connection:
        cur=connection.cursor()
        tablelists=cur.execute('SELECT name FROM sqlite_master WHERE type = \'table\'').fetchall()
        for tablename in table_dict:
            if (tablename,) not in tablelists:
                cur.execute(table_dict[tablename])

def add_task(database,task):
    with sqlite3.connect(database) as connection:
        cur = connection.cursor()
        cur.execute(ADD_TASK,task.db_render())

def get_task_one(database,name):
    with sqlite3.connect(database) as connection:
        try:
            cur = connection.cursor()
            cur.execute(GET_TASK,(name,))
            return cur.fetchone()
        except sqlite3.Error :
            return None

def get_task_all(database):
    with sqlite3.connect(database) as connection:
        cur = connection.cursor()
        cur.execute(GET_TASK_ALL)
        return list(cur.fetchall())

def get_done_tasks(database):
    with sqlite3.connect(database) as connection:
        cur = connection.cursor()
        cur.execute(GET_DONE_TASKS)
        return list(cur.fetchall())

def delete_task(database,task):
    with sqlite3.connect(database) as connection:
        cur=connection.cursor()
        cur.execute(DELETE_TASK,(task.name,))

def add_to_done(database,task):
    with sqlite3.connect(database) as connection:
        cur = connection.cursor()
        cur.execute(ADD_TASK_FINISHED,task.db_render())

def extend_date(database,task,newdate):
    with sqlite3.connect(database) as connection:
        cur=connection.cursor()
        cur.execute(EXTEND_DATE,(newdate[0],newdate[1],task.name))