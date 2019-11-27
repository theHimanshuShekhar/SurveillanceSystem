from flask import Flask, escape, request, Response
import os
from flask_cors import CORS, cross_origin
import cv2
import time

from daemon import VideoCameraDetection
cam = VideoCameraDetection()

app = Flask(__name__)
cors = CORS(app, resources={r"/folders": {"origins": "*"}})


@app.route('/')
def hello():
    return 'Server Online!'


@app.route('/folders')
def getResults():
    results = {}
    for root, dirs, files in os.walk("./results", topdown=False):
        for name in files:
            if name.split('.')[-1] == 'avi':
                folder = root.split('/')[-1]
                if folder in results:
                    results[folder].append(os.path.join(root, name))
                else:
                    results[folder] = [os.path.join(root, name)]
    return results


@app.route('/live')
def getVideo():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen():
    while True:
        frame = cam.getframe()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video')
def getVideo():
    return 'Return video from path'

@app.route('/')
def test():
    return 'Server Online'


if __name__ == '__main__':
    print('Server Start')
    app.run()
