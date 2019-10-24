import threading
import cv2
import time
from queue import Queue
import os
import asyncio
from yolo import YoloSystem
import json
import glob
import numpy as np
# print(cv2.getBuildInformation())


class VideoCameraDetection:

    def __init__(self):
        self.cam = cv2.VideoCapture(-1)
        self.frame_queue = Queue()
        self.system = YoloSystem()

        print("[INFO] loading YOLO from disk...")
        weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
        configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])
        self.net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

        self.start = time.time()
        self.daemon_start()

    def daemon_start(self):
        print('Start Daemon')
        asyncio.run(self.capture())
        asyncio.run(self.processQueue())
        asyncio.run(self.createVideo())

    async def capture(self):
        print('Start capturing frames from camera')

        def captureFrames():
            frame_queue = self.frame_queue
            while True:
                grabbed, img = self.cam.read()
                if grabbed and (time.time() - self.start > 5):
                    print(frame_queue.qsize())
                    frame_queue.put(img)

        captureThread = threading.Thread(target=captureFrames)
        captureThread.start()

    async def processQueue(self):
        print('Start processing frames in queue')

        def process():
            while True:
                if not self.frame_queue.empty():
                    async def yoloOnImage():
                        self.system.ImageRecog(
                            self.frame_queue.get(), self.net)
                    asyncio.run(yoloOnImage())
                # await asyncio.sleep(0.0001)
        processThread = threading.Thread(target=process)
        processThread.start()

    async def createVideo(self):
        print('start creating video from dir queue')

        def stitch():
            while True:
                data = {}
                with open('directory_queue.json', 'r+') as queue_file:
                    data = json.load(queue_file)
                    if 'pending_folders' in data:
                        if len(data['pending_folders']) > 0:
                            createVideo(data['pending_folders'][0])
                            data['pending_folders'].pop(0)

                with open('directory_queue.json', 'wt') as queue_file:
                    json.dump(data, queue_file)

                if len(data['pending_folders']) == 0:
                    time.sleep(60)

        stitchThread = threading.Thread(target=stitch)
        stitchThread.start()


def createVideo(path):
    img_array = []
    size = (10, 10)
    for filename in glob.glob(path + '/*.jpg'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(
        path + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 11, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    print('video created at ' + path)


VideoCameraDetection()
