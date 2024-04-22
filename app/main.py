# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    acc_socket, addr_info = server_socket.accept() # wait for client

    request = acc_socket.recv(1024)
    lines = request.decode().split("\r\n")
    method, path, protocol = lines[0].split(" ")
    if path == "/":
        response_status = "200 OK"
    else:
        response_status = "404 Not Found"
    acc_socket.send(f"HTTP/1.1 {response_status}\r\n\r\n".encode())
    acc_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
