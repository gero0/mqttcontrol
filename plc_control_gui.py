import paho.mqtt.client as mqtt
import struct
import tkinter as tk

HOST = "localhost"
PORT = 1883
TOPIC = "topic"
TIMEOUT = 2
KEEPALIVE = 60

PIN_CNT = 10

def serialize(states):
    number = 0
    for i in range(PIN_CNT):
        if (states[i]):
            number |= (1 << i)
    return number

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PLC Control")
        self.geometry("400x125")
        self.resizable(False, False)

        self.out_states = [tk.BooleanVar(value=False) for _ in range(PIN_CNT)]
        self.client = mqtt.Client()
        self.client.connect_async(HOST, PORT, KEEPALIVE)
        self.client.loop_start()
        self.create_widgets()

    def create_widgets(self):
        self.frm_cbs = tk.Frame(self)
        self.frm_cbs.pack(anchor=tk.CENTER)
        self.frm_grid_cbs = [tk.Frame(self.frm_cbs, border=4) for _ in self.out_states]
        for i, frm in enumerate(self.frm_grid_cbs): frm.grid(row=0, column=i)
        self.cbs_statebuttons = [tk.Checkbutton(self.frm_grid_cbs[i], variable=state, onvalue=True, offvalue=False, anchor=tk.CENTER) for i, state in enumerate(self.out_states)]
        for i, cb in enumerate(self.cbs_statebuttons): cb.grid(row=0, column=1)
        self.lbl_pinlabels = [tk.Label(self.frm_grid_cbs[i], text=str(i), anchor=tk.CENTER, justify="center") for i in range(PIN_CNT)]
        for i, lbl in enumerate(self.lbl_pinlabels): lbl.grid(row=1, column=1)

        self.frm_buttons = tk.Frame(self)
        self.frm_buttons.pack(anchor=tk.CENTER)

        self.btn_reset = tk.Button(self.frm_buttons, text="Reset", command=self.reset)
        self.btn_reset.grid(row=0, column=0)
        self.btn_christmas = tk.Button(self.frm_buttons, text="Christmas", command=self.christmas)
        self.btn_christmas.grid(row=0, column=1)
        self.btn_send = tk.Button(self.frm_buttons, text="Send", command=self.send)
        self.btn_send.grid(row=0, column=2)

        self.frm_status = tk.Frame(self)
        self.frm_status.pack(anchor=tk.W, padx=10, pady=5)
        self.lbl_status = tk.Label(self.frm_status, text='')
        self.lbl_status.pack()

    def send(self):
        states = [state.get() for state in self.out_states]
        states = serialize(states)

        s = struct.pack('<H', states)
        info = self.client.publish(TOPIC, s)
        info.wait_for_publish(TIMEOUT)
        self.lbl_status.config(text='Sending...')
        if info.is_published():
            self.lbl_status.config(text='Sent successfully')
        else:
            self.lbl_status.config(text='Sending failed!!')

    def reset(self):
        for state in self.out_states: state.set(False)
        self.lbl_status.config(text='States reset')

    def christmas(self):
        for state in self.out_states: state.set(True)
        self.lbl_status.config(text='Christmas tree! ^_^')

    def debug(self):
        for state in self.out_states: print(state.get(), end=' ')
        print()

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()