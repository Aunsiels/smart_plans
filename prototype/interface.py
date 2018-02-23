"""
Here, we are implementing a GUI the manipulate what we did. Basically, a user
will be able to write function and a query and check whether a smart plan
exists or not. In addition, it is possible to save and load functions.
"""

from tkinter import Tk, StringVar, Entry
from tkinter import Menu, END
from tree_function import TreeFunction
from function_indexed_grammar import FunctionIndexedGrammar
from tkinter.messagebox import showinfo, askokcancel
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, PhotoImage, RIGHT, Y, Scrollbar, VERTICAL
from tkinter import Canvas, BOTH, NW, Toplevel, Text, LEFT, YES
import re
import subprocess

# The general window
window = Tk(className=" Smart Plan Demo")

# The location where the functions are written
input_functions = ScrolledText(window, width=100, height=80)
input_functions.insert('1.0', "f1 :- c,c,b")

scrollbar = Scrollbar(window)
scrollbar.pack(side=RIGHT, fill=Y)

canevas0 = Canvas(window, bg='#FFFFFF',
                  scrollregion=(0, 0, 10000, 10000))
scrollbar.config(command=canevas0.yview)

# canevas0.config(width=250, height=200)
canevas0.config(yscrollcommand=scrollbar.set)
canevas0.pack(side=RIGHT, expand=True, fill=BOTH)


def get_functions():
    l_f = input_functions.get('1.0', END).split("\n")
    # Remove empty lines
    l_f = filter(lambda x: len(x) > 0, l_f)
    # '#' is used for comments
    l_f = filter(lambda x: x[0] != '#', l_f)
    functions = []
    for x in l_f:
        try:
            functions.append(TreeFunction(x))
        except ValueError:
            showinfo("Incorrect Function", "The function : '" + x +
                     "' is incorrect")
            return []
    return functions


def print_var(event=None):
    """print_var
    Reads the functions and the query and says if there exists a smart plan or
    not.
    :param event: The event which called the function
    """
    functions = get_functions()
    q = [x.strip() for x in query.get().split(",")]
    i_grammar = FunctionIndexedGrammar(functions, [q])
    if i_grammar.is_empty():
        showinfo("Emptyness", "There exists no smart plan")
    else:
        showinfo("Emptyness", "There exists a smart plan")


# The location where is query is written
query = StringVar()
query.set("query")
input_query = Entry(window, textvariable=query, width=100)
input_query.pack()

# Print the input area of functions
input_functions.pack()


# Menu creation


def open_command(event=None):
    """open_command
    Opens a file containing functions and store them in the text area
    :param event: The event which called the function
    """
    file = filedialog.askopenfile(parent=window,
                                  mode='rb',
                                  title='Select a file')
    if file is not None:
        contents = file.read()
        input_functions.delete('1.0', END)
        input_functions.insert('1.0', contents)
        file.close()


def save_command(event=None):
    """save_command
    Saves the functions in the text area in a file
    :param event: The event which called the function
    """
    file = filedialog.asksaveasfile(mode='w')
    if file is not None:
        # slice off the last character from get, as an extra return
        # is added
        data = input_functions.get('1.0', END+'-1c')
        file.write(data)
        file.close()


def exit_command(event=None):
    """exit_command
    Closes the window
    :param event: The event which called the function
    """
    if askokcancel("Quit", "Do you really want to quit?"):
        window.destroy()


def about_command():
    """about_command Shows an about page"""
    showinfo("About",
             "Made with <3 by Julien Romero")


def new_command(event=None):
    """new_command
    Creates an empty area for functions
    :param event: The event which called this function
    """
    input_functions.delete('1.0', END)
    query.set("query")


def write_prolog(functions, query, max_depth, filename):
    with open(filename, "w") as f:
        # Stop rules
        f.write("p([], _, []).\n")
        f.write("p(_, Counter, _) :- Counter =< 0, !, fail.\n")

        # Produce all the rules from the function
        for function in functions:
            f.write("\n".join(function.get_prolog_rules()) + "\n")

        query = ",".join([re.sub("-", "", r) + "m" * (r.count("-") % 2)
                          for r in [re.sub("\s+", ",", x.strip())
                                    for x in query.split(',')]])

        # Initialization rules
        f.write("q(X) :- p([" + query + "], X, L), print(L).\n")
        f.write("q(X) :- X < " + str(max_depth) + ", q(X + 1).\n")
        f.write("q(_).\n")
        # To start automatically the program in prolog
        f.write(":- initialization main.\n")
        f.write("main :- q(1), halt(0).\n")


def read_output(output):
    functions = []
    state = False
    current_function = []
    for c in output.decode('UTF-8'):
        if c == '"' or c == '"':
            if state and (("(" not in current_function and
                           ")" not in current_function)
                          or len(current_function) > 1):
                functions.append("".join(current_function).strip())
                current_function = []
            state = not state
        elif state and c != " ":
            current_function.append(c)
    res = ",".join(functions)
    res = re.sub("\(\,", "(", res)
    res = re.sub("\,\(", "(", res)
    res = re.sub("\,\)", ")", res)
    res = re.sub("\)\,", ")", res)
    res = re.sub("\;\,", ";", res)
    res = re.sub("\,\;", ";", res)
    return res


def find_prolog(event=None):
    functions = get_functions()
    q = query.get()
    q_g = [x.strip() for x in query.get().split(",")]
    i_grammar = FunctionIndexedGrammar(functions, [q_g])
    if i_grammar.is_empty():
        showinfo("Prolog",
                 "There exists no smart plan")
        return
    write_prolog(functions, q, 10, "tmp_prolog.pl")
    p = subprocess.Popen(["swipl", "-f", "tmp_prolog.pl", "-q", "main"],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()
    if (len(output) == 0):
        showinfo("Prolog",
                 "No plan found by Prolog")
    else:
        showinfo("Prolog",
                 "The found plan:\n" + read_output(output))


def show_prolog_rules(event=None):
    functions = get_functions()
    q = query.get()
    write_prolog(functions, q, 10, "tmp_prolog.pl")
    rule_window = Toplevel(window)
    text = Text(rule_window)
    with open("tmp_prolog.pl") as f:
        for line in f:
            text.insert(END, line)
    text.pack(side=LEFT, fill=BOTH, expand=YES)
    yscrollbar = Scrollbar(rule_window, orient=VERTICAL, command=text.yview)
    yscrollbar.pack(side=RIGHT, fill=Y)
    text["yscrollcommand"] = yscrollbar.set


dicimg = {}


def show_functions(event=None):
    counter = 0
    h = 0
    for key in dicimg:
        dicimg[key] = None
    for function in get_functions():
        function.save_gif("temp_graph")
        img = PhotoImage(file="temp_graph.gif")
        dicimg['img' + str(counter)] = img
        counter += 1
        canevas0.create_image(0, h, image=img, anchor=NW)
        h += img.height()
    canevas0.config(scrollregion=(0, 0, h, h))


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
runmenu.add_command(label="Show Functions   F2", command=show_functions)
runmenu.add_command(label="Prolog   F3", command=find_prolog)
runmenu.add_command(label="Show Prolog Rules  F4", command=show_prolog_rules)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about_command)


# Shortcuts

window.bind('<Control-s>', save_command)
window.bind('<Control-o>', open_command)
window.bind('<Control-n>', new_command)
window.bind('<Control-q>', exit_command)
window.bind('<F1>', print_var)
window.bind('<F2>', show_functions)
window.bind('<F3>', find_prolog)
window.bind('<F4>', show_prolog_rules)


window.mainloop()
