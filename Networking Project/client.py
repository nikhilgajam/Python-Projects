import socket

cl = socket.socket()
cl.connect((socket.gethostname(), 9999))

print("Client Started...\n")
msg = cl.recv(1024)
print(msg.decode(), "\n")

while True:
    msg = cl.recv(1024)
    print("Message from server(Nikhil):", msg.decode())
    x = input("Enter a message: ")
    cl.send(bytes(x, "utf-8"))
    print("Wait for response from server(Nikhil)\n")
