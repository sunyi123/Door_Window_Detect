# 门窗检测 API 文档

## API 概述

本API服务提供门窗图片质量检测功能,可以判断图片是否合格、模糊或不合格。

## 基础信息

- 基础URL: `http://localhost:5000`
- 支持格式: JSON
- 请求方式: POST

## API 端点

### 1. 健康检查

检查API服务是否正常运行。

- URL: `/health`
- 方法: `GET`
- 请求参数: 无

**响应示例:**
```json
{
    "status": "healthy",
    "timestamp": "2024-11-12T19:56:59.123456"
}
```

### 2. 图片检测

对上传的图片进行门窗检测。

- URL: `/detect`
- 方法: `POST`
- Content-Type: `multipart/form-data`

**请求参数:**

| 参数名 | 类型 | 必选 | 描述 |
|--------|------|------|------|
| image  | file | 是   | 要检测的图片文件(支持jpg/jpeg/png) |

**响应参数:**

| 参数名 | 类型 | 描述 |
|--------|------|------|
| status | string | 处理状态("success"/"error") |
| result | string | 检测结果("合格"/"不合格"/"模糊") |
| timestamp | string | 处理时间戳(ISO格式) |
| error | string | 错误信息(仅在发生错误时返回) |

**成功响应示例:**
```json
{
    "status": "success",
    "result": "合格",
    "timestamp": "2024-11-12T19:56:59.123456"
}
```

**错误响应示例:**
```json
{
    "error": "没有上传图片",
    "timestamp": "2024-11-12T19:56:59.123456"
}
```

**状态码:**
- 200: 请求成功
- 400: 请求参数错误
- 500: 服务器内部错误

## 调用示例

### Python示例:
```python
import requests

def detect_image(image_path):
    url = 'http://localhost:5000/detect'
    files = {
        'image': ('image.jpg', open(image_path, 'rb'), 'image/jpeg')
    }
    
    response = requests.post(url, files=files)
    return response.json()

# 使用示例
result = detect_image('/path/to/image.jpg')
print(result)
```

### curl示例:
```bash
curl -X POST -F "image=@/path/to/image.jpg" http://localhost:5000/detect
```

## 部署说明


1. 启动服务:
```bash
python app.py
```

服务默认运行在 `http://localhost:5000`

## 注意事项

1. 图片格式支持:
   - 支持 jpg、jpeg、png 格式
   - 建议图片大小不超过 16MB

2. 性能说明:
   - 单次请求处理时间约 1-2 秒
   - 建议单服务器并发请求不超过 10 个

3. 错误处理:
   - 所有错误都会返回详细的错误信息
   - 建议实现请求重试机制

## 错误代码说明

| 错误代码 | 描述 | 解决方案 |
|----------|------|----------|
| 400 | 没有上传图片 | 确保请求中包含image字段 |
| 400 | 无效的文件类型 | 检查图片格式是否正确 |
| 500 | 服务器处理错误 | 检查日志并联系管理员 |

## 更新日志

### v1.0.0 (2024-11-12)
- 初始版本发布
- 支持基础的门窗检测功能
- 添加健康检查接口
