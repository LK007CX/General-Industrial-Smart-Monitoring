import cv2

# cap = cv2.VideoCapture('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov')
cap = cv2.VideoCapture('rtsp://192.168.0.10:8554/test')
while cap.isOpened():
    (status, frame) = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()