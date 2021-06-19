import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from api import todolist
from base import task, duedate , task_from_str, check_input

def refresh_list():
    '''this is a fuction that refreshes the listbox'''
    
    #Todo.update()
    Task_list.delete(0,tk.END)
    for task in sorted(Todo.getall(),key=lambda x: x.due_on.delta()):
        Task_list.insert(tk.END,str(task))

    completed_list.delete(0,tk.END)
    for task in Todo.get_completed():
        completed_list.insert(tk.END,str(task))

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
    date=list(date.split('/'))
    msg=check_input(taskname,hm,date)
    if msg!=0:
        messagebox.showerror('Invalid or Incomplete Input',msg)
        return 
    Todo.addtask(task(taskname, '', duedate(hm,date[0],date[1],date[2])))
    refresh_list()

def del_button_command():
    #print(Task_list.get(tk.ACTIVE))
    s=str(Task_list.get(tk.ACTIVE)).split(',')
    confirm=messagebox.askquestion(f'Delete {s[0]}',f'Are you sure you want to delete {s[0]}')
    task1=task_from_str(s)
    if confirm=='yes':
        Todo.delete(task1)
        refresh_list()

def check_button_command():
    s=str(Task_list.get(tk.ACTIVE)).split(',')
    confirm=messagebox.askquestion(f'Mark {s[0]}',f'Are you sure you want to mark {s[0]} as complete?')
    task1=task_from_str(s)
    if confirm=='yes':
        Todo.mark_complete(task1)
        refresh_list()

def Cmp_button_command():
    print("command for displaying comppleted task button,under development")

def setscreen(root):
    width=600
    height=525
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
    frame_tasks = tk.Frame(root)
    frame_tasks.place(x=10,y=230,width=580,height=220)

    global Task_list
    Task_list=tk.Listbox(frame_tasks,font=('Ariel',10),borderwidth='1px')
    Task_list.place(x=0,y=0,width=564,height=210)

    scrollbar_tasks = tk.Scrollbar(frame_tasks)
    scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.Y)
    Task_list.config(yscrollcommand=scrollbar_tasks.set)
    scrollbar_tasks.config(command=Task_list.yview)

    scrollbar_tasks_h = tk.Scrollbar(frame_tasks,orient=tk.HORIZONTAL)
    scrollbar_tasks_h.pack(side=tk.BOTTOM, fill=tk.X)
    Task_list.config(xscrollcommand=scrollbar_tasks_h.set)
    scrollbar_tasks_h.config(command=Task_list.xview)

    del_button=tk.Button(root,text='Delete Task',bg='#cffefa',fg="#bd0704",font=('Ariel',10),command=del_button_command)
    del_button.place(x=400,y=460,width=180,height=30)

    check_button=tk.Button(root,text='Mark as Done',bg='#cffefa',fg="#02a628",font=('Ariel',10),command=check_button_command)
    check_button.place(x=10,y=460,width=190,height=30)

def setlabels_tab2(root):
    head_label=tk.Label(root,text='Completed Tasks',font=('Ariel',18),bg='#cffefa',fg='#084d81',relief='raised')
    head_label.place(x=190,y=10,width=206,height=48)

    frame_tasks = tk.Frame(root)
    frame_tasks.place(x=10,y=80,width=580,height=400)

    global completed_list
    completed_list=tk.Listbox(frame_tasks,font=('Ariel',10),borderwidth='1px')
    completed_list.place(x=0,y=0,width=564,height=380)

    scrollbar_tasks = tk.Scrollbar(frame_tasks)
    scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.Y)
    completed_list.config(yscrollcommand=scrollbar_tasks.set)
    scrollbar_tasks.config(command=completed_list.yview)

    scrollbar_tasks_h = tk.Scrollbar(frame_tasks,orient=tk.HORIZONTAL)
    scrollbar_tasks_h.pack(side=tk.BOTTOM, fill=tk.X)
    completed_list.config(xscrollcommand=scrollbar_tasks_h.set)
    scrollbar_tasks_h.config(command=completed_list.xview)

def set_lables_note(root):
    def save_text():
        with open('usernotes.txt','w') as f:
            txt=notepad.get("1.0", "end-1c")
            f.writelines(txt)
    
    def get_text():
        txt=''
        try:
            with open('usernotes.txt','r+') as f:
                txt=''.join(i for i in f.readlines())
        except:
            pass
        return txt

    frame_note=tk.Frame(root)
    frame_note.place(x=10,y=80,width=580,height=400)

    head_label=tk.Label(root,text='User Notes',font=('Ariel',18),bg='#cffefa',fg='#084d81',relief='raised')
    head_label.place(x=190,y=10,width=206,height=48)

    notepad=tk.Text(frame_note,font=('Ariel',10),borderwidth='1px')
    notepad.place(x=0,y=0,width=564,height=380)
    notepad.insert(tk.END,get_text())

    scrollbar_notepad = tk.Scrollbar(frame_note)
    scrollbar_notepad.pack(side=tk.RIGHT, fill=tk.Y)
    notepad.config(yscrollcommand=scrollbar_notepad.set)
    scrollbar_notepad.config(command=notepad.yview)

    save_button=tk.Button(root,text='Save',bg='#cffefa',fg="#02a628",font=('Ariel',10),command=save_text)
    save_button.place(x=10,y=460,width=190,height=30)
    


Todo=todolist()

root=tk.Tk()
TaskDesc=tk.StringVar()
HMData=tk.StringVar()
DateData=tk.StringVar()
Radiovar=tk.IntVar()
Radiovar.set(0)

setscreen(root)

tabcontrol=ttk.Notebook(root)
tab1=ttk.Frame(tabcontrol)
tab2=ttk.Frame(tabcontrol)
tab3=ttk.Frame(tabcontrol)
tabcontrol.add(tab1,text='Tasks')
tabcontrol.add(tab2,text='Finished Tasks')
tabcontrol.add(tab3,text='Notes')
tabcontrol.pack(expand=1,fill='both')

setlabels(tab1)
setlabels_tab2(tab2)
set_lables_note(tab3)

root.after(0,refresh_list)

root.mainloop()