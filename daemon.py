import threading
import cv2
import time
from queue import Queue
import os
import asyncio
import yolo
import json
import glob
import numpy as np
from random import randint
import math
# print(cv2.getBuildInformation())


class VideoCameraDetection:

    def __init__(self):
        self.cam = cv2.VideoCapture(-1)
        self.fps = 15
        self.minfps = 20
        self.frame_queue = Queue()
        self.system = yolo.YoloSystem()

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
        asyncio.run(self.stitchVideo())

    async def capture(self):
        print('Start capturing frames from camera')

        def captureFrames():
            framecount = 0
            while True:
                grabbed, img = self.cam.read()
                if grabbed and self.fps > self.minfps:
                    self.frame_queue.put(img)

                diff = math.floor((time.time() - self.start))
                if(diff > 5):
                    if grabbed:
                        framecount = framecount + 1
                    self.fps = framecount // math.floor(
                        (time.time() - self.start))

        captureThread = threading.Thread(target=captureFrames)
        captureThread.start()

    async def processQueue(self):
        print('Start processing frames in queue')

        def process():
            while True:
                buffer_size = self.minfps
                if self.fps > self.minfps:
                    buffer_size = self.fps + 10
                if self.frame_queue.qsize() > buffer_size:
                    buffer = []
                    for i in range(buffer_size):
                        buffer.append(self.frame_queue.get())
                    detected, timestamp = self.system.ImageRecog(
                        buffer[randint(0, buffer_size-1)], self.net)
                    if detected:
                        self.saveBuffer(buffer, timestamp)

        processThread = threading.Thread(target=process)
        processThread.start()

    def saveBuffer(self, buffer, timestamp):
        for index, frame in enumerate(buffer):
            self.system.saveResult(frame, timestamp, timestamp + str(index))

    async def stitchVideo(self):
        print('start creating video from dir queue')

        def stitch():
            while True:
                print(self.fps)
                data = {}
                with open('directory_queue.json', 'r+') as queue_file:
                    data = json.load(queue_file)
                    if 'pending_folders' in data:
                        if len(data['pending_folders']) > 0:
                            self.createVideo(data['pending_folders'][0])
                            data['pending_folders'].pop(0)

                with open('directory_queue.json', 'wt') as queue_file:
                    json.dump(data, queue_file)

                if len(data['pending_folders']) == 0:
                    time.sleep(60)

        stitchThread = threading.Thread(target=stitch)
        stitchThread.start()

    def createVideo(self, path):

        img_array = []
        size = (10, 10)
        for filename in glob.glob(path + '/*.jpg'):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)

        out = cv2.VideoWriter(
            path + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 8, size)

        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        print('video created at ' + path)


VideoCameraDetection()
