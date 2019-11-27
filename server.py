from flask import Flask, escape, request, Response, jsonify
import os
from flask_cors import CORS, cross_origin
import cv2
import time
import json

from daemon import VideoCameraDetection
cam = VideoCameraDetection()

app = Flask(__name__)

cors = CORS(app, resorces={r'/d/*': {"origins": '*'}})


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
    # response = json.dumps(results)
    response = json.dumps(results)
    return response


@app.route('/live')
def getVideo():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen():
    while True:
        frame = cam.getframe()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video')
def getPathVideo():
    return 'Return video from path'


@app.route('/')
def default():
    return 'Server Online'


@app.route('/test')
def test():
    return {serverOnline: True}


if __name__ == '__main__':
    print('Server Start')
    app.run(threaded=True)
