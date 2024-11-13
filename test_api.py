import requests
import os

def test_detect_api(image_path):
    """测试门窗检测API"""
    # API端点
    url = 'http://localhost:5000/detect'
    
    # 确认文件存在
    if not os.path.exists(image_path):
        print(f"错误: 文件不存在 - {image_path}")
        return
    
    try:
        # 准备文件
        files = {
            'image': ('test.jpg', open(image_path, 'rb'), 'image/jpeg')
        }
        
        # 发送请求
        print("正在发送请求...")
        response = requests.post(url, files=files)
        
        # 检查响应
        if response.status_code == 200:
            result = response.json()
            print("\n检测成功!")
            print(f"状态: {result['status']}")
            print(f"结果: {result['result']}")
            print(f"时间戳: {result['timestamp']}")
        else:
            print(f"\n请求失败 (状态码: {response.status_code})")
            print(f"错误信息: {response.json()}")
            
    except Exception as e:
        print(f"发生错误: {str(e)}")
    
if __name__ == "__main__":
    # 测试图片路径
    image_path = "test.jpg"
    test_detect_api(image_path)
