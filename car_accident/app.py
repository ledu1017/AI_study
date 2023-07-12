from flask import Flask, render_template, request
from car_accident import check_car_accident
import io
import base64
app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    image = request.files['image']
    fig, result = check_car_accident(image.filename)
    
    # Matplotlib으로 생성한 이미지를 PNG 형식으로 인코딩합니다.
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    png_img = base64.b64encode(img.getvalue()).decode()
    
    # 결과를 result.html 템플릿에 전달하여 렌더링합니다.
    return render_template('result.html', result=result, image=png_img)

if __name__ == '__main__':
    app.run()
