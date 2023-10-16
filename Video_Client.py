import socket
import cv2
import threading
import tkinter as tk
from tkinter import ttk
import struct
import pickle
from PIL import Image, ImageTk

# 서버 설정
SERVER_HOST = '127.0.0.1'
VIDEO_PORT = 3600
CHAT_PORT = 3700

# tkinter 설정
root = tk.Tk()
root.title("Combined Client")

main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=0)

video_frame = ttk.LabelFrame(main_frame, text="Video Streaming")
video_frame.grid(row=0, column=0)

video_label = ttk.Label(video_frame)
video_label.pack()

chat_frame = ttk.LabelFrame(main_frame, text="Chat")
chat_frame.grid(row=0, column=1)

chat_text = tk.Text(chat_frame, height=15, width=50)
chat_text.pack()

chat_entry = tk.Entry(chat_frame, width=50)
chat_entry.pack()

def receive_video_stream():
    video_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    video_client_socket.connect((SERVER_HOST, VIDEO_PORT))

    data = b""
    payload_size = struct.calcsize("Q")
    
    while True:
        while len(data) < payload_size:
            data += video_client_socket.recv(4096)
            
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += video_client_socket.recv(4096)
            
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        video_label.config(image=photo)
        video_label.image = photo

def send_chat_message():
    message = chat_entry.get()
    chat_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_client_socket.connect((SERVER_HOST, CHAT_PORT))
    chat_client_socket.send(message.encode())
    chat_text.insert(tk.END, "Client: " + message + '\n')
    chat_entry.delete(0, tk.END)
    chat_client_socket.close()

def receive_chat_messages():
    chat_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_client_socket.connect((SERVER_HOST, CHAT_PORT))
    
    while True:
        message = chat_client_socket.recv(1024).decode()
        chat_text.insert(tk.END, "Server: " + message + '\n')

video_thread = threading.Thread(target=receive_video_stream)
video_thread.start()

chat_receive_thread = threading.Thread(target=receive_chat_messages)
chat_receive_thread.start()

send_chat_button = tk.Button(chat_frame, text="메시지 전송", command=send_chat_message)
send_chat_button.pack()

root.mainloop()
