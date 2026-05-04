from tkinter import *
from tkinter import ttk
import webbrowser
from tkinter import filedialog
import serial.tools.list_ports

def open_github():
    webbrowser.open("https://github.com/Pie1722/8051_Programmer")

def open_license():
    webbrowser.open("https://opensource.org/licenses/MIT")

window = Tk()

# window size
width = 700
height = 500

# screen size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# calculate position
x = int((screen_width / 2) - (width / 2))
y = int((screen_height / 2) - (height / 2))

window.geometry(f"{width}x{height}+{x}+{y}")
window.title("8051 Programmer")

notebook = ttk.Notebook(window)

Home = Frame(notebook)
About = Frame(notebook)

notebook.add(Home, text="Home")
notebook.add(About, text="About")
notebook.pack(expand=True, fill="both")

Label(Home, text="This is Tab 1").pack(pady=20)

Label(About, text="8051 Programmer").pack(pady=5)

github_label = Label(About,
                     text="Visit my GitHub page for more info",
                     fg="blue", cursor="hand2")
github_label.pack(pady=5)
github_label.bind("<Button-1>", lambda e: open_github())

license_label = Label(About,
                      text="Open Source License",
                      fg="blue", cursor="hand2")
license_label.pack(pady=5)
license_label.bind("<Button-1>", lambda e: open_license())

window.mainloop()
