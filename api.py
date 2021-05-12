from base import duedate,task
from database import create_tables,add_task,get_task_all,get_task_one,connect,delete_task,add_to_done

class todolist:
    def __init__(self):
        self.__salt=b'm\xffW \x98Ix011\n\xf0\x86\xb2\xdd\xb6\xd4jC j\xb5\xaa\xe2#"\x19\xbd\xe0\xc1\x9bf'
        self.__key=b'\x04V\x81\x17\x7fq\xc4FN\xaf\x08\x8c\x9e\xc9\xdc\xd5Se<\x1d\x89.\xf8\xde\x94\xa7+L\x14\xbc\xb3,'
        self.__database='tasksdata.db'
        
    def authenticate (self,pwdtocheck) -> bool: #tested once, result +ve
        key1=hashlib.pbkdf2_hmac('sha256',pwdtocheck.encode('utf-8'),self.__salt,10000)
        if key1==self.__key:
            return True
        else:
            return False
    
    def addtask(self,newtask : task ) ->None:
        add_task(connect(self.__database),newtask)
    
    def getone(self,name) ->task:
        res=get_task_one(connect(self.__database), name)
        if res!= None:
            res3=res[3].split('/')
            return task(res[0],res[1],duedate(res[2],*res3))
        else: return res
    
    def getall(self):
        res=get_task_all(connect(self.__database))
        for i in range(len(res)):
            t=res[i]
            t3=res[i][3].split('/')
            res[i]=task(t[0],t[1],duedate(t[2],*t3))
        return res

    def update(self):
        all_tasks=self.getall()
        for task in all_tasks:
            if task.due_on.is_past():
                delete_task(connect(self.__database), task)
                add_to_done(connect(self.__database), task)
                #task is closed
    def extend_task(self,task,extended_date):
        extended_date(connect(self.__database),task,extended_date)