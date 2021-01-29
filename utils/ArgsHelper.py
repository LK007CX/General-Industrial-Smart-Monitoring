#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class ArgsHelper(object):
    __slots__ = 'image', 'video', 'video_looping', 'rtsp', 'rtsp_latency', 'usb', 'onboard', 'copy_frame', \
                'do_resize', 'width', 'height', 'category_num', 'model', 'detect_time', 'input_pin', 'trigger_mode', \
                'time_delay', 'detect_mode', 'yolo_dim', 'labelsfile', 'thresh', 'item_list', 'minimum_storage_interval', \
                'maximum_storage_quantity', 'enable_save_image', 'enable_remote_cv', 'enable_data_upload', \
                'server_address', 'host_name', 'conn_timeout', 'post_timeout', 'project_id', 'project_name', \
                'image_file_suffix', 'site', 'line_id', 'eqp_id', 'station_id', 'op_id', 'process_stage', 'model_name', \
                'model_version', 'model_iteration', 'model_labels', 'model_type', 'predict_type'

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
