# 8051 Programmer UI

1. Download [Python 3.14.4](https://www.python.org/downloads/).
2. Download all the above files on the same folder.
3. Use any appropriate IDE ([Visual Studio Code](https://code.visualstudio.com/download)) to to edit the file.
4. Install required libraries:
   pySerial: For enabling serial ports and com ports.
   ```powershell
   pip install pyserial
   ```
6. Run the code then the GUI will appear.
7. Upload Arduino ISP code from Arduino IDE to the board.
8. Use the GUI to upload the HEX file and flash 8051.

# Create Executable

1. Install pyinstaller
   ```powershell
   pip install pyinstaller
   ```
2. Open terminal on the main folder.
3. Execute the command to build the executable file.
   ```powershell
   python -m PyInstaller --clean --onefile --windowed --noupx --name "8051 Programmer" --icon=prog.ico --add-data "prog.ico;." --add-data "tools;tools" 8051_programmer.py
   ```
   If the CMD shows error with python not found. Then find the correct path where the pyinstaller in installed and then put the path on the command.
   For Example:
   ```powershell
   C:\Users\HOME-PC\AppData\Local\Python\pythoncore-3.14-64\python.exe -m PyInstaller --clean --onefile --windowed --noupx --name "8051 Programmer" --icon=prog.ico --add-data "prog.ico;." --add-data "tools;tools" 8051_programmer.py
   ```
   To change the name of the .exe file, edit the --name section in the command.
4. The .exe file will be under the dist folder.
   ```plaintext
   UI/
   └── 8051 Programmer.py
   └── prog.ico
   └── tools/
       └── avrdude.exe
       └── avrdude.conf
   └── dist/
       └── 8051 Programmer.exe
   ```
   
Note: Project is under development and may contain bugs.
