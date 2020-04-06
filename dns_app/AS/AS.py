from socket import *
import json
from socket import *

server_port = 53533

# Create a socket (UDP)
as_socket = socket(AF_INET, SOCK_DGRAM)

# Bind to port
as_socket.bind(('', server_port))

# Now listen to FS or US
while True:
    # Receive message
    message, client_address = as_socket.recvfrom(2048)
    temp= message.decode()
    dict = json.loads(temp)
    print(dict)
    print(len(dict))
    # Now we need to check the source (from US or FS) of the message.
    if len(dict) == 4: # If the message is sent from FS
        try:
            with open('infor.txt', 'w') as outfile:
                json.dump(dict, outfile)
            message = '201'
        except:
            message = 'ERROR: Write to File Failed'
    elif len(dict) == 2: # If the message is sent from US
        try:
            file = open("infor.txt", 'r', encoding='utf-8')
            for line in file.readlines():
                data = json.loads(line)
                if dict['TYPE'] == data['TYPE'] and dict['NAME'] == data['NAME']:
                    message = json.dumps(data)
                else:
                    message = 'ERROR: The hostname has not been registered'
        except:
            message = 'ERROR: Read File Failed'
    else:
        message ='ERROR!'

    as_socket.sendto(message.encode(), client_address)

