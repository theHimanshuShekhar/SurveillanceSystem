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
from imutils.video import FPS
# print(cv2.getBuildInformation())
# print(cv2.getVersionMajor())
# print(cv2.getVersionMinor())


class VideoCameraDetection:

    def __init__(self):
        self.cam = cv2.VideoCapture(-1)
        self.fps = 1
        self.minfps = 25
        self.batch_queue = Queue()
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
            interval = 2
            lasttime = time.time()
            frame_arr = []
            while True:
                grabbed, img = self.cam.read()

                if grabbed:
                    framecount = framecount + 1
                    if self.fps >= self.minfps:
                        frame_arr.append(img)

                def diff():
                    return int(time.time() - lasttime)

                if(diff() > interval):
                    if len(frame_arr) > 0:
                        self.batch_queue.put(
                            {"fps": self.fps, "frames": frame_arr, "length": diff()})

                    frame_arr = []

                    self.fps = framecount//diff()
                    framecount = 0
                    lasttime = time.time()

                    if diff() > 10:
                        print('time elapsed', int(
                            time.time() - self.start), 'seconds')
                cv2.waitKey(1000//30)

        captureThread = threading.Thread(target=captureFrames)
        captureThread.start()

    async def processQueue(self):
        print('Start processing frames in queue')

        def process():
            while True:
                if not self.batch_queue.empty():
                    batch = self.batch_queue.get()
                    detected, timestamp, labels = self.system.ImageRecog(
                        batch["frames"][randint(0, len(batch["frames"])-1)], self.net)
                    if detected:
                        # print('saving batch: detected', labels, batch["fps"], 'fps from batch',
                        #       'size', len(batch["frames"]))
                        self.saveBuffer(
                            batch["frames"], timestamp, batch["fps"])

                        batch = self.batch_queue.get()
                        self.saveBuffer(
                            batch["frames"], timestamp, batch["fps"])

        processThread = threading.Thread(target=process)
        processThread.start()

    def saveBuffer(self, buffer, timestamp, fps):
        for index, frame in enumerate(buffer):
            isSaved = self.system.saveResult(
                frame, timestamp, timestamp + str(index), fps)
            # print('frame', index, 'saved')

    async def stitchVideo(self):
        print('start creating video from dir queue')

        def stitch():
            while True:
                data = {}
                with open('directory_queue.json', 'r+') as queue_file:
                    data = json.load(queue_file)
                    if 'pending_folders' in data:
                        if len(data['pending_folders']) > 0:
                            self.createVideo(data['pending_folders'].pop(
                                0), data['pending_folders'].pop(
                                0))

                with open('directory_queue.json', 'wt') as queue_file:
                    json.dump(data, queue_file)

                if len(data['pending_folders']) == 0:
                    time.sleep(60)

        stitchThread = threading.Thread(target=stitch)
        stitchThread.start()

    def createVideo(self, path, fps):

        img_array = []
        size = (10, 10)
        for filename in glob.glob(path + '/*.jpg'):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)

        write_fps = fps

        out = cv2.VideoWriter(
            path + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), write_fps, size)

        for i in range(len(img_array)):
            out.write(img_array[i])
            # cv2.waitKey(1000//self.minfps)
        out.release()
        print('video created at ' + path, 'at', write_fps, 'fps')


VideoCameraDetection()
