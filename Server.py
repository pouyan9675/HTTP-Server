import os
import socket

host = ''
port = 5000
list_dir = 'files'     # Server files

def files_list():
    server_response_content = "<html><head><title>HTTP Server</title>"
    server_response_content += "</head>"
    server_response_content += "<body><h1>Server List<h1><br>"
    server_response_content += "<h2>Name</h2><hr>"
    server_response_content += "<ul>"

    all_files = os.listdir(list_dir + "/")
    for file in all_files:
        file_name = os.path.basename(file)
        if not os.path.isfile(list_dir + "/" + file_name):
            file_name += '/'
        server_response_content += '<li><a href="/' + file_name + '">' + file_name + '</a></li><br>'
    server_response_content += '</ul><hr><br></body></html>'
    return server_response_content.encode()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Starting server with --> ", host, ":", port)
    s.bind((host, port))
    print("Server bind port : ", port)
    while True:
        s.listen(3)
        print('Clients now can connect...')
        connection, address = s.accept()

        print('New Connection : ', address)
        with connection:
            req = connection.recv(1024)
            request_content = bytes.decode(req)
            request_type = request_content.split(' ')[0]
            print("Method is : ", request_type)
            print("Request body is : ", request_content)

            if (request_type == 'GET') | (request_type == 'HEAD'):
                request_file = request_content.split(' ')
                request_file = request_file[1]

            browsing_root = False
            if request_file is not None and request_file == '/':
                request_file = '/index.html'
                browsing_root = True

            request_file = list_dir + request_file
            print("Request for  file : ", request_file)

            try:
                file_h = open(request_file, 'rb')
                if request_type == 'GET':
                    response_content = file_h.read()  # read file content
                file_h.close()

                response_header = 'HTTP/1.1 200 OK\n'

            except Exception as e:

                if not browsing_root:
                    print("Error 404 File not Found!! \n", e)
                    response_header = 'HTTP/1.1 404 NOT FOUND\n'

                    if request_type == 'GET':
                        response_content = b"""<html><body>
                        <h1 style="font-size: 4em;">Error 404 File not found!!</h1>
                        </body></html>"""

                else:
                    response_header = 'HTTP/1.1 200 OK\n'
                    response_content = files_list()

            response_header += 'Server: Python-HTTP-Server \n'
            response_header += 'Connection: close\n\n'

            server_response = response_header.encode()
            if request_type == 'GET':
                server_response += response_content

            connection.send(server_response)
            print("Client disconnect")
