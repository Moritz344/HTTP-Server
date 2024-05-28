# Simple HTTP Server

This project is a basic multi-threaded HTTP server implemented in Python. It can handle simple HTTP GET and POST requests and serves files from a specified directory. The server supports echoing strings, returning the user agent, serving files, and creating files via POST requests.

# Features
GET Requests:
-  /echo/<string>: Returns the string <string> in the response body.
-  /: Returns a simple "OK" message.
-  /user-agent: Returns the user agent string of the client making the request.
-  /files/<filename>: Returns the content of the file <filename> from the specified directory if it exists.

POST Requests
- files/filename: Accepts a file upload and saves the content to <filename> in the specified directory.

# Requirements
- Python 3.6 or higher

# Usage
# Command-Line Arguments
--directory: The directory from which to serve files. If not specified, the current working directory is used.
Running the Server
Clone the repository or copy the server script to your local machine.
Open a terminal and navigate to the directory containing the script.
Run the server with the following command:
```
python3 main.py --directory files
```
# Testing the Server
POST Request Example
The HTTP server can create a .txt file in the specified directory.

```
python3 main.py --directory files
```

```
curl -vvv -d "hello world" localhost:4221/files/readme.txt
```
# GET Request Examples
```
python3 main.py 
```

```
curl -i -X GET http://localhost:4221/
```
Response:

```
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 2

OK
```

Make a GET request to an existing file in the specified directory:


```
python3 main.py --directory files
curl -i -X GET http://localhost:4221/files/index.html
```

# How
I did this project with codecrafters which is really good if you do not know what to code.


