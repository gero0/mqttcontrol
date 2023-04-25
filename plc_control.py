import paho.mqtt.client as mqtt
import struct


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


def on_connect(client, userstat, flags, rc):
    print("Connected to mqtt broker!")


def main():
    out_states = [False] * PIN_CNT
    print(out_states)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect_async(HOST, PORT, KEEPALIVE)
    client.loop_start()

    while True:
        inpt = input()
        if (inpt == "h" or inpt == "help"):
            print("0-9 change pin state, s to send, r to reset states")
        elif (inpt == "s" or inpt == "S"):
            states = serialize(out_states)
            s = struct.pack('<H', states)
            print("Sending...")
            print(s)
            info = client.publish(TOPIC, s)
            info.wait_for_publish(TIMEOUT)
            print("Success:", info.is_published())
        elif (inpt == "r" or inpt == "R"):
            out_states = [False] * PIN_CNT
            print("States reset")
            print(out_states)
        elif (inpt == "a" or inpt == "A"):
            out_states = [True] * PIN_CNT
            print("Christmas tree! ^_^")
            print(out_states)
        else:
            try:
                pin = int(inpt)
                if (pin >= 0 and pin < PIN_CNT):
                    out_states[pin] = not out_states[pin]
            except:
                print("invalid input")

            print(out_states)


if __name__ == "__main__":
    main()
