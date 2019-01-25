
import socketserver
class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):

        # Receive the request
        self.data = self.request.recv(1024).strip()
        self.data_tokens = self.data.decode().split()

        # Initialize mime type and response code
        self.mime = ""
        self.response_code = ""

        # Check if request is a GET
        try:
            self.response_type = self.data_tokens.index("GET")
            self.response_content = self.data_tokens[self.response_type+1]

        # If not a GET method, then not allowed - display 405 error
        except:
            self.response_code = "405 Method Not Allowed"
            self.mime = "text/html"
            self.page = "<html><body><h1>405 Method Not Allowed</h1></body></html>"

        try:
            # Set index.html if ends in /
            if (self.response_content[-1] == "/"):
                self.response_content += "index.html"

            # Check if HTML or CSS and set respective mime type
            if (len(self.response_content.split(".")) == 2):
                if (self.response_content.split(".")[1] == "html"):
                    self.mime = "text/html"
                if (self.response_content.split(".")[1] == "css"):
                    self.mime = "text/css"

            # Read Requested file
            with open("www" + self.response_content, "r") as f:
                self.page = f.read()

        except:
            # 404 error
            self.response_code = "404 Not Found"
            self.mime = "text/html"
            self.page = "<html><body><h1>404 Not Found</h1></body></html>"

        # Send request
        self.display = "HTTP/1.1 %s\nContent-Type: %s\r\n\r\n%s" % (self.response_code, self.mime, self.page)
        self.request.sendall(bytearray(self.display,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
