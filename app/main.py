# Uncomment this to pass the first stage
import os
import socket
import sys
import threading
from pathlib import Path


def create_http_response(status, content_type, content):
    headers = (f"HTTP/1.1 {status}\r\n"
               f"Content-Type: {content_type}\r\n"
               f"Content-Length: {len(content)}\r\n")
    response = f"{headers}\r\n{content}\r\n"
    return response

def not_found_response():
    response_status = "404 Not Found"
    headers = f"HTTP/1.1 {response_status}\r\n\r\n"
    return headers

def handle_client_connection(acc_socket, _acc_addr_info, directory_name):
    request = acc_socket.recv(1024)
    lines = request.decode().split("\r\n")
    method, path, protocol = lines[0].split(" ")
    if path == "/":
        response_status = "200 OK"
        headers = f"HTTP/1.1 {response_status}\r\n\r\n"
        response = headers
    elif path.startswith("/echo"):
        path_parts = path.split("/echo/")
        response = create_http_response("200 OK", "text/plain", path_parts[1])
    elif path.startswith("/user-agent"):
        agent = None
        for line in lines:
            if line.startswith("User-Agent:"):
                agent = line.removeprefix("User-Agent: ")
                break
        response = create_http_response("200 OK", "text/plain", agent)
    elif path.startswith("/files/"):
        filename = path.removeprefix("/files/")
        if directory_name and Path(directory_name).is_dir() and Path(f"{directory_name}/{filename}").is_file():
            file = Path(f"{directory_name}/{filename}")
            with open(file, 'r') as content:
                response = create_http_response("200 OK", "application/octet-stream", content.read())
        else:
            response = not_found_response()
    else:
        response = not_found_response()
    acc_socket.send(response.encode())
    acc_socket.close()


def main(directory_name=None):
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print(f"Logs from your program will appear here!.")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    try:
        while True:
            acc_socket, addr_info = server_socket.accept()  # wait for client
            threading.Thread(target=handle_client_connection, args=(acc_socket, addr_info, directory_name)).start()
    except KeyboardInterrupt:
        server_socket.close()
        sys.exit(0)


if __name__ == "__main__":
    _directory_name = None
    if len(sys.argv) > 1:
        flag = sys.argv[1]
        if flag == "--directory":
            if len(sys.argv) > 2:
                _directory_name = sys.argv[2]
            else:
                print("Please specify a directory name.")
    print(_directory_name)
    main(_directory_name)
