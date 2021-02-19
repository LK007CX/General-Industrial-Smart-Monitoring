import base64
import datetime
import sys
import time
from collections import namedtuple

import cv2
import numpy as np
import requests

cv2_img_info = namedtuple('cv2_img_info', 'file_name file_ext_name cv_mat')

inference_box_info = namedtuple('inference_box_info', 'image_name box_seq box_label '
                                                      'box_x_min box_y_min box_x_max box_y_max box_confidence')

edgeeye_ld_prediction = namedtuple('edgeeye_ld_prediction', 'ftp_url image_path raw_image_path line_id eqp_id '
                                                            'station_id op_id host_name fab_id process_stage '
                                                            'image_name image_ext_name project_id project_name '
                                                            'model_name model_version model_iter model_labels '
                                                            'model_type prediction_type predict_result '
                                                            'predict_defect_code inference_info_array img_array '
                                                            'img_raw_array')


def gen_edgeeye_predict_json(src_data, img_upload_mode):
    image_name, image_base64_str, image_raw_base64_str = '', bytes('', 'utf-8'), bytes('', 'utf-8')
    image_path, raw_image_path, inference_info_string = '', '', ''
    for idx in range(len(src_data)):
        # 將inference_box_info轉成inference_info字串
        # print(type(src_data[idx].inference_info_array))
        for x in range(len(src_data[idx].inference_info_array)):
            if not inference_info_string == '':
                inference_info_string = inference_info_string + ','

            inference_info_string = inference_info_string \
                                    + src_data[idx].inference_info_array[x].image_name + ';' \
                                    + src_data[idx].inference_info_array[x].box_seq + ';' \
                                    + src_data[idx].inference_info_array[x].box_label + ';' \
                                    + src_data[idx].inference_info_array[x].box_x_min + ';' \
                                    + src_data[idx].inference_info_array[x].box_y_min + ';' \
                                    + src_data[idx].inference_info_array[x].box_x_max + ';' \
                                    + src_data[idx].inference_info_array[x].box_y_max + ';' \
                                    + src_data[idx].inference_info_array[x].box_confidence

        if img_upload_mode == 'FTP':
            ftp_url = src_data[idx].ftp_url
            image_name = src_data[idx].image_name
            image_path = src_data[idx].image_path
            raw_image_path = src_data[idx].raw_image_path
            image_base64_str = bytes('', 'utf-8')
            image_raw_base64_str = bytes('', 'utf-8')

        elif img_upload_mode == 'POST':
            ftp_url = ''
            image_name = ''
            image_path = ''
            raw_image_path = ''
            image_base64_str = bytes('', 'utf-8')
            image_raw_base64_str = bytes('', 'utf-8')

            # 將Image轉換為base64字串
            for x in range(len(src_data[idx].img_array)):
                if not image_name == '':
                    image_name = image_name + ';'
                if not len(image_base64_str) == 0:
                    image_base64_str = image_base64_str + bytes('&', 'utf-8')
                if not len(image_raw_base64_str) == 0:
                    image_raw_base64_str = image_raw_base64_str + bytes('&', 'utf-8')

                image_name = image_name + src_data[idx].img_array[x].file_name
                image_base64_str = image_base64_str + cv2_base64(src_data[idx].img_array[x].cv_mat)
                image_raw_base64_str = image_raw_base64_str + cv2_base64(src_data[idx].img_raw_array[x].cv_mat)

        # if not len(image_base64_str) == 0:
        #     image_base64_str = image_base64_str + bytes('#', 'utf-8')
        # if not len(image_raw_base64_str) == 0:
        #     image_raw_base64_str = image_raw_base64_str + bytes('#', 'utf-8')

        json_data = [{
            'ftp_url': ftp_url,  # Source FTP path (FTP root path) (無上傳圖檔或Post模式, 留空)
            'image_path': image_path,  # Predict image path (無上傳圖檔或Post模式, 留空)
            'raw_image_path': raw_image_path,  # Raw image path (無上傳圖檔或Post模式, 留空)
            'line_id': src_data[idx].line_id,  # 線別
            'eqp_id': src_data[idx].eqp_id,  # 機台代碼
            'station_id': src_data[idx].station_id,  # 工作站
            'op_id': src_data[idx].op_id,  # 站點
            'host_name': src_data[idx].host_name,  # Edge裝置名稱
            'fab_id': src_data[idx].fab_id,  # 廠別
            'process_stage': src_data[idx].process_stage,  # 製程區域
            'image_name': image_name,  # 影像檔名列表, 用;分隔, name: YYMMDDhhmmss_DDhhmmssms_SeqNo
            'image_ext_name': src_data[idx].image_ext_name,  # 副檔名
            'project_id': src_data[idx].project_id,  # LCM AI365 Project ID
            'project_name': src_data[idx].project_name,  # LCM AI365 Project Name
            'model_name': src_data[idx].model_name,  # 模型名稱
            'model_version': src_data[idx].model_version,  # 模型版本
            'model_iter': src_data[idx].model_iter,  # 模型訓練次數
            'model_labels': src_data[idx].model_labels,  # 模型標籤labels, 陣列類型, 用,分隔

            # Model Type
            # 1.YOLOv3.KS (M04)
            # 2.YOLOv3-Tiny (M06)
            # 3.YOLOv3
            # 4.YOLO4Y-Tiny
            # 5.YOLOv4 (M07)
            'model_type': src_data[idx].model_type,

            # Predict Type (1-49 for EdgeEye)
            # 0.N/A
            # 1.Electronic Fence
            # 2.Object Sequence
            # 3.Object Verify
            # 4.Work Area Sequence
            # 5.Tracking Verify
            # Predict Type (50-99 for Not EdgeEye )
            # 50. SZ Auto Team - Nano App
            'prediction_type': src_data[idx].prediction_type,

            'predict_result': src_data[idx].predict_result,  # predict Result
            'predict_defect_code': src_data[idx].predict_defect_code,  # Predict defect code

            # Inference資訊
            # 陣列類型, 資訊用,分隔 [info1,info2,info3,...,info N]
            # info:'image_name;box_seq;box_label;box_x_min;box_y_min;box_x_max;box_y_max;box_confidence' 用;分隔
            'inference_info': inference_info_string,

            'img_upload_mode': img_upload_mode,  # FTP / POST
            'img_string': image_base64_str.decode("utf-8"),  # bytes to string
            'img_string_raw': image_raw_base64_str.decode("utf-8"),  # bytes to string
            'lm_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # YYYY-MM-DD HH:mm:ss
        }]

    return json_data


def http_post(url, send_headers, send_info, conn_timeout, post_timeout):
    try:
        print(time.strftime("%m-%d %H:%M:%S ", time.localtime()) + ' http_post start ... ' + url)
        r = requests.post(url, headers=send_headers, data=str(send_info) + '#endpoint',
                          timeout=(conn_timeout, post_timeout))
        r.close()

        if r.status_code == requests.codes.ok:
            print(time.strftime("%m-%d %H:%M:%S ", time.localtime()) + " Response OK (" + str(
                r.status_code) + "), Content= " + str(r.content))
        else:
            print(time.strftime("%m-%d %H:%M:%S ", time.localtime()) + " Response NG (" + str(
                r.status_code) + "), Content= " + str(r.content))

        return r.content.decode("utf-8")

    except requests.Timeout:
        print(time.strftime("%m-%d %H:%M:%S ", time.localtime()) + " " + 'Timeout')
        print(sys.exc_info())
        return "Timeout"

    except requests.exceptions.ConnectionError:
        print(time.strftime("%m-%d %H:%M:%S ", time.localtime()) + " " + 'Connection Error, please check Server')
        print(sys.exc_info())
        return "Connection Error, please check Server"

    except requests.exceptions.ChunkedEncodingError:
        print(
            time.strftime("%m-%d %H:%M:%S ", time.localtime()) + " " + 'Chunked Encoding Error, please check encoding')
        print(sys.exc_info())
        return "Chunked Encoding Error, please check encoding"

    except:
        print(time.strftime("%m-%d %H:%M:%S ",
                            time.localtime()) + " " + 'Unfortunitely, An Unknow Error Happened, Please connect system owner')
        print(sys.exc_info())
        return "Unfortunitely, An Unknow Error Happened, Please connect system owner"


def cv2_base64(cv2_image):
    base64_img = cv2.imencode('.jpg', cv2_image)[1].tostring()
    base64_str = base64.b64encode(base64_img)

    return base64_str


def base64_cv2(base64_str):
    str_img = base64.b64decode(base64_str)
    nparr = np.fromstring(str_img, np.uint8)
    cv2_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return cv2_image
