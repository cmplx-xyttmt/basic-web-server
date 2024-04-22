# Uncomment this to pass the first stage
import socket


def create_http_response(status, content):
    headers = (f"HTTP/1.1 {status}\r\n"
               f"Content-Type: text/plain\r\n"
               f"Content-Length: {len(content)}\r\n")
    response = f"{headers}\r\n{content}\r\n"
    return response

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    acc_socket, addr_info = server_socket.accept()  # wait for client

    request = acc_socket.recv(1024)
    lines = request.decode().split("\r\n")
    method, path, protocol = lines[0].split(" ")
    if path == "/":
        response_status = "200 OK"
        headers = f"HTTP/1.1 {response_status}\r\n\r\n"
        response = headers
    elif path.startswith("/echo"):
        path_parts = path.split("/echo/")
        response = create_http_response("200 OK", path_parts[1])
    elif path.startswith("/user-agent"):
        agent = None
        for line in lines:
            if line.startswith("User-Agent:"):
                agent = line.removeprefix("User-Agent: ")
                break
        response = create_http_response("200 OK", agent)
    else:
        response_status = "404 Not Found"
        headers = f"HTTP/1.1 {response_status}\r\n\r\n"
        response = headers
    acc_socket.send(response.encode())
    acc_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
