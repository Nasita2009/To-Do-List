import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# --- Conexión a la base de datos ---
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",    
        database="todolist"  
    )

# --- Inicializar la base de datos ---
def inicializar_db():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            completada BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    conn.close()

# --- Cargar tareas desde la base ---
def cargar_tareas():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, descripcion, completada FROM tareas")
    for tarea in cursor.fetchall():
        estado = "Sí" if tarea[2] else "No"
        tree.insert("", tk.END, values=(tarea[0], tarea[1], estado))
    conn.close()

# --- Agregar nueva tarea ---
def agregar_tarea():
    desc = entry_tarea.get().strip()
    if not desc:
        messagebox.showwarning("Error", "La tarea no puede estar vacía.")
        return
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tareas (descripcion, completada) VALUES (%s, %s)", (desc, False))
    conn.commit()
    conn.close()
    entry_tarea.delete(0, tk.END)
    cargar_tareas()

# --- Marcar tarea como completada ---
def completar_tarea():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Error", "Seleccione una tarea.")
        return
    tarea_id = tree.item(item[0])["values"][0]
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE tareas SET completada = TRUE WHERE id = %s", (tarea_id,))
    conn.commit()
    conn.close()
    cargar_tareas()

# --- Eliminar tarea ---
def eliminar_tarea():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Error", "Seleccione una tarea.")
        return
    tarea_id = tree.item(item[0])["values"][0]
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = %s", (tarea_id,))
    conn.commit()
    conn.close()
    cargar_tareas()

# --- Interfaz gráfica ---
root = tk.Tk()
root.title("Gestor de Tareas")
root.geometry("600x400")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

entry_tarea = tk.Entry(frame_top, width=40)
entry_tarea.pack(side=tk.LEFT, padx=5)

btn_agregar = tk.Button(frame_top, text="Agregar", command=agregar_tarea)
btn_agregar.pack(side=tk.LEFT, padx=5)

columns = ("ID", "Descripción", "Completada")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(pady=10, fill=tk.BOTH, expand=True)

frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=10)

btn_completar = tk.Button(frame_bottom, text="Marcar como Completada", command=completar_tarea)
btn_completar.pack(side=tk.LEFT, padx=5)

btn_eliminar = tk.Button(frame_bottom, text="Eliminar", command=eliminar_tarea)
btn_eliminar.pack(side=tk.LEFT, padx=5)

# --- Iniciar ---
inicializar_db()
cargar_tareas()
root.mainloop()
