import socket
import cv2
import threading
import tkinter as tk
from tkinter import ttk
import struct
import pickle
from PIL import Image, ImageTk

# 서버 설정
HOST = '127.0.0.1'
VPORT = 3600 
CPORT = 3700 

root = tk.Tk()
root.title("시청자 클라이언트")

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


def Re_video():
    Vsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Vsocket.connect((HOST, VPORT))

    data = b""
    loadsize = struct.calcsize("Q")
    
    while True:
        while len(data) < loadsize:
            data += Vsocket.recv(4096)
            
        msg_size = data[:loadsize]
        data = data[loadsize:]
        msg_size = struct.unpack("Q", msg_size)[0]
        
        while len(data) < msg_size:
            data += Vsocket.recv(4096)
            
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        video_label.config(image=photo)
        video_label.image = photo

def send_message():
    message = entry.get()

    Csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Csocket.connect((HOST, CPORT))
    Csocket.send(message.encode())
    chat.insert(tk.END, "클라이언트: " + message + '\n')
    entry.delete(0, tk.END)
    Csocket.close()

def Re_message():
    Csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Csocket.connect((HOST, CPORT))
    
    while True:
        message = Csocket.recv(1024).decode()
        chat.insert(tk.END, "서버: " + message + '\n')

Vthread = threading.Thread(target=Re_video)
Vthread.start()

Cthread = threading.Thread(target=Re_message)
Cthread.start()

button = tk.Button(Cframe, text="메시지 전송", command=send_message)
button.pack()

root.mainloop()
