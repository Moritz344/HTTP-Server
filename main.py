import socket
import threading
import os
import argparse

def handle_client(client_socket, directory):
    with client_socket:
        request = client_socket.recv(1024).decode("utf-8")
        print(f"Request: {request}")

        if not request:
            return

        request_lines = request.split('\r\n')
        request_line = request_lines[0]
        print(f"Request line: {request_lines}")

        method, path, http_version = request_line.split()[:3]

        user_agent = None
        for line in request_lines:
            if line.startswith("User-Agent:"):
                user_agent = line[len("User-Agent: "):]

        if method == "GET":
            if path.startswith("/echo/"):
                echo_string = path[len("/echo/"):]
                print(f"Echo string: {echo_string}")
                http_response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: {len(echo_string)}\r\n"
                    f"\r\n"
                    f"{echo_string}"
                )
            elif path == "/":
                http_response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: 2\r\n"
                    "\r\n"
                    "OK"
                )
            elif path == "/user-agent" and user_agent:
                http_response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    f"Content-Length: {len(user_agent)}\r\n"
                    "\r\n"
                    f"{user_agent}"
                )
            elif path.startswith("/files/"):
                filename = path[len("/files/"):]
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    with open(file_path, "rb") as f:
                        file_content = f.read()

                    http_response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: application/octet-stream\r\n"
                        f"Content-Length: {len(file_content)}\r\n"
                        "\r\n"
                    )

                    client_socket.sendall(http_response.encode("utf-8"))
                    client_socket.sendall(file_content)
                else:
                    not_found_message = "404 Not Found"
                    http_response = (
                        "HTTP/1.1 404 Not Found\r\n"
                        "Content-Type: text/plain\r\n"
                        f"Content-Length: {len(not_found_message)}\r\n"
                        "\r\n"
                        f"{not_found_message}"
                    )
                    client_socket.sendall(http_response.encode("utf-8"))
            else:
                not_found_message = "404 Not Found"
                http_response = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/plain\r\n"
                    f"Content-Length: {len(not_found_message)}\r\n"
                    "\r\n"
                    f"{not_found_message}"
                )
        elif method == "POST" and path.startswith("/files/"):
            # extract the filename and create the full path
            filename = path.split("/files/")[1]
            file_path = os.path.join(directory,filename)

            content_index = request.find("\r\n\r\n") + 4
            file_content = request[content_index:]

            # Write the body to the specified file
            os.makedirs(os.path.dirname(file_path),exist_ok=True)
            with open(file_path,"w") as file:
                file.write(file_content)
            
            http_response = "HTTP/1.1 201 Created\r\n\r\n"
            
            client_socket.sendall(http_response.encode("utf-8"))
        else:
            not_implemented_message = "501 Not Implemented"
            http_response = (
                "HTTP/1.1 501 Not Implemented\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(not_implemented_message)}\r\n"
                "\r\n"
                f"{not_implemented_message}"
            )
        

        client_socket.sendall(http_response.encode("utf-8"))

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Simple HTTP Server")
    parser.add_argument('--directory', help="Directory to serve files from")
    args = parser.parse_args()
    directory = args.directory or os.getcwd()

    print(f"Starting the server, serving files from: {directory}")

    # Create a TCP socket and bind it to localhost on port 4221
    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen()

    print("Server is listening on localhost:4221")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Create a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, directory))
        client_thread.start()

if __name__ == "__main__":
    main()
