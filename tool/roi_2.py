import cv2


def OnMouseAction(event, x, y, flags, param):
    global img, position1, position2

    image = img.copy()

    if event == cv2.EVENT_LBUTTONDOWN:  # 按下左键
        position1 = (x, y)  # 获取鼠标的坐标(起始位置)

    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:  # 按住左键拖曳不放开
        cv2.rectangle(image, position1, (x, y), (0, 255, 0), 3)  # 画出矩形选定框
        cv2.imshow('image', image)

    elif event == cv2.EVENT_LBUTTONUP:  # 放开左键
        position2 = (x, y)  # 获取鼠标的最终位置
        cv2.rectangle(image, position1, position2, (0, 0, 255), 3)  # 画出最终的矩形
        cv2.imshow('image', image)

        min_x = min(position1[0], position2[0])  # 获得最小的坐标，因为可以由下往上拖动选定框
        min_y = min(position1[1], position2[1])
        width = abs(position1[0] - position2[0])  # 切割坐标
        height = abs(position1[1] - position2[1])

        cut_img = img[min_y:min_y + height, min_x:min_x + width]
        cv2.imshow('Cut', cut_img)


def main():
    global img
    img = cv2.imread(r'../icon/back.png', cv2.IMREAD_ANYCOLOR)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', OnMouseAction)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()