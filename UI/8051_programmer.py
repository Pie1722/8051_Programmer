from tkinter import *
from tkinter import ttk, filedialog
import serial.tools.list_ports
import subprocess
import threading
import signal
import webbrowser
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1) # Dont autoscale the UI 

def open_github():
    webbrowser.open("https://github.com/Pie1722/8051_Programmer")

def open_license():
    webbrowser.open("https://www.gnu.org/licenses/gpl-3.0.en.html")

# ---------------- WINDOW ----------------

window = Tk()

# Center window
width = 700
height = 400
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (width / 2))
y = int((screen_height / 2) - (height / 2))
window.tk.call('tk', 'scaling', 1.3) # scale the text to 1.0
window.geometry(f"{width}x{height}+{x}+{y}")
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
current_process = None

# ---------------- FUNCTIONS ----------------

def browse_file():
    global selected_file

    selected_file = filedialog.askopenfilename(
        filetypes=[("HEX files", "*.hex"), ("All files", "*.*")]
    )

    if selected_file:
        file_entry.delete(0, END)
        file_entry.insert(0, selected_file)

def upload_code():

    def worker():

        global current_process

        if selected_file == "":
            output_box.after(0,lambda: (output_box.insert(END, "No HEX file selected!\n", "red"),output_box.see(END)))
            return
        
        port = port_combo.get()

        if port == "":
            output_box.after(0,lambda: (output_box.insert(END, "No Programmer Detected!\n", "red"),output_box.see(END)))
            return

        mcu = mcu_combo.get().lower()

        cmd = (
            f'"avrdude.exe" '
            f'-C "avrdude.conf" '
            f'-c stk500v1 '
            f'-P {port} '
            f'-p {mcu} '
            f'-b 19200 '
            f'-U flash:w:"{selected_file}":i'
        )

        output_box.after(0,lambda: (output_box.insert(END, f"\n> {cmd}\n"),output_box.see(END)))

        try:
            output_box.after(0, lambda: flash_button.config(state=DISABLED))
            output_box.after(0, lambda: erase_button.config(state=DISABLED))
            output_box.after(0, lambda: download_button.config(state=DISABLED))
            current_process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )

            for line in current_process.stdout:

                output_box.after(0,lambda l=line: (output_box.insert(END, l),output_box.see(END)))

            current_process.wait()

            output_box.after(0,lambda: (output_box.insert(END, "\n[Process finished]\n"),output_box.see(END)))

        except Exception as e:

            output_box.after(0,lambda: (output_box.insert(END, f"\nError: {e}\n","red"),output_box.see(END)))

        finally:
            current_process = None

            output_box.after(0, lambda: erase_button.config(state=NORMAL))
            output_box.after(0, lambda: flash_button.config(state=NORMAL))
            output_box.after(0, lambda: download_button.config(state=NORMAL))

    threading.Thread(target=worker, daemon=True).start()

def erase_chip():

    def worker():

        global current_process

        port = port_combo.get()

        if port == "":
            output_box.after(0,lambda: (output_box.insert(END, "No Programmer Detected!\n","red"),output_box.see(END)))
            return

        mcu = mcu_combo.get().lower()

        cmd = (
            f'"avrdude.exe" '
            f'-C "avrdude.conf" '
            f'-c stk500v1 '
            f'-P {port} '
            f'-p {mcu} '
            f'-b 19200 '
            f'-e'
        )

        output_box.after(0,lambda: (output_box.insert(END, f"\n> {cmd}\n"),output_box.see(END)))

        try:

            output_box.after(0, lambda: erase_button.config(state=DISABLED))
            output_box.after(0, lambda: flash_button.config(state=DISABLED))
            output_box.after(0, lambda: download_button.config(state=DISABLED))
            current_process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )

            for line in current_process.stdout:

                output_box.after(0,lambda l=line: (output_box.insert(END, l),output_box.see(END)))

            current_process.wait()

            output_box.after(0,lambda: (output_box.insert(END, "\n[Erase finished]\n"),output_box.see(END)))

        except Exception as e:

            output_box.after(0,lambda: (output_box.insert(END, f"\nError: {e}\n","red"),output_box.see(END)))

        finally:

            current_process = None

            output_box.after(0, lambda: erase_button.config(state=NORMAL))
            output_box.after(0, lambda: flash_button.config(state=NORMAL))
            output_box.after(0, lambda: download_button.config(state=NORMAL))

    threading.Thread(target=worker, daemon=True).start()

def download_code():

    def worker():

        global current_process

        port = port_combo.get()

        if port == "":
            output_box.after(0,lambda: (output_box.insert(END, "No Programmer Detected!\n","red"),output_box.see(END)))
            return

        save_file = filedialog.asksaveasfilename(
            defaultextension=".hex",
            filetypes=[("HEX files", "*.hex")]
        )

        if not save_file:
            return

        mcu = mcu_combo.get().lower()

        cmd = (
            f'"avrdude.exe" '
            f'-C "avrdude.conf" '
            f'-c stk500v1 '
            f'-P {port} '
            f'-p {mcu} '
            f'-b 19200 '
            f'-U flash:r:"{save_file}":i'
        )

        output_box.after(0,lambda: (output_box.insert(END, f"\n> {cmd}\n"),output_box.see(END)))

        try:

            output_box.after(0, lambda: erase_button.config(state=DISABLED))
            output_box.after(0, lambda: flash_button.config(state=DISABLED))
            output_box.after(0, lambda: download_button.config(state=DISABLED))

            current_process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )

            for line in current_process.stdout:

                output_box.after(0,lambda l=line: (output_box.insert(END, l),output_box.see(END)))

            current_process.wait()

            output_box.after(0,lambda: (output_box.insert(END, "\n[Download finished]\n"),output_box.see(END)))

        except Exception as e:

            output_box.after(0,lambda: (output_box.insert(END, f"\nError: {e}\n","red"),output_box.see(END)))

        finally:

            current_process = None

            output_box.after(0, lambda: erase_button.config(state=NORMAL))
            output_box.after(0, lambda: flash_button.config(state=NORMAL))
            output_box.after(0, lambda: download_button.config(state=NORMAL))

    threading.Thread(target=worker, daemon=True).start()

def cancel_process():

    global current_process

    if current_process:

        try:

            current_process.send_signal(signal.CTRL_BREAK_EVENT)

            output_box.insert(END, "\n[Process cancelled]\n","red")
            output_box.see(END)

        except Exception as e:

            output_box.insert(END, f"\nCancel Error: {e}\n","red")
            output_box.see(END)

        current_process = None
        flash_button.config(state=NORMAL)
        erase_button.config(state=NORMAL)
        download_button.config(state=NORMAL)

def on_closing():

    cancel_process()
    window.destroy()

def get_ports():
    ports = serial.tools.list_ports.comports()

    ch340_ports = []

    for port in ports:
        if "CH340" in port.description:
            ch340_ports.append(port.device)

    return ch340_ports

def refresh_ports():

    current = port_combo.get()

    ports = get_ports()

    port_combo["values"] = ports

    # If current selected port disappeared
    if current not in ports:

        if ports:
            port_combo.current(0)
        else:
            port_combo.set("")

    window.after(100, refresh_ports) #check for COM ports every 100ms

def add_hover(button, normal_color, hover_color):

    button.bind(
        "<Enter>",
        lambda e: button.config(bg=hover_color)
    )

    button.bind(
        "<Leave>",
        lambda e: button.config(bg=normal_color)
    )

# ---------------- HOME TAB ----------------

default_color = Button(window).cget("background")

# File selection 
file_entry = Entry(Home, width=35) 
file_entry.place(x=20, y=20) 
browse_button = Button(Home, text="Browse", command=browse_file)
add_hover(browse_button, default_color, "#ffffff") 
browse_button.place(x=300, y=17)

# COM port 
Label(Home, text="COM PORTS").place(x=390, y=0) 
port_combo = ttk.Combobox(Home, values=get_ports(), width=10) 
port_combo.place(x=380, y=20) 

ports = get_ports()

if ports:
    port_combo.current(0)

# MCU 
Label(Home, text="8051 VARIANT").place(x=500, y=0) 
mcu_combo = ttk.Combobox(Home, values=["89S51", "89S52"], width=10) 
mcu_combo.place(x=500, y=20) 
mcu_combo.current(0) 

# Buttons 
flash_button = Button(Home,text="Flash",width=10,command=upload_code)
add_hover(flash_button, default_color, "#ffffff")
flash_button.place(x=80, y=80) 

erase_button = Button(Home, text="Erase", width=10, command=erase_chip)
add_hover(erase_button, default_color, "#ffffff")
erase_button.place(x=220, y=80)

download_button = Button(Home, text="Download", width=10, command=download_code)
add_hover(download_button, default_color, "#ffffff")
download_button.place(x=360, y=80)

cancel_button = Button(Home, text="Cancel", width=10, command=cancel_process)
add_hover(cancel_button, default_color, "#ffffff")
cancel_button.place(x=500, y=80)

# Output box (CMD style) 
# Label(Home, text="CMD").place(x=20, y=130) 
output_box = Text(Home, height=10, width=65) 
output_box.place(x=20, y=150)
output_box.tag_config("red", foreground="red")

# ---------------- ABOUT TAB ----------------

Label(About,text="8051 Programmer",font=("Comic Sans MS", 16, "bold")).pack(pady=15)

Label(About,text="Simple GUI for programming 8051 using AVRDUDE",font=("Arial", 10)).pack(pady=5)

github_label = Label(About,text="Visit GitHub Page",fg="blue",cursor="hand2",font=("Arial", 10, "underline"))
github_label.pack(pady=10)
github_label.bind("<Button-1>", lambda e: open_github())

license_label = Label(About,text="Open Source License (GNU GPL V3.0)",fg="blue",cursor="hand2",font=("Arial", 10, "underline"))
license_label.pack(pady=5)
license_label.bind("<Button-1>", lambda e: open_license())

# ---------------- START ----------------
refresh_ports()
window.protocol("WM_DELETE_WINDOW", on_closing) #terminate all the process and close the window
window.mainloop()
