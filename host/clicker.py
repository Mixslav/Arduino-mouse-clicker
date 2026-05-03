import argparse
import ctypes
import sys
from ctypes import wintypes

import serial
from serial.tools import list_ports

ARDUINO_VID = 0x2341
NANO_EVERY_PIDS = {0x0058, 0x8058}

# --- Direct Windows SendInput click (no pynput) ---
INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

ULONG_PTR = ctypes.c_size_t


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class _INPUT_UNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT)]


class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("u", _INPUT_UNION),
    ]


_user32 = ctypes.windll.user32
_user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
_user32.SendInput.restype = wintypes.UINT


def left_click():
    down = INPUT()
    down.type = INPUT_MOUSE
    down.mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, 0)

    up = INPUT()
    up.type = INPUT_MOUSE
    up.mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, 0)

    n1 = _user32.SendInput(1, ctypes.byref(down), ctypes.sizeof(INPUT))
    n2 = _user32.SendInput(1, ctypes.byref(up), ctypes.sizeof(INPUT))
    return n1, n2


def find_nano_every():
    matches = []
    for p in list_ports.comports():
        desc = (p.description or "") + " " + (p.product or "" if p.product else "")
        is_match = "nano every" in desc.lower()
        if not is_match and p.vid == ARDUINO_VID and p.pid in NANO_EVERY_PIDS:
            is_match = True
        if is_match:
            matches.append(p)
    return matches


def pick_port():
    ports = list(list_ports.comports())
    if not ports:
        sys.exit("No serial ports found. Plug in the Arduino.")
    print("Available ports:")
    for i, p in enumerate(ports):
        print(f"  [{i}] {p.device}  {p.description}")
    choice = input("Pick a port number: ").strip()
    return ports[int(choice)].device


def resolve_port(explicit):
    if explicit:
        return explicit
    matches = find_nano_every()
    if len(matches) == 1:
        print(f"Auto-detected Nano Every on {matches[0].device}")
        return matches[0].device
    if len(matches) > 1:
        print("Multiple Nano Every boards found:")
        for i, p in enumerate(matches):
            print(f"  [{i}] {p.device}  {p.description}")
        choice = input("Pick one: ").strip()
        return matches[int(choice)].device
    print("No Nano Every auto-detected — falling back to manual list.")
    return pick_port()


def main():
    parser = argparse.ArgumentParser(description="Arduino serial -> mouse click")
    parser.add_argument("--port", help="e.g. COM9 on Windows")
    parser.add_argument("--baud", type=int, default=115200)
    args = parser.parse_args()

    port = resolve_port(args.port)

    with serial.Serial(port, args.baud, timeout=None) as ser:
        print(f"Listening on {port} @ {args.baud}. Ctrl+C to quit.", flush=True)
        while True:
            b = ser.read(1)
            if b == b".":
                continue  # heartbeat — keeps USB pipe flushing
            if b == b"C":
                try:
                    left_click()
                    print("click", flush=True)
                except Exception as e:
                    print(f"ERROR: {type(e).__name__}: {e}", flush=True)
            else:
                print(f"recv: {b!r}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
