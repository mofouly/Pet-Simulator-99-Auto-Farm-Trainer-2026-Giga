import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import offsets
from memory import Trainer

class TrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Giga Pet Simulator 99 Auto Farm Trainer 2026")
        self.root.geometry("450x500")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        # memory connection
        self.mem = None
        self.running = False
        self.threads = []

        # GUI variables
        self.var_auto_coin = tk.BooleanVar(value=False)
        self.var_auto_hatch = tk.BooleanVar(value=False)
        self.var_league = tk.BooleanVar(value=False)
        self.var_instant_break = tk.BooleanVar(value=False)
        self.var_teleport = tk.BooleanVar(value=False)
        self.var_merchant = tk.BooleanVar(value=False)
        self.var_speed = tk.BooleanVar(value=False)
        self.var_antiafk = tk.BooleanVar(value=False)

        self.build_ui()


    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Select Features", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)

        checks = [
            ("Auto Coin Farm", self.var_auto_coin),
            ("Auto Egg Hatch", self.var_auto_hatch),
            ("Backrooms League Auto-Grind", self.var_league),
            ("Instant Break", self.var_instant_break),
            ("Teleport to Best Zone", self.var_teleport),
            ("Auto Merchant Buy", self.var_merchant),
            ("Speed Hack", self.var_speed),
            ("Anti-AFK", self.var_antiafk),
        ]

        row = 1
        for text, var in checks:
            ttk.Checkbutton(main_frame, text=text, variable=var).grid(row=row, column=0, sticky=tk.W, pady=2)
            row += 1

        ttk.Separator(main_frame, orient="horizontal").grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        row += 1

        self.status_label = ttk.Label(main_frame, text="Status: Idle", foreground="gray")
        self.status_label.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=10, sticky=tk.W)

        self.start_btn = ttk.Button(btn_frame, text="Start", command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.exec_all_btn = ttk.Button(btn_frame, text="Execute All", command=self.execute_all)
        self.exec_all_btn.pack(side=tk.LEFT, padx=5)

        ttk.Label(main_frame, text="Press F1 to toggle GUI visibility", foreground="blue").grid(row=row+1, column=0, columnspan=2, pady=5)
        self.root.bind("<F1>", lambda e: self.toggle_visibility())


    def toggle_visibility(self):
        if self.root.state() == "withdrawn":
            self.root.deiconify()
        else:
            self.root.withdraw()

    def connect_memory(self):
        try:
            self.mem = Trainer()
            return True
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            return False

    def start(self):
        if self.running:
            return
        if not self.connect_memory():
            return

        self.running = True
        self.status_label.config(text="Status: Running", foreground="green")
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        # spawn threads for enabled features

        if self.var_auto_coin.get():
            t = threading.Thread(target=self.auto_coin_loop, daemon=True)
            t.start()
            self.threads.append(t)


        if self.var_auto_hatch.get():
            t = threading.Thread(target=self.auto_hatch_loop, daemon=True)
            t.start()
            self.threads.append(t)


        if self.var_league.get():
            t = threading.Thread(target=self.league_loop, daemon=True)
            t.start()
            self.threads.append(t)


        if self.var_instant_break.get():
            t = threading.Thread(target=self.instant_break_loop, daemon=True)
            t.start()
            self.threads.append(t)


        if self.var_teleport.get():
            try:
                self.mem.write_float(offsets.PLAYER_X, offsets.BEST_ZONE_COORDS[0])
                self.mem.write_float(offsets.PLAYER_Y, offsets.BEST_ZONE_COORDS[1])
                self.mem.write_float(offsets.PLAYER_Z, offsets.BEST_ZONE_COORDS[2])
            except:
                pass


        if self.var_merchant.get():
            t = threading.Thread(target=self.merchant_loop, daemon=True)
            t.start()
            self.threads.append(t)


        if self.var_speed.get():
            t = threading.Thread(target=self.speed_loop, daemon=True)
            t.start()
            self.threads.append(t)


        if self.var_antiafk.get():
            t = threading.Thread(target=self.antiafk_loop, daemon=True)
            t.start()
            self.threads.append(t)


    def stop(self):
        self.running = False
        self.status_label.config(text="Status: Idle", foreground="gray")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def execute_all(self):
        """One-click activate all features."""
        self.var_auto_coin.set(True)
        self.var_auto_hatch.set(True)
        self.var_league.set(True)
        self.var_instant_break.set(True)
        self.var_teleport.set(True)
        self.var_merchant.set(True)
        self.var_speed.set(True)
        self.var_antiafk.set(True)
        self.start()

    # ------ Feature loops ------

    def auto_coin_loop(self):
        while self.running and self.mem:
            try:
                self.mem.write_int(offsets.COIN_OFFSET, offsets.MAX_COIN_VALUE)
                self.mem.write_int(offsets.GEMS_OFFSET, offsets.MAX_GEMS_VALUE)
            except:
                pass
            time.sleep(0.29)


    def auto_hatch_loop(self):
        while self.running and self.mem:
            try:
                self.mem.write_int(offsets.EGG_HATCH_FLAG, 1)
            except:
                pass
            time.sleep(0.39)


    def league_loop(self):
        tasks_count = 8
        while self.running and self.mem:
            try:
                for i in range(tasks_count):
                    addr = offsets.BACKROOMS_TASK_PROGRESS_BASE + (i * 4)
                    self.mem.write_int(addr, 1)
                self.mem.write_int(offsets.BACKROOMS_REWARD_CLAIM_FLAG, 1)
            except:
                pass
            time.sleep(0.69)


    def instant_break_loop(self):
        while self.running and self.mem:
            try:
                health_ptr = self.mem.read_int(offsets.BREAKABLE_HEALTH_PTR)
                if health_ptr:
                    for i in range(50):
                        self.mem.write_float(health_ptr + i * 4, 0.0)
            except:
                pass
            time.sleep(0.35)


    def merchant_loop(self):
        while self.running and self.mem:
            try:
                self.mem.write_int(offsets.MERCHANT_BUY_FLAG, 1)
            except:
                pass
            time.sleep(0.55)


    def speed_loop(self):
        while self.running and self.mem:
            try:
                self.mem.write_float(offsets.SPEED_MULTIPLIER, 50.0)
            except:
                pass
            time.sleep(0.18)


    def antiafk_loop(self):
        while self.running and self.mem:
            try:
                self.mem.write_int(offsets.AFK_TIMER, 0)
            except:
                pass
            time.sleep(5.12)


if __name__ == "__main__":
    root = tk.Tk()
    # Set dark theme colours
    root.configure(bg="#1e1e1e")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", background="#EE82EE", foreground="white")
    style.configure("TLabel", background="#1e1e1e", foreground="white")
    style.configure("TCheckbutton", background="#1e1e1e", foreground="white")
    app = TrainerApp(root)
    root.mainloop()
