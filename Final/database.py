import sys
import os
import sqlite3
from contextlib import closing

from objects import Task

conn = None

def connect():
    global conn
    if not conn:
        DB_File = "task_list_db.sqlite"
        conn = sqlite3.connect(DB_File)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def make_task(row):
    return Task(row["taskID"], row["description"], row["completed"])

def get_all_task():
    query = '''SELECT taskID, description, completed FROM Task'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

        tasks = []
        for row in results:
            tasks.append(make_task(row))
        return tasks

def get_comp_task():
    query = '''SELECT taskID, description, completed FROM Task WHERE completed='1' '''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

        tasks = []
        for row in results:
            tasks.append(make_task(row))
        return tasks

def get_pend_task():
    query = '''SELECT taskID, description, completed FROM Task WHERE completed='0' '''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

        tasks = []
        for row in results:
            tasks.append(make_task(row))
        return tasks

def add_task(task):
    sql = '''INSERT OR IGNORE INTO Task (taskID, description, completed)
             VALUES (?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (task.tid, task.desc, task.comp))
        conn.commit()

def delete_task(task):
    sql = '''DELETE FROM Task WHERE taskID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (task,))
        conn.commit()

def complete_task(task):
    sql = '''UPDATE TASK
             SET completed = 1
             WHERE taskID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (task,))
        conn.commit()
