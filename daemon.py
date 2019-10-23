import threading
import cv2
import time
from queue import Queue
import asyncio
from yolo import *
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
                    frame_queue.put(img)

        captureThread = threading.Thread(target=captureFrames)
        captureThread.start()

    async def processQueue(self):
        print('Start processing frames in queue')

        def process():
            while True:
                if not self.frame_queue.empty():
                    self.system.ImageRecog(self.frame_queue.get(), self.net)
                # await asyncio.sleep(0.0001)
        processThread = threading.Thread(target=process)
        processThread.start()

    async def createVideo(self):
        print('start creating video from dir queue')

        def stitch():
            # while True:
            print('createVideo()')

        stitchThread = threading.Thread(target=stitch)
        stitchThread.start()


VideoCameraDetection()
