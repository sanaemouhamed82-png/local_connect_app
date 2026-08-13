from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import socket
import json

class LocalConnectUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        
        self.add_widget(Label(text="Local Connect Phone", font_size='20sp', bold=True))
        
        self.ip_input = TextInput(text="192.168.0.190", multiline=False, size_hint_y=None, height=100)
        self.add_widget(self.ip_input)
        
        self.btn_connect = Button(text="Connect to PC", size_hint_y=None, height=100)
        self.btn_connect.bind(on_press=self.connect_to_pc)
        self.add_widget(self.btn_connect)
        
        self.btn_call = Button(text="Trigger Call", size_hint_y=None, height=100)
        self.btn_call.bind(on_press=self.trigger_call)
        self.add_widget(self.btn_call)
        
        self.status_label = Label(text="Disconnected")
        self.add_widget(self.status_label)
        
        self.sock = None
        self.connected = False

    def connect_to_pc(self, instance):
        ip = self.ip_input.text.strip()
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, 5000))
            self.connected = True
            self.status_label.text = "Connected to PC"
        except Exception as e:
            self.status_label.text = f"Error: {e}"

    def trigger_call(self, instance):
        if self.connected and self.sock:
            pkt = {"type": "INCOMING_CALL", "from": "Android"}
            self.sock.sendall(json.dumps(pkt).encode('utf-8'))

class LocalConnectApp(App):
    def build(self):
        return LocalConnectUI()

if __name__ == '__main__':
    LocalConnectApp().run()
