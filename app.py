"""
云软通话记录获取服务
用于获取云软平台的通话录音地址

接口地址: POST /ucc-phone/v1/pub/phone/getPath
请求参数: {"sessionId": "会话ID"}
返回: {"code": "0", "reason": "", "detail": [{"path": "录音地址", ...}]}
"""

from flask import Flask, request, jsonify
import requests
import logging
import os

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 云软API配置
YUNRUAN_HOST = os.environ.get('YUNRUAN_HOST', 'u.im-cc.com')
YUNRUAN_API_URL = f"https://{YUNRUAN_HOST}/ucc-phone/v1/pub/phone/getPath"


@app.route('/ucc-phone/v1/pub/phone/getPath', methods=['POST'])
def get_phone_path():
    """
    获取通话录音地址
    
    请求参数:
        sessionId: 会话ID
        
    返回:
        成功: {"code": "0", "detail": [{"path": "录音地址", ...}]}
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
        
        session_id = data.get('sessionId')
        if not session_id:
            return jsonify({
                "code": "1",
                "reason": "sessionId参数不能为空"
            })
        
        logger.info(f"云软通话记录获取地址：{YUNRUAN_API_URL}，请求参数：sessionId={session_id}")
        
        # 调用云软API
        response = requests.post(
            YUNRUAN_API_URL,
            json={"sessionId": session_id},
            headers={
                "Content-Type": "application/json"
            },
            timeout=30
        )
        
        logger.info(f"云软返回字符串responseStr：{response.text}")
        
        # 解析响应
        result = response.json()
        
        # 检查返回码
        if result.get('code') != '0':
            reason = result.get('reason', '未知错误')
            logger.info(f"未获取到数据，返回码：{result.get('code')}，原因：{reason}")
            return jsonify(result)
        
        # 获取通话记录详情
        detail = result.get('detail', [])
        if not detail or len(detail) == 0:
            return jsonify({
                "code": "1",
                "reason": "未获取到通话记录"
            })
        
        # 返回第一条记录的path
        history_obj = detail[0]
        path = history_obj.get('path', '')
        
        logger.info(f"云软解析对象historyObj：{history_obj}")
        
        return jsonify({
            "code": "0",
            "path": path,
            "detail": history_obj
        })
        
    except requests.exceptions.Timeout:
        logger.error("云软API请求超时")
        return jsonify({
            "code": "2",
            "reason": "请求超时"
        })
    except requests.exceptions.RequestException as e:
        logger.error(f"云软API请求异常: {e}")
        return jsonify({
            "code": "3",
            "reason": f"请求异常: {str(e)}"
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
        "endpoints": {
            "get_path": "POST /ucc-phone/v1/pub/phone/getPath",
            "health": "GET /health"
        }
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
