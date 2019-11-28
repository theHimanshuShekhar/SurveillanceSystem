from flask import Flask, escape, request, Response, jsonify, send_file, send_from_directory
import os
from flask_cors import CORS, cross_origin
import cv2
import time
import json
import base64

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
            if name.split('.')[-1] == 'mp4':
                folder = root.split('/')[-1]
                if folder in results:
                    results[folder].append(os.path.join(root, name))
                else:
                    results[folder] = [os.path.join(root, name)]
    response = json.dumps(results)
    print('returned folders and videos')
    return response


@app.route('/thumb')
def getThumb():
    # path = './results/2019-10-24/1571907539.3689172.avi'
    # video = cv2.VideoCapture(path)
    # if video.isOpened:
    #     frame = video.read()[1]
    #     cnt = cv2.imencode('.jpg', frame)
    #     print(type(cnt))

    #     # b64 = base64.encodestring(cnt)
    #     # # print(b64.tostring())
    #     # print(type(b64))
    # video.release()
    return {'thumb': 'Test'}


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
    path = request.args.get('path')
    vid = cv2.VideoCapture(path)
    return Response(genVid(path, vid), mimetype='multipart/x-mixed-replace; boundary=frame')


def genVid(path, vid):
    while True:
        frame = vid.read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/')
def default():
    return 'Server Online'


@app.route('/getconfig')
def getconfig():
    with open('config.json', 'r+') as config_file:
        data = json.load(config_file)
    return data


@app.route('/setconfig')
def setconfig():
    data = {}
    selected = request.args.get('json')
    with open('config.json', 'r+') as config_file:
        data = json.load(config_file)
        data["selected_labels"] = []
        for sel in selected.split(','):
            data["selected_labels"].append(sel)

    with open('config.json', 'wt') as config_file:
        json.dump(data, config_file)

    return {'success': True}


@app.route('/test')
def test():
    return {serverOnline: True}


if __name__ == '__main__':
    print('Server Start')
    app.run(threaded=True)
