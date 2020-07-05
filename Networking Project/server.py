import socket

sr = socket.socket()
sr.bind((socket.gethostname(), 9999))
sr.listen(11)
print("Server Started...\n")
c, adr = sr.accept()
print("Connected with", c, adr, "\n")
c.send(bytes("Now you are connected to server(Nikhil)", "utf-8"))

while True:
    x = input("Enter a message: ")
    print("Wait for response from client")
    c.send(bytes(x, "utf-8"))
    print("\nMessage from client:", c.recv(1024).decode())
