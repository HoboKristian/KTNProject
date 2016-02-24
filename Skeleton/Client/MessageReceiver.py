# -*- coding: utf-8 -*-
from threading import Thread
import socket

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        Thread.__init__(self)
        self.daemon = True

        # TODO: Finish initialization of MessageReceiver
        self.connection = connection
        self.client = client

    def run(self):
        while True:
            try:
                t = self.connection.recv(4096)
                self.client.receive_message(t)
            except:
                self.client.disconnect();
                break
