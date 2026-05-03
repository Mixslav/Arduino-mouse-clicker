# Arduino-mouse-clicker

This is an Arduino EVERY mouse clicker for the robot arm. This way the robot can click on to Windows and control my Ender 3 pnp mashine. It will repeat the PCB assembly for the RGB board.

Press a physical switch → your PC performs a left mouse click.

## Wiring

Connect the switch between Arduino pin **D2** and **GND**. That's it.

## 1. Flash the Arduino

Open this repo in **VS Code with the PlatformIO extension**, plug in the Nano Every, click **Upload**. Done. (Only needed once per board.)

## 2. Run on Windows

Copy the `host/` folder to your Windows PC, plug in the Arduino, then:

- **`run.bat`** — double-click to run with a console window (shows `click` for each press; good for testing).
- **`run-silent.vbs`** — double-click to run hidden, no console window. Drop a copy in your Startup folder (`Win+R` → `shell:startup`) to auto-launch at login.

The first run installs Python and the needed packages automatically (~1 min, internet required, accept any SmartScreen prompt). Every run after that is instant.

## Troubleshooting

| Problem | Fix |
|---|---|
| Clicks feel laggy or get stuck for a few seconds | Unplug the Arduino, plug it back in, then start `run.bat` again. |
| `Could not open port 'COMx'` | Close VS Code's Serial Monitor — it's holding the port. |
| Nothing happens on press | Check wiring (D2 ↔ switch ↔ GND) and that the firmware uploaded. The onboard LED should blink on each press. |
| SmartScreen blocks `run.bat` | Click **More info** → **Run anyway**. First run only. |
| Click happens twice per press | Increase `LOCKOUT_MS` in `src/main.cpp`, re-upload. |
