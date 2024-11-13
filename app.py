from flask import Flask, request, jsonify
from detector import Processor
import os
import logging
from datetime import datetime

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化检测器
try:
    processor = Processor()
    logger.info("检测器初始化成功")
except Exception as e:
    logger.error(f"检测器初始化失败: {str(e)}")
    raise

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/detect', methods=['POST'])
def detect():
    try:
        # 检查是否有文件上传
        if 'image' not in request.files:
            return jsonify({'error': '没有上传图片'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
            
        # 保存上传的图片
        temp_path = 'temp.jpg'
        file.save(temp_path)
        logger.info(f"接收到图片: {file.filename}")
        
        # 进行检测
        result = processor.process(temp_path)
        logger.info(f"检测结果: {result}")
        
        # 删除临时文件
        os.remove(temp_path)
        
        return jsonify({
            'status': 'success',
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
