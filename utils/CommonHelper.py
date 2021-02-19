#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, "r", encoding='gbk') as f:
            return f.read()
