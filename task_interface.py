import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8080/task"

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de tâches")

        tk.Label(root, text="Description").pack()
        self.description_entry = tk.Entry(root)
        self.description_entry.pack()

        tk.Label(root, text="Statut").pack()
        self.status_var = tk.StringVar(value="todo")
        self.status_menu = tk.OptionMenu(root, self.status_var, "todo", "in_progress", "done")
        self.status_menu.pack()

        tk.Label(root, text="Utilisateur ID").pack()
        self.user_entry = tk.Entry(root)
        self.user_entry.pack()

        self.task_listbox = tk.Listbox(root, width=70, height=10)
        self.task_listbox.pack(padx=10, pady=10)
        self.task_listbox.bind('<<ListboxSelect>>', self.on_task_select)

        tk.Button(root, text="Ajouter Tâche", command=self.create_task).pack(pady=2)
        tk.Button(root, text="Mettre à jour", command=self.update_task).pack(pady=2)
        tk.Button(root, text="Supprimer", command=self.delete_task).pack(pady=2)

        self.selected_task_id = None
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
            "status": self.status_var.get(),
            "priority": "medium",
            "user_id": int(self.user_entry.get())
        }
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            messagebox.showinfo("Succès", "Tâche ajoutée.")
            self.clear_fields()
            self.get_tasks()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def update_task(self):
        if self.selected_task_id is None:
            messagebox.showwarning("Attention", "Sélectionne une tâche à modifier.")
            return

        payload = {
            "description": self.description_entry.get(),
            "status": self.status_var.get(),
            "priority": "medium",
            "user_id": int(self.user_entry.get())
        }
        try:
            response = requests.put(f"{API_URL}/{self.selected_task_id}", json=payload)
            response.raise_for_status()
            messagebox.showinfo("Succès", "Tâche mise à jour.")
            self.clear_fields()
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
            self.clear_fields()
            self.get_tasks()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def on_task_select(self, event):
        selected = self.task_listbox.curselection()
        if not selected:
            return
        task_info = self.task_listbox.get(selected[0])
        parts = [part.strip() for part in task_info.split("|")]
        self.selected_task_id = int(parts[0].replace("ID:", "").strip())
        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, parts[1])
        self.status_var.set(parts[2])
        self.user_entry.delete(0, tk.END)
        self.user_entry.insert(0, parts[4].replace("User:", "").strip())

    def clear_fields(self):
        self.selected_task_id = None
        self.description_entry.delete(0, tk.END)
        self.status_var.set("todo")
        self.user_entry.delete(0, tk.END)

def show_rainbow_animation(root):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.geometry("400x300+500+200")
    canvas = tk.Canvas(splash, width=400, height=300, bg="white")
    canvas.pack()

    colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    for i, color in enumerate(colors):
        canvas.create_arc(
            50 + i * 5, 50 + i * 5,
            350 - i * 5, 350 - i * 5,
            start=0, extent=180, style="arc", width=10, outline=color
        )

    name_label = tk.Label(splash, text="", font=("Helvetica", 16), bg="white", fg="#023047")
    name_label.place(relx=0.5, rely=0.75, anchor="center")

    name = "Friedrich Alyssa"
    index = 0

    def animate_name():
        nonlocal index
        if index <= len(name):
            name_label.config(text=name[:index])
            index += 1
            splash.after(100, animate_name)

    def start_app():
        splash.destroy()
        root.deiconify()
        TaskManagerApp(root)

    animate_name()
    splash.after(2500, start_app)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_rainbow_animation(root)
    root.mainloop()
