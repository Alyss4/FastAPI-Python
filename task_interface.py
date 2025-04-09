import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8080/task"

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de tâches")

        tk.Label(root, text="Description").pack(padx=10, pady=5)
        self.description_entry = tk.Entry(root)
        self.description_entry.pack(padx=10, pady=5)

        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.pack(padx=10, pady=10)

        tk.Button(root, text="Ajouter Tâche", command=self.create_task).pack(pady=5)
        tk.Button(root, text="Supprimer", command=self.delete_task).pack(pady=5)

        self.get_tasks()

    def get_tasks(self):
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            self.task_listbox.delete(0, tk.END)
            for task in response.json():
                display = f"ID: {task['id']} | {task['description']} | {task['status']} | {task['priority']} | User: {task['user_id']}"
                self.task_listbox.insert(tk.END, display)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def create_task(self):
        payload = {
            "description": self.description_entry.get(),
            "status": "todo",
            "priority": "medium",
            "user_id": 1
        }
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            messagebox.showinfo("Succès", "Tâche ajoutée.")
            self.get_tasks()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionne une tâche.")
            return
        task_id = int(self.task_listbox.get(selected).split("|")[0].replace("ID:", "").strip())
        try:
            response = requests.delete(f"{API_URL}/{task_id}")
            response.raise_for_status()
            messagebox.showinfo("Succès", "Tâche supprimée.")
            self.get_tasks()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
