' Runs clicker.py with no console window — good for autostart.
Set sh = CreateObject("WScript.Shell")
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
sh.CurrentDirectory = scriptDir
sh.Run "pythonw """ & scriptDir & "\clicker.py""", 0, False
