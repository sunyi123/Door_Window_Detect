# 门窗检测

## 环境配置:

```
# python=3.10, cuda=12.1
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

## Docker
### 环境要求
- Docker
- NVIDIA GPU
- NVIDIA Driver (支持CUDA 12.1)
- NVIDIA Container Toolkit

### 部署步骤

#### 1. 安装 NVIDIA Container Toolkit（如果未安装）
```bash
# Ubuntu系统安装命令
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

#### 2. 加载Docker镜像
```bash
# 加载提供的镜像文件
docker load < door-window-detect.tar
```

#### 3. 运行容器
```bash
# 创建容器并挂载项目目录
docker run -d --gpus all \
  -v /your/local/path/Door_Window_Detect:/app/Door_Window_Detect \
  --name door-window-container \
  door-window-detect
```

#### 4. 运行代码
```bash
# 进入容器
docker exec -it door-window-container bash

# 现在你在容器内部，可以运行Python脚本
python3 your_script.py
```

### 验证部署
```bash
# 检查CUDA是否可用
docker exec -it door-window-container python3 -c "import torch; print(torch.cuda.is_available())"
```

### 常见问题解决

1. 如果出现GPU不可用的问题：
   - 确认NVIDIA驱动已正确安装
   - 确认使用了--gpus all参数启动容器

2. 如果出现权限问题：
   - 检查挂载目录的权限
   - 必要时使用sudo运行docker命令

3. 如果需要查看容器日志：
   ```bash
   docker logs door-window-container
   ```

### 目录说明
容器中的工作目录为 `/app/Door_Window_Detect`，这里会映射到你的本地项目目录。

### 注意事项
- 确保挂载路径正确
- 代码修改后不需要重启容器
- 建议定期备份项目文件
