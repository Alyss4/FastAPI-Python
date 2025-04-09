from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ..db import getconnection
import sqlite3

router = APIRouter(prefix="/task", tags=["Task"])

class TaskCreateRequest(BaseModel):
    description: str
    status: str = "todo"
    priority: str = "medium"
    user_id: int

# GET all tasks
@router.get("/", status_code=status.HTTP_200_OK)
def get_tasks():
    try:
        conn = getconnection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, description, statut, priorite, user_id FROM TASK")
        tasks = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "description": row[1], "status": row[2], "priority": row[3], "user_id": row[4]} for row in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET task by id
@router.get("/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    conn = getconnection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, statut, priorite, user_id FROM TASK WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    if task:
        return {"id": task[0], "description": task[1], "status": task[2], "priority": task[3], "user_id": task[4]}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche non trouvée")

# POST create task
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreateRequest):
    conn = getconnection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM USER WHERE id = ?", (task.user_id,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="Utilisateur associé non trouvé")

    try:
        cursor.execute("""
            INSERT INTO TASK (description, statut, priorite, user_id)
            VALUES (?, ?, ?, ?)
        """, (task.description, task.status, task.priority, task.user_id))
        conn.commit()
        task_id = cursor.lastrowid
        return {"id": task_id}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Tâche avec cette description déjà existante")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# PUT update task
@router.put("/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: TaskCreateRequest):
    conn = getconnection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM TASK WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche non trouvée")

    try:
        cursor.execute(
            "UPDATE TASK SET description = ?, statut = ?, priorite = ?, user_id = ? WHERE id = ?",
            (task.description, task.status, task.priority, task.user_id, task_id)
        )
        conn.commit()
        return {"message": "Tâche mise à jour avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur : {str(e)}")
    finally:
        conn.close()

# DELETE task
@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int):
    conn = getconnection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM TASK WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche non trouvée")

    cursor.execute("DELETE FROM TASK WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"message": "Tâche supprimée"}