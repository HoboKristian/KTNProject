# -*- coding: utf-8 -*-
import SocketServer
import time
import json
import re

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

logged_in_users = {}
history = []

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def local_key(self):
        return self.key_from_ip_port(self.ip, self.port)

    def key_from_ip_port(self, ip, port):
        return str(ip + str(port))

    def user_logged_in(self):
        sender = logged_in_users[self.local_key()]['username']
        return sender != ''

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        logged_in_users[self.local_key()] = {
                'ip': self.ip,
                'port': self.port,
                'connection': self.connection,
                'username': ''
                }

        print logged_in_users

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            if received_string != "":
                print received_string
                received_string = json.loads(received_string)

                request = received_string['request']
                content = received_string['content']

                if request == 'login':
                    self.handle_login(content)
                elif request == 'logout':
                    self.handle_logout()
                elif request == 'msg':
                    self.handle_msg(content)
                elif request == 'help':
                    self.handle_help()
                elif request == 'names':
                    self.handle_names()
                else:
                    self.send_reponse('error', 'not supported', 'server')

    def send_reponse(self, response, content, sender):
        self.send_reponse_to_ip_port(self.connection, response, content, sender, self.ip, self.port)

    def send_history(self):
        self.send_reponse('history', json.dumps(history), 'server')

    def send_error(self, error):
        self.send_reponse("error", error, "server")

    def send_reponse_to_ip_port(self, connection, response, content, sender, ip, port):
        send_time = time.time()
        response = {
                "response": response,
                "content": content,
                "timestamp": send_time,
                "sender": sender
                }
        connection.sendto(json.dumps(response), (ip, port))

    def handle_login(self, username):
        if re.match("^[\w\d_-]+$", username):
            username_avail = True
            for key in logged_in_users:
                user = logged_in_users[key]
                if username == user['username']:
                    username_avail = False
            if username_avail:
                if not self.user_logged_in():
                    logged_in_users[self.local_key()]['username'] = username
                    self.send_history()
                else:
                    self.send_error("Client already logged in")
            else:
                self.send_error("username already logged in")
        else:
            self.send_error("username is not a-Z or 0-9")

    def handle_logout(self):
        if not user_logged_in():
            self.send_error("not logged in")
        else:
            logged_in_users[self.local_key()]['username'] = ''

    def handle_msg(self, message):
        sender = logged_in_users[self.local_key()]['username']
        if sender == '':
            self.send_error("not logged in")
        else:
            history.append({'sender':sender, 'content':message})
            for key in logged_in_users:
                user = logged_in_users[key]
                ip = user['ip']
                port = user['port']
                connection = user['connection']
                username = user['username']

                if username != '':
                    try:
                        self.send_reponse_to_ip_port(connection, "message", message, sender, ip, port)
                    except:
                        pass

    def handle_names(self):
        if not user_logged_in():
            self.send_error("not logged in")
        else:
            names = []
            for key in logged_in_users:
                user = logged_in_users[key]
                username = user['username']
                if username != '':
                    names.append(username)

            self.send_reponse("info", json.dumps(names), "server")

    def handle_help(self):
        help_text = """Support commands are:
        login: logs in the username
        logout: logs out the username
        help: displays this
        msg: broadcasts a message
        names: sends a list of all logged in usernames"""

        self.send_reponse("info", help_text, "server")


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
