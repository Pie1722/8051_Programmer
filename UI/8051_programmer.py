from tkinter import *
from tkinter import ttk, filedialog
import serial.tools.list_ports

# ---------------- WINDOW ----------------

window = Tk()
window.geometry("700x400")
window.title("8051 Programmer")
window.resizable(False, False)
# ---------------- NOTEBOOK ----------------

notebook = ttk.Notebook(window)

Home = Frame(notebook)
About = Frame(notebook)

notebook.add(Home, text="Home")
notebook.add(About, text="About")

notebook.pack(expand=True, fill="both")

# ---------------- VARIABLES ----------------

selected_file = ""

# ---------------- FUNCTIONS ----------------

def browse_file():
    global selected_file

    selected_file = filedialog.askopenfilename(
        filetypes=[("HEX files", "*.hex"), ("All files", "*.*")]
    )

    if selected_file:
        file_entry.delete(0, END)
        file_entry.insert(0, selected_file)

def run_command(action):

    if selected_file == "":
        output_box.insert(END, "No HEX file selected\n")
        output_box.see(END)
        return

    output_box.insert(END, f"\n[{action.upper()}]\n")
    output_box.insert(END, f"HEX: {selected_file}\n")
    output_box.insert(END, f"MCU: {mcu_combo.get()}\n")
    output_box.insert(END, f"PORT: {port_combo.get()}\n")

    output_box.see(END)

def upload_code():
    if selected_file == "":
        output_box.insert(END, "No HEX file selected\n")
        output_box.see(END)
        return

    output_box.insert(END, f"Uploading: {selected_file}\n")
    output_box.insert(END, f"MCU: {mcu_combo.get()}\n")
    output_box.insert(END, f"Port: {port_combo.get()}\n")
    output_box.see(END)

def get_ports():
    ports = serial.tools.list_ports.comports()

    ch340_ports = []

    for port in ports:
        if "CH340" in port.description:
            ch340_ports.append(port.device)

    return ch340_ports

def refresh_ports():
    ports = get_ports()
    port_combo["values"] = ports

    if ports and port_combo.get() == "":
        port_combo.current(0)

    window.after(1000, refresh_ports)

# ---------------- HOME TAB ----------------

# File selection 
file_entry = Entry(Home, width=35) 
file_entry.place(x=20, y=20) 
Button(Home, text="Browse", command=browse_file).place(x=300, y=17) 

# COM port 
Label(Home, text="COM PORTS").place(x=390, y=0) 
port_combo = ttk.Combobox(Home, values=get_ports(), width=10) 
port_combo.place(x=380, y=20) 

ports = get_ports()

if ports:
    port_combo.current(0)

# MCU 
Label(Home, text="8051 VARIANT").place(x=500, y=0) 
mcu_combo = ttk.Combobox(Home, values=["89S51", "89S52", "89C52"], width=10) 
mcu_combo.place(x=500, y=20) 
mcu_combo.current(0) 

# Buttons 
Button(Home, text="Flash", width=10, command=lambda: run_command("flash")).place(x=50, y=80) 
Button(Home, text="Erase", width=10, command=lambda: run_command("erase")).place(x=180, y=80) 
Button(Home, text="Download", width=12).place(x=310, y=80) 

# Output box (CMD style) 
Label(Home, text="CMD").place(x=20, y=130) 
output_box = Text(Home, height=10, width=65) 
output_box.place(x=20, y=150)

# ---------------- START ----------------
refresh_ports() #check for new CH340 ports
window.mainloop()
