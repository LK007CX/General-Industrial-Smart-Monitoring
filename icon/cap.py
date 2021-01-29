import cv2
import numpy as np

# 图片的分辨率为200*300，这里b, g, r设为随机值，注意dtype属性
img = np.zeros((400, 600, 3), dtype=np.uint8)
# img[0, :, :] = 1
# img[1, :, :] = 74
# img[2, :, :] = 111
img[:, :, 0] = 111
img[:, :, 1] = 74
img[:, :, 2] = 1
# 显示图片

# print(img.shape)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
# print(img.shape)
# img[:, :, 3] = 2
# print(img.shape)
cv2.imshow('test', img)
cv2.imwrite('cap.png', img)
cv2.waitKey(0)
cv2.destroyWindow('test')
