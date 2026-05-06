from tkinter import *
from tkinter import ttk, filedialog
import serial.tools.list_ports
import subprocess
import threading
import signal

# ---------------- WINDOW ----------------

window = Tk()

# Center window
width = 700
height = 400
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (width / 2))
y = int((screen_height / 2) - (height / 2))

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
            output_box.after(0, lambda: output_box.insert(END, "No HEX file selected\n"))
            return

        port = port_combo.get()

        if port == "":
            output_box.after(0, lambda: output_box.insert(END, "No CH340 device detected\n"))
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

        output_box.after(
            0,
            lambda: (
                output_box.insert(END, f"\n> {cmd}\n"),
                output_box.see(END)
            )
        )

        try:
            output_box.after(0, lambda: flash_button.config(state=DISABLED))
            output_box.after(0, lambda: erase_button.config(state=DISABLED))
            current_process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )

            for line in current_process.stdout:

                output_box.after(
                    0,
                    lambda l=line: (
                        output_box.insert(END, l),
                        output_box.see(END)
                    )
                )

            current_process.wait()

            output_box.after(
                0,
                lambda: (
                    output_box.insert(END, "\n[Process finished]\n"),
                    output_box.see(END)
                )
            )

        except Exception as e:

            output_box.after(
                0,
                lambda: output_box.insert(END, f"\nError: {e}\n")
            )

        finally:
            current_process = None

            output_box.after(0, lambda: erase_button.config(state=NORMAL))
            output_box.after(0, lambda: flash_button.config(state=NORMAL))

    threading.Thread(target=worker, daemon=True).start()

def erase_chip():

    def worker():

        global current_process

        port = port_combo.get()

        if port == "":
            output_box.after(
                0,
                lambda: output_box.insert(END, "No CH340 device detected\n")
            )
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

        output_box.after(
            0,
            lambda: (
                output_box.insert(END, f"\n> {cmd}\n"),
                output_box.see(END)
            )
        )

        try:

            output_box.after(0, lambda: erase_button.config(state=DISABLED))
            output_box.after(0, lambda: flash_button.config(state=DISABLED))
            current_process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )

            for line in current_process.stdout:

                output_box.after(
                    0,
                    lambda l=line: (
                        output_box.insert(END, l),
                        output_box.see(END)
                    )
                )

            current_process.wait()

            output_box.after(
                0,
                lambda: (
                    output_box.insert(END, "\n[Erase finished]\n"),
                    output_box.see(END)
                )
            )

        except Exception as e:

            output_box.after(
                0,
                lambda: output_box.insert(END, f"\nError: {e}\n")
            )

        finally:

            current_process = None

            output_box.after(0, lambda: erase_button.config(state=NORMAL))
            output_box.after(0, lambda: flash_button.config(state=NORMAL))

    threading.Thread(target=worker, daemon=True).start()

def cancel_process():

    global current_process

    if current_process:

        try:

            current_process.send_signal(signal.CTRL_BREAK_EVENT)

            output_box.insert(END, "\n[Process cancelled]\n")
            output_box.see(END)

        except Exception as e:

            output_box.insert(END, f"\nCancel Error: {e}\n")
            output_box.see(END)

        current_process = None
        flash_button.config(state=NORMAL)
        erase_button.config(state=NORMAL)

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
flash_button = Button(Home, text="Flash", width=10, command=upload_code)
flash_button.place(x=50, y=80) 

erase_button = Button(Home, text="Erase", width=10, command=erase_chip)
erase_button.place(x=180, y=80)

Button(Home, text="Download", width=12).place(x=310, y=80) 

Button(Home, text="Cancel", width=10, command=cancel_process).place(x=440, y=80)

# Output box (CMD style) 
Label(Home, text="CMD").place(x=20, y=130) 
output_box = Text(Home, height=10, width=65) 
output_box.place(x=20, y=150)

# ---------------- START ----------------
refresh_ports()
window.mainloop()
