from datetime import datetime,timedelta
import hashlib
import sqlite3


class duedate:
    #dynamically updated duedate class
    #no need of external updating
    #synced with local pc clock
    def __init__(self,tim,day,month=datetime.now().month,year=datetime.now().year):
        tim=tim.split(':')
        self.due=datetime(int(year),int(month),int(day),int(tim[0]),int(tim[1]))
    def remaining(self) ->str:
        return str(self.due-datetime.now()).split('.')[0] #usually for printing purpose
    def addtime(self,m=0,h=0,day=0):
        self.due+=timedelta(days=day,hours=h,minutes=m)
    def is_past(self):
        return (datetime.now()>self.due) #to delete a task

class task:
    def __init__(self,name,desc,due,imp=0):
        self.name=name
        self.desc=desc
        self.due_on : duedate =due #duedate object
        #imp 0-least, 1-imp, 2-,most imp
        if int(imp)<3:
            self.imp=int(imp)
        else:
            self.imp=2
        self.is_completed=False
    def status(self) ->(int,str):
        if self.is_completed:
            return 1,'Completed Successfully! Yeah you are on track.' 
        elif self.due_on.is_past():
            return 0,'Sorry, due date is past... Try to follow timetable'
        else:
            return 2,'Pending'
    def done(self):
        if not self.due_on.is_past(): self.__is_completed=True
        else: return 'Sorry due date is past'
    def __str__(self):
        curr=self.status()
        if curr[0]==1 or curr[0]==0:
            return curr[1]
        else:
            return f'{self.name},{curr[1]},due on-{str(self.due_on.due)},remaining-{self.due_on.remaining()}'
    def db_render(self):
        return (self.name,self.desc,f'{self.due_on.due.hour}:{self.due_on.due.minute}',f'{self.due_on.due.day}/{self.due_on.due.month}/{self.due_on.due.year}')

