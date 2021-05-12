import sqlite3

CREATE_TABLE_TASKS='''IF NOT EXISTS CREATE TABLE tasks( 
    ID INTEGER PRIMARY KEY  AUTOINCREMENT NOT NULL,
    NAME TEXT NOT NULL,
    DESC TEXT,
    TIM TEXT NOT NULL,
    DDMMYYYY TEXT NOT NULL);'''
CREATE_TABLE_FINISHEDTASKS='''IF NOT EXISTS CREATE TABLE finished_tasks( 
    ID INTEGER PRIMARY KEY  AUTOINCREMENT NOT NULL,
    NAME TEXT NOT NULL,
    DESC TEXT,
    TIM TEXT NOT NULL,
    DDMMYYYY TEXT NOT NULL);'''
ADD_TASK='''INSERT INTO tasks (NAME,DESC,TIM,DDMMYYYY) VALUES (?,?,?,?);'''
ADD_TASK_FINISHED='''INSERT INTO finished_tasks (NAME,DESC,TIM,DDMMYYYY) VALUES (?,?,?,?);'''
GET_TASK='''SELECT NAME,DESC,TIM,DDMMYYYY FROM tasks WHERE NAME = (?)'''
GET_TASK_ALL='''SELECT NAME,DESC,TIM,DDMMYYYY FROM tasks'''
DELETE_TASK='''DELETE FROM tasks WHERE NAME=(?)'''
EXTEND_DATE='''UPDATE tasks SET TIM=(?),DDMMYYYY=(?) WHERE NAME=(?) '''

def connect(database):
    return sqlite3.connect(database)

def create_tables(connection):
    with connection:
        cur = connection.cursor()
        cur.execute(CREATE_TABLE_TASKS)
        cur.execute(CREATE_TABLE_FINISHEDTASKS)

def add_task(connection,task):
    with connection:
        cur = connection.cursor()
        cur.execute(ADD_TASK,task.db_render())

def get_task_one(connection,name):
    with connection:
        try:
            cur = connection.cursor()
            cur.execute(GET_TASK,(name,))
            return cur.fetchone()
        except sqlite3.Error :
            return None

def get_task_all(connection):
    with connection:
        cur = connection.cursor()
        cur.execute(GET_TASK_ALL)
        return list(cur.fetchall())
def delete_task(connection,task):
    with connection:
        cur=connection.cursor()
        cur.execute(DELETE_TASK,(task.name,))

def add_to_done(connection,task):
    with connection:
        cur = connection.cursor()
        cur.execute(ADD_TASK_FINISHED,task.db_render())

def extend_date(connection,task,newdate):
    with connection:
        cur=connection.cursor()
        cur.execute(EXTEND_DATE,(newdate[0],newdate[1],task.name))


