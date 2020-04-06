import json
from flask import Flask
from flask import request
from socket import *

app = Flask(__name__)


@app.route('/register', methods=['PUT'])
def register():
    infor = request.get_json() # HTTP PUT request
    hostname = infor['hostname']
    ip = infor['ip']
    as_ip = infor['as_ip']
    as_port = infor['as_port']
    # print(hostname)
    # print(ip)
    # print(as_ip)
    # print(as_port)
    server_name = as_ip
    server_port = 53533
    fs_socket = socket(AF_INET, SOCK_DGRAM) #UDP

    dns_request = {
        'TYPE': 'A',
        'NAME': hostname,
        'VALUE': ip,
        'TTL': 10
    }
    message = json.dumps(dns_request)
    fs_socket.sendto(message.encode(), (server_name, server_port))

    # Receiver response back
    message, server_address = fs_socket.recvfrom(2048)
    # Close the socket
    fs_socket.close()
    return message.decode()


def Fibonacci(n):
    if n < 0:
        print("Incorrect Input")
        # First Fibonacci number is 0
    elif n == 1:
        return 0
    # Second Fibonacci number is 1
    elif n == 2:
        return 1
    else:
        return Fibonacci(n - 1) + Fibonacci(n - 2)


@app.route('/fibonacci', methods=['GET'])
def get_fibonacci_number():
    try:
        temp = int(request.args.get('number'))
        x = int(temp)
        if x >=0:
            return 'Fibonacci Number for the sequence number {0} is {1}, 200 OK'.format(x, Fibonacci(x))
        else:
            return 'ERROR 400'
    except:
        return 'Error 400'

app.run(host='0.0.0.0',
        port=9090,
        debug=True)
