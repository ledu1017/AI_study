import os
import torch
import cv2
import matplotlib.pyplot as plt
from src.Models import Unet

os.environ['KMP_DUPLICATE_LIB_OK']='True'

def check_car_accident(img):
    # 여러 형태의 파손 영역 감지
    labels = ['Breakage_3', 'Crushed_2', 'Scratch_0', 'Seperated_1']
    models = []

    n_classes = 2
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    for label in labels:
        model_path = f'models/[DAMAGE][{label}]Unet.pt'

        model = Unet(encoder = 'resnet34', pre_weight = 'imagenet', num_classes=n_classes).to(device)
        model.model.load_state_dict(torch.load(model_path, map_location = torch.device(device)))
        model.eval()

        models.append(model)

    print('Loaded pretrained models!')

    img_path = 'car_image/image1.png'
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (256, 256))

    img_input = img / 255.
    img_input = img_input.transpose([2, 0, 1])
    img_input = torch.tensor(img_input).float().to(device)
    img_input = img_input.unsqueeze(0)

    fig, ax = plt.subplots(1, 5, figsize = (24, 10))

    ax[0].imshow(img)
    ax[0].axis('off')

    outputs = []

    for i, model in enumerate(models):
        output = model(img_input)

        img_output = torch.argmax(output, dim = 1).detach().cpu().numpy()
        img_output = img_output.transpose([1, 2, 0])

        outputs.append(img_output)

        ax[i+1].set_title(labels[i])
        ax[i+1].imshow(img_output, cmap='jet')
        ax[i+1].axis('off')

    fig.set_tight_layout(True)

    # 파손 영역 크기 계산

    for i, label in enumerate(labels):
        print(f'{label}: {outputs[i].sum()}')

    # 파손 영역 크기에 따른 가격 산출
    price_table = [
        100,    # Breakage_3
        200,    # Crushed_2
        50,     # Scratch_0
        120,    # Seperated_1
    ]
    
    total_price = 0
    result_str = ""
    
    for i, price in enumerate(price_table):
        area = outputs[i].sum()
        total_price += area * price
        result_str += f'{labels[i]} : \t영역: {area}\t가격:{area * price}원\n'
    
    result_str += f'총 가격: {total_price}원'
    
    # 이미지와 결과 문자열을 함께 반환합니다.
    return fig, result_str
