# Arduino Mouse Clicker

A single physical switch that triggers a left mouse click on your PC.

- **Hardware:** Arduino Nano Every + 1 momentary switch
- **Firmware:** PlatformIO project in `src/`
- **Host:** Python script in `host/` that listens on the serial port and clicks

The Nano Every can't act as a USB HID device on its own, so this design has the Arduino send a byte over USB serial and a small Python program on the PC performs the actual click.

---

## 1. Wiring

| Switch leg | Arduino pin |
|------------|-------------|
| 1          | **D2**      |
| 2          | **GND**     |

No external resistor needed — the firmware uses `INPUT_PULLUP`.

---

## 2. Flash the Arduino (one-time)

You can do this from either Linux or Windows — whichever machine has VS Code + PlatformIO installed.

1. Install **VS Code** and the **PlatformIO IDE** extension.
2. Open this folder (`arduino-mouse-clicker`) in VS Code.
3. Plug the Nano Every into USB.
4. Click the **PlatformIO: Upload** button (➡ arrow in the bottom toolbar), or run:
   ```
   pio run -t upload
   ```

You only need to do this once per board. After that the firmware stays on the Arduino.

---

## 3. Set up and run on Windows

1. **Copy the `host/` folder** to your Windows machine (anywhere — e.g. `C:\Users\<you>\arduino-clicker\host`).
2. **Plug in the Arduino.**
3. **Double-click `run.bat`.**

That's it. The script will:

- Detect whether Python is installed. If not, it downloads and silently installs Python 3.12 for the current user (no admin needed). You may see a Windows SmartScreen / antivirus prompt the first time — click **Run** / **Allow**.
- Install `pyserial` and `pynput` if they're missing.
- Auto-detect the Nano Every's COM port by USB VID/PID.
- Start listening for switch presses.

Press the switch → one left-click. The terminal prints `click` for each one. Close the window or press `Ctrl+C` to quit.

**Subsequent runs are instant** — Python and the deps are already there, so `run.bat` skips straight to listening.

### Forcing a specific COM port

If auto-detect picks the wrong port (e.g. multiple Arduinos plugged in), open `run.bat` in Notepad and change the last command from:
```
"!PYEXE!" clicker.py
```
to:
```
"!PYEXE!" clicker.py --port COM9
```

To see which port is which: **Device Manager** → **Ports (COM & LPT)** → look for `Arduino Nano Every (COMx)`.

---

## 4. (Optional) Make it run on startup

Run `run.bat` once first so Python is installed. Then:

1. Press `Win+R`, type `shell:startup`, press Enter — this opens the Startup folder.
2. Drop **`run-silent.vbs`** (from the `host` folder) — or a shortcut to it — into that folder.
3. From now on, the clicker starts in the background at login with no visible window.

To stop it, open Task Manager and end the `pythonw.exe` process.

---

## Troubleshooting

| Problem | Likely cause |
|---|---|
| `Could not open port 'COM9'` | The Serial Monitor in VS Code/PlatformIO is still attached. Close it. |
| Nothing happens on press | Check wiring (D2 ↔ switch ↔ GND) and that the Arduino was uploaded successfully. |
| SmartScreen blocks `run.bat` | Click **More info** → **Run anyway**. This only happens the very first time. |
| Python download fails | Check your internet connection, then run `run.bat` again. |
| Click happens twice per press | Increase `DEBOUNCE_MS` in `src/main.cpp` (e.g. 50), re-upload. |
