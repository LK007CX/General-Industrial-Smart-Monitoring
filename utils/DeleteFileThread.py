# -*- coding: utf-8 -*-
# /usr/bin/python3
import os

from PyQt5.QtCore import QThread


class DeleteFileThread(QThread):
    """
    Delete the first n files in the specified folder, sorted by time.
    """

    def __init__(self, file_path, max_save_num, parent=None):
        super(DeleteFileThread, self).__init__(parent)

        self.max_save_num = max_save_num
        self.file_path = file_path

    def sort_file_by_time(self):
        """
        Sort file by modification time or creation time.
        :return: None
        """
        dir_list = os.listdir(self.file_path)
        if not dir_list:
            return
        else:
            # Note that the lambda expression is used here to arrange the files
            # in ascending order according to the last modification time.
            # os.path.getmtime(): get the last modification time of the file
            # os.path.getctime(): get the last creation time of the file
            dir_list = sorted(dir_list, key=lambda x: os.path.getctime(os.path.join(self.file_path, x)))
            temp_list = []
            for file_name in dir_list:
                temp_list.append(os.path.join(self.file_path, file_name))
            return temp_list

    def delete_file_by_index(self, temp_list):
        """
        Delete file by index.
        :param temp_list: file name list
        :return: None
        """
        try:
            length = len(temp_list)
            if length < self.max_save_num:
                pass
            delete_list = temp_list[0: (length - self.max_save_num)]
            for file_name in delete_list:
                if not os.path.exists(file_name):
                    break
                os.remove(file_name)
            print("已删除" + str(len(delete_list)) + "张图片")
        except Exception as e:
            print(e)

    def run(self):
        while True:
            temp_list = self.sort_file_by_time()
            self.delete_file_by_index(temp_list)
            self.sleep(60)
