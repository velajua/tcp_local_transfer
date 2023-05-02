import os
import socket
import tkinter as tk
from tkinter import filedialog, messagebox

from datetime import date

# Define the address and port of the receiving machine
receiver_address = '127.0.0.1'

# Create a socket object

# Define a function to handle the "submit" button press
def submit():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Validate the IP address
    receiver_address = receiver_address_var.get()
    try:
        socket.inet_aton(receiver_address)
    except socket.error:
        messagebox.showerror("Error", "Invalid IP address")
        return

    # Get the message to send
    message = chat_input.get("1.0", tk.END).strip()
    

    # Check if file checkbox is selected
    if send_file_var.get() == 1:
        # Get the selected file path
        file_path = file_path_var.get()

        # Check if file path is valid
        if not os.path.isfile(file_path):
            messagebox.showerror("Error", "Invalid file path")
            return

        # Get the current date
        current_date = str(date.today())

        # Connect to the receiving machine
        try:
            sock.connect((receiver_address, int(receiver_port_var.get())))
        except socket.error:
            messagebox.showerror("Error", "Connection error")
            return

        # Send the file contents over the socket
        with open(file_path, 'rb') as f:
            data = f.read()
            # Send the file name and date
            sock.sendall(f"{os.path.basename(file_path)}|{current_date}".encode())
            # Send the file data
            sock.sendall(data)

        # Update the error label
        messagebox.showinfo("Success", "File sent successfully")
    elif message:
        # Connect to the receiving machine
        try:
            sock.connect((receiver_address, int(receiver_port_var.get())))
        except socket.error:
            messagebox.showerror("Error", "Connection error")
            return

        # Send the message over the socket
        sock.sendall(message.encode())
        chat_output.config(state=tk.NORMAL)
        chat_output.insert(tk.END, sock.recv(1024).decode() + '\n')
        chat_output.config(state=tk.DISABLED)        
        
        if 'ENDZZZ' in message:
            sock.close()
            root.quit()
            exit()

# Create a Tkinter window
root = tk.Tk()
root.title("Chat and File Sender")

# Create a label for the file path
file_path_label = tk.Label(root, text="File path:")
file_path_label.pack()
file_path_var = tk.StringVar()
file_path_entry = tk.Entry(root, textvariable=file_path_var)
file_path_entry.pack()

# Create a "browse" button to select the file
def browse():
    file_path = filedialog.askopenfilename()
    file_path_var.set(file_path)

browse_button = tk.Button(root, text="Browse", command=browse)
browse_button.pack()

# Create a label for the IP address
receiver_address_label = tk.Label(root, text="Receiver IP address:")
receiver_address_label.pack()
receiver_address_var = tk.StringVar()
receiver_address_entry = tk.Entry(root, textvariable=receiver_address_var)
receiver_address_entry.pack()

receiver_port_label = tk.Label(root, text="Receiver IP port:")
receiver_port_label.pack()
receiver_port_var = tk.StringVar()
receiver_port_entry = tk.Entry(root, textvariable=receiver_port_var)
receiver_port_entry.pack()

# Create a checkbox to send a file
send_file_var = tk.IntVar()
send_file_checkbox = tk.Checkbutton(root, text="Send file", variable=send_file_var)
send_file_checkbox.pack()

# Create a chat window
chat_output = tk.Text(root)
chat_output.pack()
chat_output.config(state=tk.DISABLED)

# Create a scrollbar for the chat window
scrollbar = tk.Scrollbar(root, command=chat_output.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_output.config(yscrollcommand=scrollbar.set)

# Create a label for the chat input
chat_input_label = tk.Label(root, text="Message:")
chat_input_label.pack()

# Create a chat input box
chat_input = tk.Text(root, height=3)
chat_input.pack()

# Create a "submit" button to send the message or file
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

# Run the Tkinter event loop
root.mainloop()
