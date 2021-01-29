#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from PyQt5.QtCore import QThread

from utils.edgeAgent import http_post, gen_edgeeye_predict_json


class EdgeAgentWorker(QThread):

    def __init__(self, args, parent=None):
        super(EdgeAgentWorker, self).__init__(parent)
        self.conn_timeout = args.conn_timeout
        self.post_timeout = args.post_timeout
        self.server_address = args.server_address

    def send(self, info):
        """
        Send data to the server.
        :param info: information
        :return: None
        """
        rtn = http_post(url=self.server_address, \
                        send_headers={"Content-Type": "application/json; charset=UTF-8", "user-agent": "EdgeApp"}, \
                        send_info=gen_edgeeye_predict_json([info], "POST"), \
                        conn_timeout=self.conn_timeout, post_timeout=self.post_timeout)
        print(rtn)

    def run(self):
        pass
