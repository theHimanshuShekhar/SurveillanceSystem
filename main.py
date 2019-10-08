
import cv2
import os

from yolo import *

# create a Socket.IO server
# import socketio
# sio = socketio.Server()
# print(sio)


def show_webcam(mirror=False):

    weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
    configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])

    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

    cam = cv2.VideoCapture(0)
    system = YoloSystem()
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
            # call yolo on current frame
        newimg = system.ImageRecog(img, net)
        # send frame to client using socket.

        cv2.imshow('my webcam', newimg)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()
