import tkinter as tk
from tkinter import messagebox
import socket
import json
import threading

class PhoneClientApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Local Connect - Phone")
        self.geometry("400x600")
        self.configure(bg="#11111b")

        self.sock = None
        self.connected = False

        # Header Title
        tk.Label(
            self, 
            text="📱 تطبيق الاتصال الهاتفي", 
            font=("Segoe UI", 14, "bold"), 
            fg="#cdd6f4", 
            bg="#11111b"
        ).pack(pady=15)

        # IP Input Box
        ip_frame = tk.Frame(self, bg="#11111b")
        ip_frame.pack(pady=10)
        
        tk.Label(ip_frame, text="IP الكمبيوتر:", fg="#cdd6f4", bg="#11111b", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.ip_entry = tk.Entry(ip_frame, font=("Segoe UI", 11), width=15)
        self.ip_entry.insert(0, "192.168.0.190")
        self.ip_entry.pack(side=tk.LEFT, padx=5)

        self.btn_connect = tk.Button(
            self, 
            text="اتصال بالكمبيوتر 🔗", 
            bg="#89b4fa", 
            fg="#11111b", 
            font=("Segoe UI", 10, "bold"), 
            command=self.connect_to_pc
        )
        self.btn_connect.pack(pady=10)

        # Control Box
        actions_box = tk.LabelFrame(
            self, 
            text="التحكم بالمكالمات والرسائل", 
            fg="#89b4fa", 
            bg="#11111b", 
            font=("Segoe UI", 11, "bold")
        )
        actions_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Trigger Call
        tk.Button(
            actions_box, 
            text="📞 إجراء مكالمة للكمبيوتر", 
            bg="#a6e3a1", 
            fg="#11111b", 
            font=("Segoe UI", 11, "bold"), 
            padx=10, 
            pady=8, 
            command=self.trigger_call
        ).pack(fill=tk.X, padx=15, pady=10)

        # Chat Area
        self.chat = tk.Text(actions_box, bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 10), height=10)
        self.chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        msg_f = tk.Frame(actions_box, bg="#11111b")
        msg_f.pack(fill=tk.X, padx=10, pady=10)
        self.msg_entry = tk.Entry(msg_f, font=("Segoe UI", 10))
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Button(msg_f, text="إرسال", bg="#89b4fa", fg="#11111b", command=self.send_msg).pack(side=tk.RIGHT)

    def connect_to_pc(self):
        ip = self.ip_entry.get().strip()
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, 5000))
            self.connected = True
            self.btn_connect.config(text="🟢 متصل بالكمبيوتر", bg="#a6e3a1")
            threading.Thread(target=self.listen_pc, daemon=True).start()
            messagebox.showinfo("نجاح", "تم الاتصال بالكمبيوتر بنجاح!")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل الاتصال بـ {ip}: {e}")

    def trigger_call(self):
        if not self.connected:
            messagebox.showwarning("تنبيه", "قم بالاتصال بالكمبيوتر أولاً!")
            return
        pkt = {"type": "INCOMING_CALL", "from": "هاتف أندرويد"}
        self.sock.sendall(json.dumps(pkt).encode('utf-8'))

    def send_msg(self):
        txt = self.msg_entry.get().strip()
        if not txt or not self.connected:
            return
        pkt = {"type": "SMS_RECEIVED", "from": "الهاتف", "body": txt}
        self.sock.sendall(json.dumps(pkt).encode('utf-8'))
        self.chat.insert(tk.END, f"أنا: {txt}\n")
        self.msg_entry.delete(0, tk.END)

    def listen_pc(self):
        while self.connected:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                pkt = json.loads(data.decode('utf-8'))
                if pkt.get("type") == "SMS_SEND":
                    body = pkt.get("body", "")
                    self.chat.insert(tk.END, f"💻 الكمبيوتر: {body}\n")
            except Exception:
                break

if __name__ == "__main__":
    app = PhoneClientApp()
    app.mainloop()
