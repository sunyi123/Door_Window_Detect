# 门窗检测

## 环境配置:

```
# python=3.8, cuda=12.1
pip install opencv-python pillow numpy
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
pip install ultralytics
```

## 检测链路:
```
from detector import Processor
p = Processor()
detect_res = p.process(img_path)
# detect_res in ['模糊'， '合格'， '不合格']
```
- 首先检测图片是否模糊，若模糊直接返回'模糊'
- 对于清晰图片，其次检测图片中是否有门窗，若有则返回'合格'
- 对于未检测到门窗的图片，判断图片处于室内或室外，判断为室外返回'合格'，否则返回'不合格'
