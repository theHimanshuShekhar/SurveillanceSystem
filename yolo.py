
import numpy as np
import datetime
# import argparse
import time
import cv2
import os
import json

# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
#	help="path to input image")
# ap.add_argument("-y", "--yolo", required=True,
#	help="base path to YOLO directory")
# ap.add_argument("-c", "--confidence", type=float, default=0.5,
#	help="minimum probability to filter weak detections")
# ap.add_argument("-t", "--threshold", type=float, default=0.3,
#	help="threshold when applyong non-maxima suppression")
# args = vars(ap.parse_args())


class YoloSystem:

    lasttime = time.time()

    def __init__(self):
        print('Create system object')
        self.lasttime = None
        self.lastpath = None

    def ImageRecog(self, image, net):

        timestamp = datetime.datetime.now().isoformat()

        labelsPath = os.path.sep.join(["yolo-coco", "coco.names"])
        LABELS = open(labelsPath).read().strip().split("\n")

        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
                                   dtype="uint8")

        (H, W) = image.shape[:2]

        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        net.setInput(blob)
        # start = time.time()
        layerOutputs = net.forward(ln)
        # end = time.time()

        # print("[INFO] YOLO took {:.6f} seconds".format(end - start))

        boxes = []
        confidences = []
        classIDs = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > 0.7:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5,
                                0.3)

        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)
            print('detected: ' + text)
            # self.saveResult(image, timestamp, text)
            return True, timestamp

        return False, timestamp

    def saveResult(self, image, timestamp, text, fps):

        dirname = os.path.dirname(__file__)

        if not os.path.exists(dirname + '/results'):
            os.makedirs('results')

        new = False
        if not self.lasttime:
            self.lasttime = time.time()

        currenttime = time.time()
        time_elapsed = abs(self.lasttime - currenttime)
        if(time_elapsed > 20):
            new = True
            self.lasttime = currenttime
        else:
            self.lasttime = time.time()

        currentdate = str(datetime.date.today())

        if not os.path.exists(dirname + '/results/' + currentdate):
            os.makedirs('results/' + currentdate)

        currentpath = os.path.join(dirname, 'results/' + currentdate + '/' +
                                   str(currenttime))

        if(new or not self.lastpath):
            if new:
                self.addFolder(self.lastpath, fps)

            self.lastpath = currentpath

            currenttime = str(currenttime)

            if not os.path.exists(dirname + '/results/' + currentdate + '/' + currenttime):
                os.makedirs('results/' + currentdate + '/' + currenttime)
            path = os.path.join(dirname, 'results/' + currentdate + '/' +
                                currenttime)

            self.lastpath = path

        filename = '/' + timestamp + '.jpg'

        cv2.imwrite(self.lastpath + filename, image)

    def addFolder(self, path, fps):
        print('add completed folder path to config queue' + path)
        data = {}
        with open('directory_queue.json', 'r') as config_file:
            data = json.load(config_file)
            if 'pending_folders' in data:
                data['pending_folders'].append(path)
                data['pending_folders'].append(fps)
            else:
                data['pending_folders'] = [path, fps]

        with open('directory_queue.json', 'wt') as config_file:
            json.dump(data, config_file)
