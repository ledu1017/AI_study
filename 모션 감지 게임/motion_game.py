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

            if faces:  # 얼굴이 감지되면,
                face = faces[0]  # 첫 번째 얼굴을 선택

                up = face[idList[0]]  # 얼굴의 위쪽 지점 선택
                down = face[idList[1]]  # 얼굴의 아래쪽 지점 선택

                for id in idList:  # idList의 모든 id에 대해,
                    cv2.circle(img, face[id], 5, (255, 0, 255), 5)  # 얼굴 지점에 원을 그림
                cv2.line(img, up, down, (0, 255, 0), 3)  # 얼굴의 위쪽과 아래쪽 지점 사이에 선을 그림
                cv2.line(img, face[idList[2]], face[idList[3]], (0, 255, 0), 3)  # 얼굴의 두 가운데 지점 사이에 선을 그림

                upDown, _ = detector.findDistance(face[idList[0]], face[idList[1]])  # 위쪽과 아래쪽 지점 사이의 거리 계산
                leftRight, _ = detector.findDistance(face[idList[2]], face[idList[3]])  # 두 가운데 지점 사이의 거리 계산

                ## Distance of the Object
                cx, cy = (up[0] + down[0]) // 2, (up[1] + down[1]) // 2  # 위쪽과 아래쪽 지점의 중간 좌표 계산
                cv2.line(img, (cx, cy), (pos[0] + 50, pos[1] + 50), (0, 255, 0), 3)  # 중간 좌표와 오브젝트 사이에 선을 그림
                distMouthObject, _ = detector.findDistance((cx, cy), (pos[0] + 50, pos[1] + 50))  # 중간 좌표와 오브젝트 사이의 거리 계산
                print(distMouthObject)  # 계산된 거리를 출력

                # Lip opened or closed
                ratio = int((upDown / leftRight) * 100)  # 입이 열려있는지 여부를 결정하는 비율 계산
                # print(ratio)  # 계산된 비율을 출력
                if ratio > 60:  # 비율이 60보다 크면,
                    mouthStatus = "Open"  # 입이 열려있음
                else:  # 비율이 60보다 작거나 같으면,
                    mouthStatus = "Closed"  # 입이 닫혀있음
                cv2.putText(img, mouthStatus, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)  # 입의 상태를 이미지에 텍스트로 표시

                if distMouthObject < 100 and ratio > 60:  # 거리가 100 미만이고, 입이 열려있으면,
                    if isEatable:  # 오브젝트가 먹을 수 있는 경우,
                        currentObject = resetObject()  # 오브젝트를 리셋하고,
                        count += 1  # 점수를 1점 늘림
                    else:  # 오브젝트가 먹을 수 없는 경우,
                        gameOver = True  # 게임 오버
            cv2.putText(img, str(count), (1100, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 5)  # 현재 점수를 이미지에 텍스트로 표시
        else:  # 게임 오버 상태라면,
            cv2.putText(img, "Game Over", (300, 400), cv2.FONT_HERSHEY_PLAIN, 7, (255, 0, 255), 10)  # "Game Over" 텍스트를 이미지에 표시

        cv2.imshow("Image", img)  # 이미지를 화면에 표시

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