import paho.mqtt.client as mqtt
import struct
from plc_control import serialize, on_connect
import tkinter as tk
import tkinter.ttk as ttk

HOST = "localhost"
PORT = 1883
TOPIC = "topic"
TIMEOUT = 2
KEEPALIVE = 60

PIN_CNT = 10

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PLC Control")
        self.geometry("500x100")
        self.resizable(False, False)

        self.out_states = [tk.BooleanVar(value=False) for _ in range(PIN_CNT)]
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.connect_async(HOST, PORT, KEEPALIVE)
        self.client.loop_start()
        self.create_widgets()

    def create_widgets(self):
        self.frm_cbs = tk.Frame(self)
        self.frm_cbs.pack(anchor=tk.CENTER)
        self.frm_grid_cbs = [tk.Frame(self.frm_cbs, border=4) for _ in self.out_states]
        for i, frm in enumerate(self.frm_grid_cbs): frm.grid(row=0, column=i)
        self.cbs_statebuttons = [tk.Checkbutton(self.frm_grid_cbs[i], variable=state, onvalue=True, offvalue=False, anchor=tk.CENTER) for i, state in enumerate(self.out_states)] # might try making these pretty LEDs later 😎
        for i, cb in enumerate(self.cbs_statebuttons): cb.grid(row=0, column=1)
        self.lbl_pinlabels = [tk.Label(self.frm_grid_cbs[i], text=str(i), anchor=tk.CENTER, justify="center") for i in range(PIN_CNT)] # having to use a nasty hack just to move labels to the bottom of the buttons, really classy tkinter 🙄
        for i, lbl in enumerate(self.lbl_pinlabels): lbl.grid(row=1, column=1) # labels don't want to be centered for some reason 😒

        self.frm_buttons = tk.Frame(self)
        self.frm_buttons.pack(anchor=tk.CENTER)

        self.btn_reset = tk.Button(self.frm_buttons, text="Reset", command=self.reset)
        self.btn_reset.grid(row=0, column=0)
        self.btn_christmas = tk.Button(self.frm_buttons, text="Christmas", command=self.christmas)
        self.btn_christmas.grid(row=0, column=1)
        self.btn_send = tk.Button(self.frm_buttons, text="Send", command=self.send)
        self.btn_send.grid(row=0, column=2)

        self.btn_debug = tk.Button(self, text="Debug", command=self.debug) # will probably be removed later
        self.btn_debug.place(x=0, y=60)

    def send(self):
        # states = serialize(self.out_states) # won't work, because these are not regular bools but some weird wrappers
        states = [state.get() for state in self.out_states]
        states = serialize(states)

        s = struct.pack('<H', states)
        info = self.client.publish(TOPIC, s)
        info.wait_for_publish(TIMEOUT)

    def reset(self):
        for state in self.out_states: state.set(False)

    def christmas(self):
        for state in self.out_states: state.set(True)

    def debug(self):
        for state in self.out_states: print(state.get(), end=' ')
        print()

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()