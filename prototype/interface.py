from tkinter import Tk, Label, Button, StringVar, Entry, PanedWindow
from tkinter import HORIZONTAL, TOP, BOTH, Y, Menu, END
from tree_function import TreeFunction
from function_indexed_grammar import FunctionIndexedGrammar
from tkinter.messagebox import showinfo, askokcancel
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

window = Tk(className=" Smart Plan Demo")

input_functions = ScrolledText(window, width=100, height=80)
input_functions.insert('1.0', "f1 :- c,c,b")

def print_var(event=None):
    l_f = input_functions.get('1.0', END).split("\n")
    l_f = filter(lambda x: len(x) > 1, l_f)
    l_f = filter(lambda x: x[0] != '#', l_f)
    functions = []
    for x in l_f:
        try:
            functions.append(TreeFunction(x))
        except ValueError:
            showinfo("Incorrect Function", "The function : '" + x + \
                     "' is incorrect")
            return
    q = query.get().split(",")
    i_grammar = FunctionIndexedGrammar(functions, [q])
    if i_grammar.is_empty():
        showinfo("Emptyness", "There exists no smart plan")
    else:
        showinfo("Emptyness", "There exists a smart plan")


query = StringVar()
query.set("query")
input_query = Entry(window, textvariable=query, width=100)
input_query.pack()

# entrée
input_functions.pack()

# create a menu & define functions for each menu item

def open_command(event=None):
    file = filedialog.askopenfile(parent=window,mode='rb',title='Select a file')
    if file != None:
        contents = file.read()
        input_functions.delete('1.0', END)
        input_functions.insert('1.0',contents)
        file.close()

def save_command(event=None):
    file = filedialog.asksaveasfile(mode='w')
    if file != None:
        # slice off the last character from get, as an extra return
        # is added
        data = input_functions.get('1.0', END+'-1c')
        file.write(data)
        file.close()

def exit_command(event=None):
    if askokcancel("Quit", "Do you really want to quit?"):
        window.destroy()

def about_command():
    label = showinfo("About",
                     "A work made with <3")

def new_command(event=None):
    input_functions.delete('1.0', END)
    query.set("query")

menu = Menu(window)
window.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New     Ctrl+N", command=new_command)
filemenu.add_command(label="Open... Ctrl+O", command=open_command)
filemenu.add_command(label="Save    Ctrl+S", command=save_command)
filemenu.add_separator()
filemenu.add_command(label="Exit    Ctrl+Q", command=exit_command)
runmenu = Menu(menu)
menu.add_cascade(label="Run", menu=runmenu)
runmenu.add_command(label="Existence   F1", command=print_var)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about_command)
# end of menu creation

window.bind('<Control-s>', save_command)
window.bind('<Control-o>', open_command)
window.bind('<Control-n>', new_command)
window.bind('<Control-q>', exit_command)
window.bind('<F1>', print_var)


window.mainloop()
