import socket
import cv2
import threading
import tkinter as tk
from tkinter import ttk
import struct
import pickle
from PIL import Image, ImageTk

HOST = '127.0.0.1'
Vport = 3600
Cport = 3700


Vsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Vsocket.bind((HOST, Vport))
Vsocket.listen()

Csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Csocket.bind((HOST, Cport))
Csocket.listen()

Vclient = []
Cclient = []


vid = cv2.VideoCapture(0)

root = tk.Tk()
root.title("서버")

main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=0)

Vframe = ttk.LabelFrame(main_frame, text="비디오")
Vframe.grid(row=0, column=0)

video_label = ttk.Label(Vframe)
video_label.pack()

Cframe = ttk.LabelFrame(main_frame, text="채팅")
Cframe.grid(row=0, column=1)

chat = tk.Text(Cframe, height=15, width=50)
chat.pack()

entry = tk.Entry(Cframe, width=50)
entry.pack()

def Cap_video(client):
    while True:
        ret, frame = vid.read()
        frame_bytes = pickle.dumps(frame)
        msg = struct.pack("Q", len(frame_bytes)) + frame_bytes
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        video_label.config(image=photo)
        video_label.image = photo
        try:
            client.sendall(msg)
        except:
            print("클라이언트 연결이 종료되었습니다.")
            Vclient.remove(client)

def handle_chat(client):
    while True:
        try:
            message = client.recv(1024).decode()
            chat.insert(tk.END, "Client: " + message + '\n')
        except Exception as e:
            print("클라이언트 연결이 종료되었습니다.")
            Cclient.remove(client)
            break

def accept_video():
    while True:
        client, addr = Vsocket.accept()
        Vclient.append(client)
        video_stream_thread = threading.Thread(target=Cap_video, args=(client,))
        video_stream_thread.start()

def accept_chat():
    while True:
        client, addr = Csocket.accept()
        Cclient.append(client)
        chat_thread = threading.Thread(target=handle_chat, args=(client,))
        chat_thread.start()

vthread = threading.Thread(target=accept_video)
vthread.start()

chat_thread = threading.Thread(target=accept_chat)
chat_thread.start()

def send_message():
    message = entry.get()
    for client in Cclient:
        try:
            client.send(message.encode())
        except:
            Cclient.remove(client)
    chat.insert(tk.END, "서버: " + message + '\n')
    entry.delete(0, tk.END)

button = tk.Button(Cframe, text="메시지 전송", command=send_message)
button.pack()

root.mainloop()
