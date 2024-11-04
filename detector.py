import cv2
import torch
from torch.autograd import Variable as V
from torch.nn import functional as F
from ultralytics import YOLO
from PIL import Image
import numpy as np

from BlurryImageDetector.detect import is_image_blurry
from IndoorOutdoorClassification.detect import load_labels, load_model, returnTF


class Processor:
    def __init__(self, blurry_threshold=0.5, door_threshold=0.1, window_threshold=0.1):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.blurry_detect_model = torch.load('BlurryImageDetector/trained_model/trained_model-Kaggle_dataset')
        self.blurry_detect_model = self.blurry_detect_model['model_state']
        self.blurry_detect_model.to(self.device)
        
        self.door_detect_model = YOLO('YOLO_models/doors.pt')
        self.window_detect_model = YOLO('YOLO_models/windows.pt')

        self.scene_detect_model = load_model()
        self.scene_detect_model.avgpool = torch.nn.AvgPool2d(kernel_size=14, stride=14, padding=0)
        self.scene_classes, self.scene_labels_IO, self.scene_labels_attribute, self.scene_W_attribute = load_labels()
        self.tf = returnTF()

        self.blurry_threshold = blurry_threshold
        self.door_threshold, self.window_threshold = door_threshold, window_threshold
        
    def indoor_outdoor_detect(self, img_path):
        with torch.no_grad():
            img = Image.open(img_path)
            input_img = V(self.tf(img).unsqueeze(0), volatile=True)
            # input_img = self.tf(img).unsqueeze(0)
            logit = self.scene_detect_model.forward(input_img)
            h_x = F.softmax(logit, 1).data.squeeze()
            probs, idx = h_x.sort(0, True)
            io_image = np.mean(self.scene_labels_IO[idx[:10].numpy()])

        return 'indoor' if io_image < 0.5 else 'outdoor'

    def process(self, img_path):
        # print("--------------start--------------")
        img_gray = cv2.imread(img_path, 0)

        blurry_detect_res = is_image_blurry(self.blurry_detect_model, img_gray, self.blurry_threshold)
        if blurry_detect_res:
            return '模糊'

        door_detect_res = self.door_detect_model.predict(img_path, save=False, conf=self.door_threshold)
        if len(door_detect_res[0].boxes.cls):
            return '合格'
        window_detect_res = self.window_detect_model.predict(img_path, save=False, conf=self.window_threshold)
        if len(window_detect_res[0].boxes.cls):
            return '合格'

        scene_detect_res = self.indoor_outdoor_detect(img_path)
        if scene_detect_res == 'outdoor':
            return '合格'

        return '不合格'


if __name__ == '__main__':
    p = Processor()
    detect_res = p.process('../images/vague/8b4056b88b3ecb00459bca404bc5756c.jpg')
    print(detect_res)
