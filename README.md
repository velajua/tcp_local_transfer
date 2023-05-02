# TCP Client-Server File Transfer
This program allows the user to send both text and files from the client (sender) to the server (receiver) via a TCP connection through a local network.

## Requirements
Python 3.x
tkinter (for GUI)

The requirements can be installed by using `pip install -r requirements.txt`

## Usage
- Run the server script on the receiving end by executing `python receiver.py` on the command line.
- Run the client script on the sending end by executing `python sender.py` on the command line.
- Enter the IP address and port number of the server (receiver) into the client GUI to establish a connection.
- To send a file, click the "Browse" button and select a file from your local machine. Then click the `Send File` checkbox and the `Submit` button to transfer the file to the server. The file will be saved in the same directory as the server script.
- To send a text message, simply type the message into the text box and click the `Submit` button. The message will be displayed in the chat window on the server side.

![sender](tcp_local_transfer/imgs/sender.png)

![receiver](tcp_local_transfer/imgs/receiver.png)

## Notes
- The default IP address used by the server is the local host (127.0.0.1).
- The default port number used is chosen at random from the available ports.
- The server script will display the received file name and the IP address and port number of the client that sent the file.
- The chat window on the server side will display the IP address and port number of the client that sent the text message, along with the message itself.
- The client script will display an error message if the connection to the server cannot be established or if the selected file cannot be sent.
