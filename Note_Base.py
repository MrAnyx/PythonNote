from tkinter import *
import sqlite3 as sql
import os


def actualiser():
	myliste.delete(0, END)
	affiche()


def del_done():

	cursor.execute("""DELETE FROM MEMO WHERE done = 1""")
	db.commit()
	actualiser()


def done(): 
	try:
		test = myliste.get(myliste.curselection())
		liste = test.split(" --> ")
		cursor.execute("""UPDATE MEMO SET done = 1 WHERE theme LIKE "%{}%" AND description LIKE "%{}%" """.format(liste[0], liste[1]))
		db.commit()
		actualiser()
	except:
		value_theme.set("Erreur")
		value_description.set("Erreur")
		value.set("Erreur")



def add():
	
	theme = value_theme.get()
	description = value_description.get()


	if(len(theme) == 0 or len(description) == 0):
		value_theme.set("Erreur")
		value_description.set("Erreur")

	else:

		color = select_color_from_theme(theme)

		cursor.execute("""INSERT INTO MEMO (theme, description, color, done) VALUES (?, ?, ?, ?)""", (theme.strip(), description, color, 0))
		db.commit()
		
		actualiser()
		raz()



def affiche():
	cursor.execute("""SELECT theme, description, color, done FROM MEMO""")
	liste = cursor.fetchall()
	for n in liste:
		myliste.insert(END, "{} --> {}".format(n[0].strip(), n[1]))
		if(n[3] == 0):color = select_color_from_theme(n[0])
		else:color = "#515151"
		myliste.itemconfig(END, bg = color)

def search():
	if(len(value.get()) == 0):
		value_theme.set("Erreur")
		value_description.set("Erreur")
		value.set("Erreur")
	else:
		if(var.get() == 1):
			myliste.delete(0,END)
			cursor.execute("""SELECT theme, description, color, done FROM MEMO WHERE theme LIKE "%{}%" """.format(value.get()))
			liste = cursor.fetchall()
			for n in liste:
				myliste.insert(END, "{} --> {}".format(n[0].strip(), n[1]))
				if(n[3] == 0):color = n[2]
				else:color = "#515151"
				myliste.itemconfig(END, bg = color)
				raz()

		elif(var.get() == 2):
			myliste.delete(0,END)
			cursor.execute("""SELECT theme, description, color, done FROM MEMO WHERE description LIKE "%{}%" """.format(value.get()))
			liste = cursor.fetchall()
			for n in liste:
				myliste.insert(END, "{} --> {}".format(n[0].strip(), n[1]))
				if(n[3] == 0):color = n[2]
				else:color = "#515151"
				myliste.itemconfig(END, bg = color)
				raz()

		else:
			value.set("Erreur")


def remove():
	
	try:
		test = myliste.get(myliste.curselection())
		liste = test.split(" --> ")
		cursor.execute("""DELETE FROM MEMO WHERE theme LIKE "%{}%" AND description LIKE "%{}%" """.format(liste[0], liste[1]))
		db.commit()
		actualiser()
	except:
		value_theme.set("Erreur")
		value_description.set("Erreur")
		value.set("Erreur")


def update():
	if(len(value_theme.get()) == 0 or len(value_description.get()) == 0 or myliste.curselection() == None):
		value_theme.set("Erreur")
		value_description.set("Erreur")

	else:
		color = select_color_from_theme(value_theme.get())

		try:
			pos = myliste.curselection()
			liste = myliste.get(pos).split(" --> ")
			cursor.execute("""UPDATE MEMO SET theme = "{}",description = "{}", color = "{}" WHERE theme LIKE "%{}%" AND description LIKE "%{}%" """.format(value_theme.get(), value_description.get(), color, liste[0], liste[1]))
			db.commit()
			actualiser()
			raz()

		except:
			value_theme.set("Erreur")
			value_description.set("Erreur")


def raz():
	value.set("")
	value_theme.set("")
	value_description.set("")
	var.set(0)



def add_theme_color():
	theme = value_theme.get()
	color = value_description.get()
	if(len(theme) == 0 or len(color) == 0):
		value_theme.set("Erreur")
		value_description.set("Erreur")
	else:
		try:
			cursor.execute("""INSERT INTO COLOR (theme, color) VALUES (?, ?)""", (theme, color))
			cursor.execute("""UPDATE MEMO SET color = "{}" WHERE theme = "{}" """.format(select_color_from_theme(theme), theme))
			db.commit()
			raz()
			actualiser()
		except:
			value_theme.set("Erreur")
			value_description.set("Erreur")


def select_color_from_theme(theme):
	color = "#FFFFFF"
	try:
		cursor.execute("""SELECT theme, color FROM COLOR WHERE theme = "{}" """.format(theme))
		test = cursor.fetchall()
		for n in test:
			color = n[1]

	except:
		color = "#FFFFFF"

	return color


def affiche_bdd():
	liste = os.listdir('BDD')
	myliste_new_open.delete(0, END)
	for n in liste:
		myliste_new_open.insert(END, n)

def new_bdd():
	liste = list(value_new_open.get())
	a = 0

	for n in liste:
		if(n == "."):
			value_new_open.set("Erreur")
			a=1

	if(len(value_new_open.get()) == 0 or a == 1):
		value_new_open.set("Erreur")
	else:
		db = sql.connect("BDD/{}.db".format(value_new_open.get()))
		cursor = db.cursor()

		cursor.execute("""
		CREATE TABLE IF NOT EXISTS MEMO(
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
			theme TEXT,
			description TEXT,
			color TEXT,
			done INTEGER)
		""")

		cursor.execute("""
		CREATE TABLE IF NOT EXISTS COLOR(
			theme TEXT PRIMARY KEY UNIQUE,
			color TEXT)
		""")
		value_new_open.set("")
		affiche_bdd()


def open_bdd():
	global cursor, db
	try:
		db = sql.connect("BDD/{}".format(myliste_new_open.get(myliste_new_open.curselection())))
		cursor = db.cursor()
		fenetre_new_open.destroy()
		fenetre_principal()
	except:
		value_new_open.set("Erreur")




def aide_new_open():
	fenetre_aide_new_open = Tk()
	fenetre_aide_new_open.title("Help")
	fenetre_aide_new_open.resizable(width = False, height = False)
	fenetre_aide_new_open.configure(bg = "#969696")

	frame_help_new_open = Frame(fenetre_aide_new_open, bg = "#969696")
	scrollbar = Scrollbar(frame_help_new_open)
	scrollbar.pack(side = RIGHT, fill = Y)

	myliste_help_new_open = Listbox(frame_help_new_open, yscrollcommand = scrollbar.set, width = 32)
	for i in range(100):
		myliste_help_new_open.insert(END, "Yolo " + str(i))
	myliste_help_new_open.pack(fill = X, side = LEFT, )

	# ajouter une BDD pour les aides

	frame_help_new_open.pack(fill=X, side = LEFT)
	scrollbar.config(command = myliste_help_new_open.yview)

	fenetre_aide_new_open.mainloop()

def aide():
	pass

def rename_new_open():
	liste = list(value_new_open.get())
	a = 0
	
	for n in liste:
		if(n == "."):
			value_new_open.set("Erreur")
			a=1

	if(len(value_new_open.get()) == 0 or a == 1 or myliste_new_open.get(myliste_new_open.curselection()) == None):
		value_new_open.set("Erreur")
	else:
		os.rename("BDD/{}".format(myliste_new_open.get(myliste_new_open.curselection())), "BDD/{}.db".format(value_new_open.get()))
		affiche_bdd()
		raz_new_open()



def remove_new_open():
	try:
		os.remove("BDD/{}".format(myliste_new_open.get(myliste_new_open.curselection())))
		affiche_bdd()

	except:
		value_new_open.set("Erreur")

def raz_new_open():
	value_new_open.set("")
###########################################################################

def fenetre_principal():
	global myliste, value, value_theme, value_description, var
	fenetre = Tk()
	fenetre.title("Memo")
	fenetre.configure(bg = "#969696")
	fenetre.resizable(width = False, height = False)
	###########################################################################
	frame1 = Frame(fenetre)

	scrollbar = Scrollbar(frame1)
	scrollbar.pack(side = RIGHT, fill = Y)

	myliste = Listbox(frame1, yscrollcommand = scrollbar.set , width = 32)
	affiche()
	myliste.pack( side = LEFT, fill = X )

	scrollbar.config(command = myliste.yview )

	frame1.pack(side = TOP, fill = X, padx = 5, pady = 10)
	###########################################################################
	frame2 = Frame(fenetre, bg = "#969696")

	value = StringVar()
	entry = Entry(frame2, textvariable = value, bg = "bisque", selectbackground = "bisque", selectforeground = "#FF0000", font = ("", 12)).pack(padx = 5, pady = 10, fill = X)

	var = IntVar()
	RB1 = Radiobutton(frame2, text = "Thème", variable = var, value = 1, bg = "#969696", activebackground = "#969696").pack(side = LEFT, padx = 25, expand = 1)
	RB2 = Radiobutton(frame2, text = "Description", variable = var, value = 2, bg = "#969696", activebackground = "#969696").pack(side = LEFT, padx = 25, expand = 1)

	frame2.pack(side = TOP, fill = X)
	###########################################################################
	frame3 = Frame(fenetre, bg = "#969696")

	value_theme = StringVar()
	entry_theme = Entry(frame3, textvariable = value_theme, bg = "bisque", selectbackground = "bisque", selectforeground = "#FF0000", font = ("", 12), width = 9).pack(side = LEFT, padx = 5, pady = 10, expand = 1)

	value_description = StringVar()
	entry_description = Entry(frame3, textvariable = value_description, bg = "bisque", selectbackground = "bisque", selectforeground = "#FF0000", font = ("", 12), width = 15).pack(side = LEFT, padx = 5, pady = 10, expand = 1)

	frame3.pack(side = TOP, fill = X)
	###########################################################################
	frame4 = Frame(fenetre, bg = "#969696")

	bouton_search = Button(frame4, text = "Search", bg = "#515151", font = ("", 11), foreground = "white", width = 7, command = search).pack(side = LEFT, padx = 5, pady = 10, expand = 1)
	bouton_done = Button(frame4, text = "Done", bg = "#515151", font = ("", 11), foreground = "white", width = 7, command = done).pack(side = LEFT, padx = 5, pady = 10, expand = 1)
	bouton_add = Button(frame4, text = "Add", bg = "#515151", font = ("", 11), foreground = "white", width = 7, command = add).pack(side = LEFT, padx = 5, pady = 10, expand = 1)

	frame4.pack(side = TOP, fill = X)
	###########################################################################
	menubar = Menu(fenetre)
	filemenu = Menu(menubar, tearoff = 0)
	filemenu.add_command(label="Exit", command=fenetre.destroy)
	menubar.add_cascade(label="File", menu=filemenu)

	edit = Menu(menubar, tearoff = 0)
	edit.add_command(label="Delete \"Done\"", command = del_done)
	edit.add_command(label="Add theme / color", command = add_theme_color)
	edit.add_separator()
	edit.add_command(label="Refresh", command = actualiser)
	edit.add_command(label="Update", command = update)
	edit.add_command(label="Remove", command = remove)
	edit.add_separator()
	edit.add_command(label="RaZ", command = raz)
	menubar.add_cascade(label="Edit", menu=edit)

	aide = Menu(menubar, tearoff = 0)
	aide.add_command(label = "Help", command = aide)
	menubar.add_cascade(label = "Other", menu = aide)
	###########################################################################
	fenetre.config(menu = menubar)
	fenetre.mainloop()
	db.close()


###########################################################################


fenetre_new_open = Tk()
fenetre_new_open.title("New / Open")
fenetre_new_open.resizable(width = False, height = False)
fenetre_new_open.configure(bg = "#969696")

frame_new_open = Frame(fenetre_new_open, bg = "#969696")
scrollbar = Scrollbar(frame_new_open)
scrollbar.pack(side = RIGHT, fill = Y)
myliste_new_open = Listbox(frame_new_open, yscrollcommand = scrollbar.set , width = 33)
affiche_bdd()
myliste_new_open.pack( side = LEFT, fill = X )
scrollbar.config(command = myliste_new_open.yview )
frame_new_open.pack(side = TOP, fill = X, padx = 5, pady = 10)

frame_new_open1 = Frame(fenetre_new_open, bg = "#969696")
value_new_open = StringVar()
entry_new_open = Entry(frame_new_open1, textvariable = value_new_open, bg = "bisque", selectforeground = "red", selectbackground = "bisque", font = ("", 12)).pack(side = TOP, padx = 5, pady = 5, fill = X)
frame_new_open1.pack(side = TOP, fill = X, padx = 5, pady = 5)

bouton_new = Button(frame_new_open1, text = "New", bg = "#515151", fg = "white", font = ("", 12), command = new_bdd).pack(expand = 1, padx = 5, pady = 15, side = LEFT, fill = X)
bouton_open = Button(frame_new_open1, text = "Open", bg = "#515151", fg = "white", font = ("", 12), command = open_bdd).pack(expand = 1, padx = 5, pady = 15, side = LEFT, fill = X)


menubar = Menu(fenetre_new_open)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label="Exit", command=fenetre_new_open.quit)
menubar.add_cascade(label="File", menu=filemenu)

edit = Menu(menubar, tearoff = 0)
edit.add_command(label="Rename", command = rename_new_open)
edit.add_command(label="Remove", command = remove_new_open)
edit.add_separator()
edit.add_command(label="RaZ", command = raz_new_open)
menubar.add_cascade(label="Edit", menu=edit)

aide = Menu(menubar, tearoff = 0)
aide.add_command(label = "Help", command = aide_new_open)
menubar.add_cascade(label = "Other", menu = aide)
fenetre_new_open.config(menu = menubar)

fenetre_new_open.mainloop()