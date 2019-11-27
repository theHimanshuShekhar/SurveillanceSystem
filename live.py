from flask import Flask, escape, request, Response
import os
from flask_cors import CORS, cross_origin
import cv2
import time

app = Flask(__name__)

cors = CORS(app, resources={r"/folders": {"origins": "*"}})


@app.route('/')
def hello():
    return 'Server Online Works!'


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


@app.route('/video')
def getVideo():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen():
    while True:
        path = './current/' + os.listdir('./current')[0]
        image = cv2.imread(path)
        ret, jpeg = cv2.imencode('.jpg', image)
        if ret:
            frame = jpeg.tobytes()
            # print(len(frame))
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        os.remove(path)
        time.sleep(1000//40)


@app.route('/')
def test():
    return 'Server Online'


if __name__ == '__main__':
    print('Server Start')
    app.run()
