#!/usr/bin/python3
# -*- coding: UTF-8 -*-


def get_names(config_path):
    """
    Get names by config.
    :param config_path: config path
    :return: CUSTOM_CLASSES_LIST
    """
    CUSTOM_CLASSES_LIST = []
    with open(config_path) as f:
        for line in f.readlines():
            if line != '':
                CUSTOM_CLASSES_LIST.append(line.rstrip('\n'))
    return CUSTOM_CLASSES_LIST


def get_cls_dict(config_path):
    """
    Get the class ID to name translation dictionary.
    :param config_path: config path
    :return: None
    """
    return {i: n for i, n in enumerate(get_names(config_path))}
