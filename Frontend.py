import tkinter as tk
import tkinter.messagebox as messagebox
from api import todolist
from base import task, duedate


def refresh_list():
    '''this is a fuction that refreshes the listbox'''
    
    Todo.update()
    Task_list.delete(0,tk.END)
    for task in Todo.getall():
        Task_list.insert(tk.END,str(task))

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey',**kwargs):
        super().__init__(master,kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.bind("<Button-1>", self.on_click)
        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
    def on_click(self,*args):
        self.delete(0, 'end')

def add_button_command():
    #this function controls adding of events
    taskname=TaskDesc.get()
    hm=HMData.get()
    date=DateData.get()
    if taskname=='enter task description' or hm=='HH:MM' or date=='DD/MM/YYYY':
        messagebox.showerror('Invalid or Incomplete Input','Please enter Correct input according to format')
        return 
    date=list(date.split('/'))
    Todo.addtask(task(taskname, '', duedate(hm,date[0],date[1],date[2])))
    refresh_list()

def del_button_command():
    #print(Task_list.get(tk.ACTIVE))
    s=str(Task_list.get(tk.ACTIVE)).split(',')[0]
    confirm=messagebox.askquestion(f'Delete {s}',f'Are you sure you want to delete {s}')
    if confirm=='yes':
        Todo.delete(s)
        refresh_list()




def Cmp_button_command():
    print("command for displaying comppleted task button")



def setscreen(root):
    width=600
    height=500
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=False, height=False)
    try:
        icon=tk.PhotoImage(file='icon.png')
        root.iconphoto(False,icon)
    except:
        pass
    root.title('TO-DO List')

def setlabels(root):
    head_label=tk.Label(root,text='Task Assistant',font=('Ariel',18),bg='#cffefa',fg='#084d81',relief='raised')
    head_label.place(x=190,y=10,width=206,height=48)


    task_entry=EntryWithPlaceholder(root,'enter task description',"#084d81",font=('Ariel',10),bg="#cffefa",textvar=TaskDesc)
    task_entry.place(x=80,y=100,width=227,height=30)

    time_entry=EntryWithPlaceholder(root,'HH:MM',"#084d81",font=('Ariel',10),bg="#cffefa",textvar=HMData)
    time_entry.place(x=310,y=100,width=99,height=30)

    DateEntry=EntryWithPlaceholder(root,'DD/MM/YYYY',"#084d81",font=('Ariel',10),bg="#cffefa",textvar=DateData)
    DateEntry.place(x=412,y=100,width=110,height=30)


    add_button=tk.Button(root,text='ADD',font=('Ariel',10),bg="#cffefa",fg="#fb630c",command=add_button_command)
    add_button.place(x=240,y=170,width=95,height=30)

    ref_button=tk.Button(root,text='⟳',font=('Ariel',20),fg="#084d81",command=refresh_list)
    ref_button.place(x=520,y=200,width=50,height=30)


    radio1=tk.Radiobutton(root,text='Least',font=('Ariel',10),variable=Radiovar,value=1)
    radio1.place(x=70,y=130,width=85,height=25)


    radio2=tk.Radiobutton(root,text='Important',font=('Ariel',10),variable=Radiovar,value=2)
    radio2.place(x=150,y=130,width=85,height=25)


    radio3=tk.Radiobutton(root,text='Urgent',font=('Ariel',10),variable=Radiovar,value=3)
    radio3.place(x=230,y=130,width=85,height=25)

Todo=todolist()

root=tk.Tk()
TaskDesc=tk.StringVar()
HMData=tk.StringVar()
DateData=tk.StringVar()
Radiovar=tk.IntVar()
Radiovar.set(0)

setscreen(root)
setlabels(root)

frame_tasks = tk.Frame(root)
frame_tasks.place(x=10,y=230,width=580,height=220)

Task_list=tk.Listbox(frame_tasks,font=('Ariel',10),borderwidth='1px')
Task_list.place(x=0,y=0,width=575,height=219)

scrollbar_tasks = tk.Scrollbar(frame_tasks)
scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.Y)

Task_list.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=Task_list.yview)

Cmp_button=tk.Button(root,text='Show Completed Tasks',bg='#cffefa',fg="#084d81",font=('Ariel',10),command=Cmp_button_command)
Cmp_button.place(x=400,y=460,width=180,height=30)

del_button=tk.Button(root,text='Delete Task',bg='#cffefa',fg="#084d81",font=('Ariel',10),command=del_button_command)
del_button.place(x=10,y=460,width=180,height=30)

root.after(1000,refresh_list)

root.mainloop()