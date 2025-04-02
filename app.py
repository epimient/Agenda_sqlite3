import tkinter as tk
import sqlite3

class App:
    def __init__(self, ventana_principal):        
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("Agenda")
    
    #base de datos
        self.con = sqlite3.connect('agenda.db')
        self.cur = self.con.cursor()
        
        self.cur.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, edad INTEGER)')
        self.con.commit()
        
        self.label_nombre = tk.Label(self.ventana_principal, text = 'Nombre')
        self.label_nombre.pack(pady = 5)
        
        self.entry_nombre = tk.Entry(self.ventana_principal)
        self.entry_nombre.pack(pady = 5)
        
        self.label_edad = tk.Label(self.ventana_principal, text = 'edad')
        self.label_edad.pack(pady = 5)
        
        self.entry_edad = tk.Entry(self.ventana_principal)
        self.entry_edad.pack(pady = 5)
        
        self.listbox = tk.Listbox(self.ventana_principal, width=50)
        self.listbox.pack(pady=5)
        
        self.boton_guardar = tk.Button(self.ventana_principal, text = 'guardar', command = self.guardar_datos)
        self.boton_guardar.pack(pady = 20)
        
        self.boton_mostrar = tk.Button(self.ventana_principal, text = 'mostrar', command = self.mostrar_datos)
        self.boton_mostrar.pack(pady = 20)
        
        self.boton_actualizar = tk.Button(self.ventana_principal, text = 'actualizar', command = self.actualizar_datos)
        self.boton_actualizar.pack(pady = 20)

        self.boton_eliminar = tk.Button(self.ventana_principal, text = 'eliminar', command = self.eliminar_datos)
        self.boton_eliminar.pack(pady = 20)
    
    def guardar_datos(self):
        nombre = self.entry_nombre.get()
        edad = self.entry_edad.get()
        
        self.cur.execute('INSERT INTO usuarios (nombre, edad) VALUES (?,?)', (nombre, edad))
        self.con.commit()
        
        self.entry_nombre.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)
    
    def mostrar_datos(self):
        self.listbox.delete(0,tk.END)
        
        self.cur.execute('SELECT * FROM usuarios')
        registros = self.cur.fetchall()
        
        for registro in registros:
            self.listbox.insert(tk.END, f"ID: {registro[0]}, Nombre: {registro[1]}, Edad: {registro[2]}")
    
    def actualizar_datos(self):
        seleccion = self.listbox.curselection()
        
        if seleccion:
            index = seleccion[0]
            registro = self.listbox.get(index)
            registro_id = registro.split(',')[0].split(':')[1]
            
            nuevo_nombre = self.entry_nombre.get()
            nueva_edad = self.entry_edad.get()
            
            self.cur.execute('UPDATE usuarios SET nombre = ?, edad = ? WHERE id = ?',(nuevo_nombre, nueva_edad, registro_id))
            self.con.commit()
            
            self.mostrar_datos()
            
            self.entry_nombre.delete(0,tk.END)
            self.entry_edad.delete(0,tk.END)
        else:
            print("No hay ningun resigistro seleccionado para actualizar")
    
    def eliminar_datos(self):
        seleccion = self.listbox.curselection()
        
        if seleccion:
            index = seleccion[0]
            registro = self.listbox.get(index)
            registro_id = registro.split(',')[0].split(':')[1]
            
            self.cur.execute('DELETE FROM usuarios WHERE id = ?',(registro_id,))
            self.con.commit()
            
            self.mostrar_datos()
        else:
            print("No hay ningun resigistro seleccionado para eliminar")

mi_ventana =tk.Tk()
app = App(mi_ventana)
mi_ventana.mainloop()
        
