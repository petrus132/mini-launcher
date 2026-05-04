import os
import json
import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import threading
import hashlib

# ===== CONFIG =====
MANIFEST_URL = "https://petrus132.github.io/mini-launcher/launcher/manifest.json"
APPS_DIR = os.path.join(os.getenv('APPDATA'), "MyLauncher")

BG = "#0f172a"
CARD = "#1e293b"
TEXT = "#e2e8f0"
ACCENT = "#22c55e"
WARN = "#f59e0b"

# ===== HASH =====
def sha(data):
    return hashlib.sha256(data).hexdigest()

# ===== LAUNCHER =====
class Launcher:

    def __init__(self, root):
        self.root = root
        self.root.title("Mini Launcher")
        self.root.geometry("900x600")
        self.root.configure(bg=BG)

        self.manifest = {}
        self.images = {}

        self.canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
        self.scroll = ttk.Scrollbar(root, command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas, bg=BG)

        self.frame.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

        self.load_manifest()

    # ===== LOAD =====
    def load_manifest(self):
        try:
            r = requests.get(MANIFEST_URL)
            self.manifest = r.json()
            self.render()
        except Exception as e:
            print("Manifest error:", e)

    def installed(self):
        if not os.path.exists(APPS_DIR):
            return []
        return os.listdir(APPS_DIR)

    # ===== SMART UPDATE =====
    def smart_update(self, key, cfg):
        path = os.path.join(APPS_DIR, key)
        os.makedirs(path, exist_ok=True)

        state_file = os.path.join(path, "state.json")

        if os.path.exists(state_file):
            old_state = json.load(open(state_file))
        else:
            old_state = {}

        new_state = {}

        for file in cfg["files"]:
            url = f"{cfg['base_url']}/{file}"
            try:
                r = requests.get(url)
                content = r.content
            except:
                continue

            h = sha(content)
            new_state[file] = h

            if file not in old_state or old_state[file] != h:
                print("Updating:", file)

                full_path = os.path.join(path, file)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)

                with open(full_path, "wb") as f:
                    f.write(content)

        with open(state_file, "w") as f:
            json.dump(new_state, f)

    # ===== INSTALL =====
    def install(self, key, cfg):
        threading.Thread(target=self._install, args=(key,cfg), daemon=True).start()

    def _install(self, key, cfg):
        path = os.path.join(APPS_DIR, key)
        os.makedirs(path, exist_ok=True)

        state = {}

        for f in cfg["files"]:
            url = f"{cfg['base_url']}/{f}"
            try:
                r = requests.get(url)
                content = r.content
            except:
                continue

            full_path = os.path.join(path, f)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "wb") as file:
                file.write(content)

            state[f] = sha(content)

        with open(os.path.join(path, "state.json"), "w") as f:
            json.dump(state, f)

        self.render()

    # ===== PLAY =====
   PYTHON = r"C:\Users\pwpia\AppData\Local\Programs\Python\Python313\python.exe"

    def play(self, key):
        path = os.path.join(APPS_DIR, key)
        game_file = os.path.join(path, "main.py")

        subprocess.Popen([PYTHON, game_file], cwd=path)
    # ===== UI =====
    def render(self):
        for w in self.frame.winfo_children():
            w.destroy()

        installed = self.installed()

        row = col = 0

        for key, g in self.manifest.items():

            card = tk.Frame(self.frame, bg=CARD, width=220, height=260)
            card.grid(row=row, column=col, padx=10, pady=10)
            card.pack_propagate(False)

            # ICON
            try:
                r = requests.get(f"{g['base_url']}/{g.get('icon','')}")
                img = Image.open(BytesIO(r.content)).resize((120,120))
                img = ImageTk.PhotoImage(img)
                self.images[key] = img
                tk.Label(card, image=img, bg=CARD).pack()
            except:
                pass

            tk.Label(card, text=g["name"], fg=TEXT,
                     bg=CARD, font=("Segoe UI", 11, "bold")).pack()

            tk.Label(card, text=g.get("description",""),
                     fg="#94a3b8", bg=CARD, wraplength=200).pack()

            if key in installed:
                tk.Button(card, text="PLAY",
                          bg=ACCENT, fg="black",
                          command=lambda k=key: self.play(k)).pack(pady=3)

                tk.Button(card, text="UPDATE",
                          bg=WARN, fg="black",
                          command=lambda k=key,g=g: self.smart_update(k,g)).pack(pady=3)
            else:
                tk.Button(card, text="INSTALL",
                          bg=ACCENT, fg="black",
                          command=lambda k=key,g=g: self.install(k,g)).pack(pady=5)

            col += 1
            if col >= 4:
                col = 0
                row += 1


# ===== RUN =====
if __name__ == "__main__":
    root = tk.Tk()
    app = Launcher(root)
    root.mainloop()
