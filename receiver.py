import socket
import os
import tkinter as tk
import threading
import traceback

# Define the IP address and port number to bind the socket to
IP_ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 0

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP address and port number
server_socket.bind((IP_ADDRESS, PORT))
PORT = server_socket.getsockname()[1]

# Listen for incoming connections
server_socket.listen()

print(f'Server listening on {IP_ADDRESS}:{PORT}...')

# Create a Tkinter window
root = tk.Tk()
root.title("Chat and File Receiver")

# Create a label to show the received file name
file_name_var = tk.StringVar()
file_name_label = tk.Label(root, textvariable=file_name_var)
file_name_label.pack()

# Create a chat window
chat_output = tk.Text(root)
chat_output.pack()
chat_output.config(state=tk.DISABLED)

# Create a scrollbar for the chat window
scrollbar = tk.Scrollbar(root, command=chat_output.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_output.config(yscrollcommand=scrollbar.set)
chat_output.config(state=tk.NORMAL)
chat_output.insert(tk.END, f'Server listening on {IP_ADDRESS}:{PORT}...\n')
chat_output.config(state=tk.DISABLED)

client_socket = None

def handle_connection():
    global client_socket
    connection_finished = False
    while not connection_finished:
        try:
            # Accept incoming connection
            client_socket, client_address = server_socket.accept()
            print(f'Connection from {client_address[0]}:{client_address[1]}')

            # Receive message from client
            data = client_socket.recv(1024).decode()

            # Check if the received data is a file
            if "|" in data:
                # Received file name and date from client
                file_name, current_date = data.split("|")

                # Append the current date to the file name
                file_name = os.path.splitext(file_name)[0] + "_" + current_date + os.path.splitext(file_name)[1]

                # Open file for writing
                with open(file_name, 'wb') as file:
                    # Receive file data from client
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        file.write(data)

                print(f'Received file "{file_name}" from {client_address[0]}:{client_address[1]}')

                # Update the file name label
                file_name_var.set(f'Received file "{file_name}" from {client_address[0]}:{client_address[1]}')
            elif data:
                # Received text message from client
                message = f'{client_address[0]}:{client_address[1]} - {data}'

                # Append the message to the chat window
                chat_output.config(state=tk.NORMAL)
                chat_output.insert(tk.END, message + '\n')
                chat_output.config(state=tk.DISABLED)
                chat_output.see(tk.END)
                client_socket.sendall(f'Sent - {client_address[0]}:{client_address[1]} - {data}'.encode())

                # Check if the message is "ENDZZZ"
                if 'ENDZZZ' in message:
                    connection_finished = True

                    # Close the client socket
                    client_socket.close()

                    # Stop the Tkinter event loop
                    root.quit()

                    # Close the server socket
                    server_socket.close()

                    # Wait for all threads to complete
                    for t in threading.enumerate():
                        if t != threading.current_thread():
                            t.join()
        except Exception:
            print(traceback.format_exc())
            connection_finished = True
            if client_socket:
                client_socket.close()
            # Stop the Tkinter event loop
            root.quit()

            # # Close the server socket
            server_socket.close()

# Start a new thread to handle incoming connections
connection_thread = threading.Thread(target=handle_connection)
connection_thread.start()

def on_closing():
    server_socket.close()
    for t in threading.enumerate():
        if t != threading.current_thread():
            t.join()
    root.quit()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the Tkinter event loop
root.mainloop()
