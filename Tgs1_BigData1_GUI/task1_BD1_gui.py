import tkinter as tk
# Libary yang pertama berfungsi untuk meng import modul tkinter, 
# Jadi untuk melihat tampilan yang ada di Libray Tkinter kita harus mengimport modul nya dulu
# Sedangkan "as" sendiri itu untuk alias/sebutan nama agar mudah buat kita
from tkinter import ttk
# Untuk memasukan sebuah widget yang ada di tkinter, agar dia bisa digunakan gituu
from tkcalendar import Calendar 
# The tkcalendar module provides 2 classes, the first is DateEntry and the second is Calendar,
# Here we take the Calendar class which functions to display a calendar widget.
from tkinter.scrolledtext import ScrolledText
# The tkinter module contains a module called scrolledtext.py and it contains a class called ScrolledText,
# The ScrolledText class functions to display the scroll bar widget vertically.
from time import strftime
# strftime atau string from time adalah modul untuk menjalankan fungsi yang berhubungan dengan waktu, 
# metode waktu strftime() mengonversi tuple atau struct_time.
from tkinter import *

todos = {}

def detailTodo(cb = None):
    win = tk.Toplevel()
    win.wm_title("Description Details") # change text from 'Detail Keterangan' to 'Description Details'
    selectedItem = treev.focus()
    selectedIndex = treev.item(selectedItem)['text']
    selectedTodo = todos[tanggal][selectedIndex]
    judul = tk.StringVar(value = selectedTodo['Title'])
    tk.Label(win, text = "Time: ").grid(row = 0, column = 0, sticky = "N") # change text from 'Waktu' to 'Time' 
    tk.Label(win, text = "{} | {}".format(tanggal, selectedTodo["Time"])).grid(row = 0, column = 1, sticky = "E")
    tk.Label(win, text = "Title: ").grid(row = 1, column = 0, sticky = "N") # change text from 'Judul' to 'Title'
    tk.Entry(win, state = "disabled", textvariable = judul).grid(row = 1, column = 1, sticky = "E")
    tk.Label(win, text = "Description: ").grid(row = 2, column = 0, sticky = "N") # change text from 'Keterangan' to 'Description'
    keterangan = ScrolledText(win, width = 12, height = 5)
    keterangan.grid(row = 2, column = 1, sticky = "E")
    keterangan.insert(tk.INSERT, selectedTodo["Description"])
    keterangan.configure(state = "disabled")

def LoadTodos():
    global todos
    f = open('kegiatanku.dat', 'r') # rename file from 'mytodo.dat' to 'kegiatanku.dat'
    data = f.read()
    f.close()
    todos = eval(data)
    ListTodo()

def SaveTodos():
    f = open('kegiatanku.dat', 'w') # rename file from 'mytodo.dat' to 'kegiatanku.dat'
    f.write(str(todos))
    f.close()

def delTodo():
    tanggal = str(cal.selection_get())
    selectedItem = treev.focus()
    todos[tanggal].pop(treev.item(selectedItem)['text'])
    ListTodo()

def ListTodo(cb = None):
    for i in treev.get_children():
        treev.delete(i)
    tanggal = str(cal.selection_get())
    if tanggal in todos:
        for i in range(len(todos[tanggal])):
            treev.insert("", "end", text = i, values = (todos[tanggal][i]['Time'], todos[tanggal][i]['Title'], todos[tanggal][i]['Description']))
# add Description to ListTodo

def addTodo(win, key, jam, menit, judul, keterangan):
    newTodo = {
        "Time":"{}:{}".format(jam.get(), menit.get()),
        "Title":judul.get(),
        "Description": keterangan.get("1.0", tk.END)
    }   #rename "tanggal", "judul", "keterangan" to "time", "title", "description" // by Malvin 
    if key in todos:
        todos[key].append(newTodo)
    else:
        todos[key] = [newTodo]
    win.destroy()
    ListTodo()

def AddForm():
    win = tk.Toplevel()
    win.wm_title("+")
    jam = tk.IntVar(value = 10)
    menit = tk.IntVar(value = 30)
    judul = tk.StringVar(value = "")
    tk.Label(win, text = "Time: ").grid(row = 0, column = 0)
    tk.Spinbox(win, from_=0, to = 23, textvariable = jam, width = 3).grid(row = 0, column = 1)
    tk.Spinbox(win, from_=0, to = 59, textvariable = menit, width = 3).grid(row = 0, column = 2)
    tk.Label(win, text = "Title: ").grid(row = 1, column = 0)
    tk.Entry(win, textvariable = judul).grid(row = 1, column = 1, columnspan = 2)
    tk.Label(win, text = "Description: ").grid(row = 2, column = 0)
    keterangan = ScrolledText(win, width = 20, height = 5)
    keterangan.grid(row = 2, column = 1, columnspan = 2, rowspan = 4)
    tanggal = str(cal.selection_get())
    tk.Button(win, text = "Add", command = lambda: addTodo(win, tanggal, jam, menit, judul, keterangan)).grid(row = 6, columnspan = 3)
#rename "tanggal", "judul", "keterangan", "tambah" to "time", "title", "description", "add" // by Malvin 



root = tk.Tk()
# untuk membuat ukuran canvas // by bayu
root.geometry("850x350")
# untuk mengatur agar tidak bisa di ganti-ganti ukuranya, False 1 untuk X, False 2 untuk Y // by bayu
# bg = PhotoImage(file = "nama_file.png") # to load image file
# label1 = tk.Label( root, image = bg) # show image
# label1.place(x = 0,y = 0) # show image
root.resizable(False,False)
# untuk menambahkan judul // by bayu
root.title("Your Task is Here")
cal = Calendar(root, font = "Consolas", weight = "Bold", selectmode = 'day', locale = 'id_ID', cursor = 'tcross')
# Change the font from 'Times' to 'Consolas' and change the cursor from 'hand1' to 'tcross' // by Malvin
cal.grid(row = 1, column = 0, sticky = 'N', rowspan = 7)
cal.bind("<<CalendarSelected>>", ListTodo)
tanggal = str(cal.selection_get())
treev = ttk.Treeview(root)
treev.grid(row = 0, column = 1, sticky = 'WNE', rowspan = 4, columnspan = 2)
scrollBar = tk.Scrollbar(root, orient = "vertical", command = treev.yview)
scrollBar.grid(row = 0, column = 3, sticky = "ENS", rowspan = 4)
treev.configure(yscrollcommand=scrollBar.set)
treev.bind("<Double-1>", detailTodo)
treev["columns"] = ('1', '2', '3') # add column 3
treev["show"] = 'headings'
treev.column("1", width = 80)
# Change width from 100 to 80
treev.heading("1", text = "TIME")
treev.heading("2", text = 'TITLE')
treev.heading("3", text = 'DESCRIPTION') # add column 3 'DESCRIPTION'
# Change text from 'JAM' to 'TIME', 'JUDUL' to 'TITLE' // by malvin
btnAdd = tk.Button(root, text = "Add", width = 20, bg = "PeachPuff3", fg = "DarkMagenta", command = AddForm)
# Change text from 'Tambah' to 'Add'
# Change the color from black to dark magenta
btnAdd.grid(row = 4, column = 1, sticky = "N")
btnDel = tk.Button(root, text = "Delete", width = 20, bg = "PeachPuff3", fg = "red3", command = delTodo)
# Change text from 'Hapus' to 'Delete'
# Change the color from black to red
btnDel.grid(row = 4, column = 2, sticky = "N" )
btnLoad = tk.Button(root, text = "Load", width = 20, bg = "PeachPuff3", fg = "blue3", command = LoadTodos)
# Change the color from black to blue
btnLoad.grid(row = 5, column = 1, sticky = "S")
btnSave = tk.Button(root, text = "Save", width = 20, bg = "PeachPuff3", fg = "DarkGreen", command = SaveTodos)
# Change the color from black to dark green
btnSave.grid(row = 5, column = 2, sticky = "S")
root.mainloop()