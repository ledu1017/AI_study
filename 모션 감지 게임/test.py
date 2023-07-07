import os
import random
import cv2
import requests
import jsonify
import json
from flask import Flask, render_template, Response, request
from flask_cors import CORS
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone

app = Flask(__name__)
CORS(app)

def generate_frames():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = FaceMeshDetector(maxFaces=1)
    idList = [0, 17, 78, 292]

    folderEatable = 'Objects/eatable'
    listEatable = os.listdir(folderEatable)
    eatables = []
    for object in listEatable:
        eatables.append(cv2.imread(f'{folderEatable}/{object}', cv2.IMREAD_UNCHANGED))

    folderNonEatable = 'Objects/noneatable'
    listNonEatable = os.listdir(folderNonEatable)
    nonEatables = []
    for object in listNonEatable:
        nonEatables.append(cv2.imread(f'{folderNonEatable}/{object}', cv2.IMREAD_UNCHANGED))

    currentObject = eatables[0]
    pos = [300, 0]
    speed = 8
    count = 0
    global isEatable
    isEatable = True
    gameOver = False

    def resetObject():
        global gameOver
        global isEatable
        pos[0] = random.randint(100, 1180)
        pos[1] = 0
        randNo = random.randint(0, 2)
        if randNo == 0:
            currentObject = nonEatables[random.randint(0, 3)]
            isEatable = False
        else:
            currentObject = eatables[random.randint(0, 3)]
            isEatable = True   

        if not isEatable:
            gameOver = True
            username = request.form['username']
            print(username)
            new_score = 0

            # 점수를 PHP로 전송
            url = 'http://localhost/update_score.php'
            data = {'username': username, 'score': new_score}
            response = requests.post(url, data=data)

            if response.status_code == 200:
                result = json.loads(response.content)
                if result['status'] == 'success':
                    print('Score updated successfully')
                else:
                    print('Failed to update score')
            else:
                print('Failed to connect to PHP script')

        return currentObject

    while True:
        success, img = cap.read()

        if gameOver is False:
            img, faces = detector.findFaceMesh(img, draw=False)

            img = cvzone.overlayPNG(img, currentObject, pos)
            pos[1] += speed

            if pos[1] > 520:
                currentObject = resetObject()

            if faces:
                face = faces[0]

                up = face[idList[0]]
                down = face[idList[1]]

                for id in idList:
                    cv2.circle(img, face[id], 5, (255, 0, 255), 5)
                cv2.line(img, up, down, (0, 255, 0), 3)
                cv2.line(img, face[idList[2]], face[idList[3]], (0, 255, 0), 3)

                upDown, _ = detector.findDistance(face[idList[0]], face[idList[1]])
                leftRight, _ = detector.findDistance(face[idList[2]], face[idList[3]])

                cx, cy = (up[0] + down[0]) // 2, (up[1] + down[1]) // 2
                cv2.circle(img, (cx, cy), 7, (0, 255, 255), cv2.FILLED)

                if isEatable:
                    if upDown < 35 and leftRight < 25:
                        pos[1] += speed
                        pos[0] = cx
                        count += 1
                        currentObject = resetObject()

        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/start_game')
def start_gate():
    response = requests.get('http://localhost/ranking.php')
    response.encoding = 'utf-8'  # 인코딩 설정
    data = response.text
    decoded_data = json.loads(data)  # 유니코드 이스케이프 시퀀스를 한글로 변환
    return render_template('index.html', rankings = decoded_data)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # flask run --host=0.0.0.0 --port=5000