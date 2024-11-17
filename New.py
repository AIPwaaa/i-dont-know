import os
import json
import tarfile
import calendar
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import re

class ShellEmulator:
    def __init__(self, config_file):
        self.load_config(config_file)
        self.current_dir = 'a'
        self.vfs = self.load_vfs(self.vfs_path)

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        self.username = config['username']
        self.vfs_path = config['vfs_path']

    def load_vfs(self, vfs_path):
        vfs = {}
        with tarfile.open(vfs_path, 'r') as tar:
            for member in tar.getmembers():
                vfs[member.name] = member
        return vfs

    def list_directory(self, path):
        if path=='/':
            self.current_dir='a'
            return self.list_directory(self.current_dir)
        if path=='':
            path=self.current_dir
        path = path.replace('\\', '/')
        if self.current_dir in path:
            abs_path = path if path == '.' else (path.rstrip('/'))
        else:
            abs_path = self.current_dir + '/' + path if path == '.' else ((self.current_dir+'/'+path).rstrip('/'))
        if abs_path not in self.vfs or not self.vfs[abs_path].isdir():
            return f"ls: cannot access '{abs_path}': No such file or directory"
        abs_path_with_slash = abs_path if abs_path.endswith('/') else abs_path + '/'
        content = []
        for item in self.vfs:
            if item.startswith(abs_path_with_slash):
                relative_path = item[len(abs_path_with_slash):]
                if '/' not in relative_path.strip('/'):
                    content.append(relative_path)
        return " ".join(content) if content else f"{abs_path}: No files or directories found"

    def change_directory(self, path):
        if path=='a' or path=='/':
            self.current_dir='a'
            return ""
        if path==self.current_dir:
            return ""
        if self.current_dir in path or path in self.current_dir:
            abs_path = path if path == '.' else (path.rstrip('/'))
            if abs_path not in self.vfs or not self.vfs[abs_path].isdir():
                return f"cd: no such file or directory: {path}"
            self.current_dir = path
        else:
            abs_path = self.current_dir + '/' + path if path == '.' else ((self.current_dir+'/'+path).rstrip('/'))
            if abs_path not in self.vfs or not self.vfs[abs_path].isdir():
                return f"cd: no such file or directory: {path}"
            self.current_dir=abs_path
        return ""

    def whoami(self):
        return self.username

    def cal(self):
        return calendar.TextCalendar().formatmonth(2024, 11)

    import re

    def find(self, pattern):
        regex_pattern = pattern.replace('*', '.*').replace('?', '.')
        regex = re.compile(f"^{regex_pattern}$")
        results = []
        for path in self.vfs:
            if regex.search(path.split('/')[-1]):
                results.append(path)
        if results:
            return "\n".join(results)
        else:
            return f"find: '{pattern}' not found"

    def exit_shell(self):
        return "exit"

class ShellGUI:
    def __init__(self, root, emulator):
        self.emulator = emulator

        root.title("Shell Emulator")
        self.command_entry = tk.Entry(root, width=80)
        self.command_entry.bind("<Return>", self.process_command)
        self.command_entry.pack(padx=10, pady=5)

        self.output_box = scrolledtext.ScrolledText(root, height=20, width=80)
        self.output_box.pack(padx=10, pady=5)
        self.output_box.insert(tk.END, f"{self.emulator.username}@shell:~$ ")

    def process_command(self, event):
        command = self.command_entry.get()
        output = self.run_command(command)
        self.output_box.insert(tk.END, f"{command}\n{output}\n{self.emulator.username}@shell:~$ ")
        self.command_entry.delete(0, tk.END)

    def run_command(self, command):
        tokens = command.split()
        if len(tokens) == 0:
            return ""
        cmd = tokens[0]
        args = tokens[1:]

        if cmd == 'ls':
            if args:
                return self.emulator.list_directory(args[0])
            else:
                return self.emulator.list_directory(self.emulator.current_dir)
        elif cmd == 'cd':
            if args:
                return self.emulator.change_directory(args[0])
            else:
                return "cd: missing argument"
        elif cmd == 'cal':
            return self.emulator.cal()
        elif cmd == 'whoami':
            return self.emulator.whoami()
        elif cmd == 'find':
            if args:
                return self.emulator.find(args[0])
            else:
                return "find: missing argument"
        elif cmd == 'exit':
            messagebox.showinfo("Shell Emulator", "Exiting...")
            root.quit()
        else:
            return f"{cmd}: command not found"

if __name__ == "__main__":
    root = tk.Tk()
    emulator = ShellEmulator('config.json')
    gui = ShellGUI(root, emulator)
    root.mainloop()
