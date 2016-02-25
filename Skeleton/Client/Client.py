# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

legal_requests = ['login', 'logout', 'msg', 'names', 'help']

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host;
        self.port = server_port;

        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.port))

        self.connected = True

        self.msg_parser = MessageParser()
        self.msg_receiver = MessageReceiver(self, self.connection)
        self.msg_receiver.start()

        while self.connected:
            inp = raw_input("command <content>:\n").split()
            command = inp[0]
            if command not in legal_requests:
                print("please type a legal command")
                continue

            content = None
            if command == 'login' or command == 'msg':
                if len(inp) <= 1:
                    print("please type <content>")
                    continue
                content = " ".join(inp[1:])

            data = {
                    'request': command,
                    'content': content}

            self.send_payload(json.dumps(data))

        self.msg_receiver.join()

    def disconnect(self):
        print("disconnected from server")
        self.connected = False

    def receive_message(self, message):
        message = self.msg_parser.parse(message)

        try:
            response = message['response']
            content = message['content']
        except:
            print "error"
            print message
            return

        if response == 'error':
            print content
        elif response == 'history':
            for chat_entry in content:
                print(chat_entry['sender'] + ":" + chat_entry['content'])
        elif response == 'message':
            sender = message['sender']
            print sender + ":" + content
        elif response == 'info':
            print content
        else:
            print "wops" + message

    def send_payload(self, data):
        self.connection.sendto(data, (self.host, self.port))

    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
