import sqlite3
from typing import Union, TypedDict, Optional

class Tasks(TypedDict):
    id: int
    title: str
    done: bool

class updateTasks(TypedDict):
    id: int
    title: Optional[str]
    done: Optional [bool]
def getdb():
    conn=sqlite3.connect('mydb.db',check_same_thread=False)
    cur=conn.cursor()
    return conn,cur
def initialize_table(conn,cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER NOT NULL,
        title TEXT NOT NULL,
        done BOOL NOT NULL
    )
    """)
    conn.commit()
def insert_data(conn,cur,records: Union[list,tuple]):
    query='INSERT INTO tasks (id,title,done) VALUES (?,?,?)'
    if isinstance(records,list):
        cur.executemany(query,records)
        conn.commit()
        return {"201":f"Successfully added {len(records)} records"}
    elif isinstance(records,tuple):
        cur.execute(query,records)
        conn.commit()
        return {"201": f"Successfully added a record"}
    else:
        return {"400": f"Error has occurred"}
def retrieve_all(conn,cur):
    cur.execute('SELECT * FROM tasks')
    results=cur.fetchall()
    data=[]
    for result in results:
        data.append({"id":result[0],"title":result[1],"done":result[2]})
    return data
def retrieve(conn,cur,id):
    cur.execute('SELECT * FROM tasks WHERE id=?',(int(id),))
    result=cur.fetchone()
    if len(result)==0:
        return {"404":{"Error":"Not found"}}
    return {"200":{"id": result[0], "title": result[1], "done": result[2]}}
def update(conn,cur,task: updateTasks):
    cur.execute("UPDATE tasks SET title=?, done=? WHERE id=?",(task['title'],task['done'],task['id']))
    conn.commit()
    return {"200":task}
def delete(conn,cur,id):
    response=retrieve(conn,cur,id)
    if "200" in response:
        cur.execute("DELETE FROM tasks WHERE id=?",(int(id),))
        conn.commit()
        return {"204":f"Task with id {id} has been deleted successfully"}
    else:
        return response