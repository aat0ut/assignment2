from fastapi import FastAPI
from typing import TypedDict
import db
app = FastAPI()

class Tasks(TypedDict):
    id: int
    title: str
    done: bool
tasks=[
    Tasks(id=1,title='solve homework',done=False),
    Tasks(id=2,title='get groceries', done=True),
    Tasks(id=3, title='work out', done=False)
]
tasks_tuples=[(rec['id'], rec['title'], rec['done']) for rec in tasks]
conn,cur=db.getdb()
db.initialize_table(conn,cur)

data=db.retrieve_all(conn,cur)

if len(data)==0:
    db.insert_data(conn,cur,tasks_tuples)
@app.get('/sql/')
def return_data():
    retrieved=db.retrieve_all(conn,cur)
    return {"200":retrieved}
@app.get("/")
def return_details():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }
@app.get("/tasks")
def return_tasks():
    return {"200":tasks}

@app.get("/tasks/{req_id}")
def return_task_id(req_id: int):
    if req_id is None or req_id not in (task.get('id') for task in tasks):
        return { "ERROR CODE 404": f"Task {req_id} not found" }
    else:
        return {"200":(task for task in tasks if task["id"]==req_id)}
@app.get("/health")
def return_health():
    return {"200":"read",'status':"ok"}

# No need for explicit validation since Tasks enforces not null values
@app.post("/tasks/")
def create_task(task: Tasks):
    if task:
        tasks.append(task)
        return {"200":{'id': task['id'], 'title': task['title'], 'done': task['done']}}
    else:
        return {"404":"Invalid ID"}
@app.put("/tasks/{req_id}")
def update_task(req_id: int, title: str, done: bool):
    for task in tasks:
        if task.get('id')==req_id:
            task['title']=title
            task['done']=done
            return {"200":task}
    return {"Error 404": f"Task with id: {req_id} does not exist"}

@app.delete("/tasks/{req_id}")
def del_task(req_id: int):
    for task in tasks:
        if task['id']==req_id:
            del tasks[tasks.index(task)]
            return {"204":f"Task wit id {req_id} has been deleted"}
    return {"Error 404": f"Task with id: {req_id} does not exist"}