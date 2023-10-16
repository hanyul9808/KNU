import socket
import cv2
import threading
import tkinter as tk
from tkinter import ttk
import struct
import pickle
from PIL import Image, ImageTk

HOST = '127.0.0.1'
videoPORT = 3600
chatPORT = 3700
video_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_server_socket.bind((HOST, videoPORT))
video_server_socket.listen()

chat_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_server_socket.bind((HOST, chatPORT))
chat_server_socket.listen()

video_clients = []
chat_clients = []


vid = cv2.VideoCapture(0)

root = tk.Tk()
root.title("Combined Server")

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

def send_video_stream(client):
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
            video_clients.remove(client)

def handle_chat_client(client):
    while True:
        try:
            message = client.recv(1024).decode()
            chat_text.insert(tk.END, "Client: " + message + '\n')
        except Exception as e:
            print("클라이언트 연결이 종료되었습니다.")
            chat_clients.remove(client)
            break

def accept_video_clients():
    while True:
        client, addr = video_server_socket.accept()
        video_clients.append(client)
        video_stream_thread = threading.Thread(target=send_video_stream, args=(client,))
        video_stream_thread.start()

def accept_chat_clients():
    while True:
        client, addr = chat_server_socket.accept()
        chat_clients.append(client)
        chat_thread = threading.Thread(target=handle_chat_client, args=(client,))
        chat_thread.start()

video_accept_thread = threading.Thread(target=accept_video_clients)
video_accept_thread.start()

chat_accept_thread = threading.Thread(target=accept_chat_clients)
chat_accept_thread.start()

def send_chat_message():
    message = chat_entry.get()
    for client in chat_clients:
        try:
            client.send(message.encode())
        except:
            print("클라이언트 연결이 종료되었습니다.")
            chat_clients.remove(client)
    chat_text.insert(tk.END, "Server: " + message + '\n')
    chat_entry.delete(0, tk.END)

send_chat_button = tk.Button(chat_frame, text="메시지 전송", command=send_chat_message)
send_chat_button.pack()

root.mainloop()
