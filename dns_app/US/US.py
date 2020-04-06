from flask import Flask
from flask import request
import json
from socket import *
from urllib.request import urlopen

app = Flask(__name__)


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname=request.args.get('hostname')
    fs_port=request.args.get('fs_port')
    number=request.args.get('number')
    as_ip=request.args.get('as_ip')
    as_port=request.args.get('as_port')

    if not hostname or not fs_port or not number or not as_ip or not as_port:
        return '400'

    else:
        ip_request = {
        'TYPE': 'A',
        'NAME': hostname
        }
        server_name = as_ip
        server_port = 53533
        message = json.dumps(ip_request)
        us_socket = socket(AF_INET, SOCK_DGRAM)
        us_socket.sendto(message.encode(), (server_name, server_port))
        # Receiver response back
        response, server_address = us_socket.recvfrom(2048)
        # get the information - json object
        temp = response.decode()
        infor = json.loads(temp)
        ip_address = infor['VALUE']
        # Close the socket
        us_socket.close()
        html='http://{}:{}/fibonacci?number={}'.format(ip_address,fs_port,number)
        link = urlopen(html)
        myfile = link.read()
        return myfile

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
