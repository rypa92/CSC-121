""""Ryan C Pate"""
"""
1. The attached database file, task_list_db.sqlite, contains a Task table that stores the tasks.
2. Use the three-tier architecture (presentation, business, database) for this program, and store the
code for each tier in a separate file.
3. The View Completed Tasks command should display tasks that have been completed.
4. The View Pending Tasks command should only display tasks that have not been completed.
5. The Complete a Task command should only mark a pending task as completed, not delete it
from the database.
6. The Add a Task command should save user entered task into the database as a pending task.
7. The Delete a Task may delete a completed or pending task from the database.
8. You may
"""

import database
from objects import Task
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_title("CSC-121 Final")
        self.create_widgets()

    def create_widgets(self):
        #formating
        self.line_format = "{:10s} {:40s} {:10s}"
        self.lbl = self.line_format.format("TID", "Description", "Completed")

        #labels
        self.topLabel = tk.Label(self, text=self.lbl, width=40)

        #listbox
        self.taskList = tk.Listbox(self, width=40)

        #buttons
        self.fill = tk.Button(self, text="View All", command=self.display_tasks)
        self.pend = tk.Button(self, text="View Pending", command=self.display_pend)
        self.comp = tk.Button(self, text="View Completed", command=self.display_comp)
        self.add = tk.Button(self, text="New Task", command=self.open_add)
        self.delete = tk.Button(self, text="Delete Task", command=self.open_delete)
        self.complete = tk.Button(self, text="Mark as Complete", command=self.open_complete)
        self.quit = tk.Button(self, text="Quit", command=self.destroy)

        #grid
        self.grid()
        self.topLabel.grid(row=0, column=0, columnspan=3)
        self.taskList.grid(row=1, column=0, columnspan=3)
        self.fill.grid(row=2, column=0)
        self.add.grid(row=2, column=1)
        self.delete.grid(row=2, column=2)
        self.complete.grid(row=3, column=0)
        self.comp.grid(row=3, column=1)
        self.pend.grid(row=3, column=2)
        self.quit.grid(row=4, columnspan=3)

    #commands
    def display_tasks(self):
        tasks = database.get_all_task()
        self.taskList.delete(0, self.taskList.size())
        for task in tasks:
            self.taskList.insert(task.tid, self.line_format.format(str(task.tid), str(task.desc), str(task.comp)))

    def display_comp(self):
        tasks = database.get_comp_task()
        self.taskList.delete(0, self.taskList.size())
        for task in tasks:
            self.taskList.insert(task.tid, self.line_format.format(str(task.tid), str(task.desc), str(task.comp)))

    def display_pend(self):
        tasks = database.get_pend_task()
        self.taskList.delete(0, self.taskList.size())
        for task in tasks:
            self.taskList.insert(task.tid, self.line_format.format(str(task.tid), str(task.desc), str(task.comp)))

    def open_add(self):
        nw = add_more_tasks(self)
        nw.wait_window()

    def open_delete(self):
        nw = delete_task(self)
        nw.wait_window()

    def open_complete(self):
        nw = complete_task(self)
        nw.wait_window()

    def handle_add(self, fir):
        TID = self.taskList.size() + 1
        task = Task(TID, fir, 0)
        database.add_task(task)
        self.display_tasks()

    def handle_del(self, fir):
        database.delete_task(fir)
        self.display_tasks()

    def handle_complete(self, fir):
        database.complete_task(fir)
        self.display_tasks()


class add_more_tasks(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        #labels
        self.topLBL = tk.Label(self, text="Task: ")

        #entry
        self.topENT = tk.Entry(self)

        #button
        self.btn = tk.Button(self, text="Submit", command=lambda: inputs())

        #grid
        self.grid()
        self.topLBL.grid(row=0, column=0)
        self.topENT.grid(row=0, column=1)
        self.btn.grid(row=2, columnspan=2)

        def inputs():
            desc = self.topENT.get()
            self.app.handle_add(desc)
            self.destroy()

class delete_task(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        #labels
        self.topLBL = tk.Label(self, text="Task ID: ")

        #entry
        self.topENT = tk.Entry(self)

        #button
        self.btn = tk.Button(self, text="Submit", command=lambda: inputs())

        #grid
        self.grid()
        self.topLBL.grid(row=0, column=0)
        self.topENT.grid(row=0, column=1)
        self.btn.grid(row=2, columnspan=2)

        def inputs():
            tID = int(self.topENT.get())
            self.app.handle_del(tID)
            self.destroy()

class complete_task(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        #labels
        self.topLBL = tk.Label(self, text="Task ID: ")

        #entry
        self.topENT = tk.Entry(self)

        #button
        self.btn = tk.Button(self, text="Submit", command=lambda: inputs())

        #grid
        self.grid()
        self.topLBL.grid(row=0, column=0)
        self.topENT.grid(row=0, column=1)
        self.btn.grid(row=2, columnspan=2)

        def inputs():
            tID = int(self.topENT.get())
            self.app.handle_complete(tID)
            self.destroy()


def main():
    database.connect()
    app = App()
    app.mainloop()
    database.close()


main()
