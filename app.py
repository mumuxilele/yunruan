"""
云软通话记录获取服务
用于获取云软平台的通话录音地址

接口地址: POST /ucc-phone/v1/pub/phone/getPath
请求参数: {"sessionId": "会话ID"}
返回: {"code": "0", "path": "录音地址", ...}
"""

from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 固定的录音地址（测试用）
FIXED_MP3_PATH = "https://wojiaccloud-1252177460.file.myqcloud.com/5c4969cb51394395b25e78d1dac2f3e0/2026-01-09/mp3/fa3e490c3c664c4b9b6d1e6de3f38143.mp3"


@app.route('/ucc-phone/v1/pub/phone/getPath', methods=['POST'])
def get_phone_path():
    """
    获取通话录音地址
    
    请求参数:
        sessionId: 会话ID
        
    返回:
        成功: {"code": "0", "path": "录音地址", "sessionId": "...", ...}
        失败: {"code": "非0", "reason": "原因"}
    """
    try:
        # 获取请求参数
        data = request.get_json()
        if not data:
            return jsonify({
                "code": "1",
                "reason": "请求参数为空"
            })
        
        session_id = data.get('sessionId', '')
        
        logger.info(f"请求参数: sessionId={session_id}")
        
        # 返回固定的录音地址
        return jsonify({
            "code": "0",
            "reason": "",
            "path": FIXED_MP3_PATH,
            "phoneNumber": "13800138000",
            "sessionId": session_id,
            "duration": 180,
            "caller": "13800138000",
            "callee": "13900139000",
            "callTime": "2026-04-23 10:30:00"
        })
        
    except Exception as e:
        logger.error(f"服务器内部错误: {e}")
        return jsonify({
            "code": "4",
            "reason": f"服务器内部错误: {str(e)}"
        })


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({"status": "ok"})


@app.route('/', methods=['GET'])
def index():
    """首页"""
    return jsonify({
        "service": "云软通话记录服务",
        "version": "1.0.0",
        "mock": True,
        "fixed_path": FIXED_MP3_PATH,
        "endpoints": {
            "get_path": "POST /ucc-phone/v1/pub/phone/getPath",
            "health": "GET /health"
        }
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
