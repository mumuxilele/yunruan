# 云软通话记录服务

基于 Python Flask 的云软通话记录获取服务。

## 接口说明

### 获取通话录音地址

**请求地址**: `POST /ucc-phone/v1/pub/phone/getPath`

**请求参数**:
```json
{
    "sessionId": "会话ID"
}
```

**成功响应**:
```json
{
    "code": "0",
    "path": "http://component.im-cc.com/download/...",
    "detail": {
        "path": "http://component.im-cc.com/download/...",
        "phoneNumber": "08706631789",
        "callNumber": "18869404825",
        "sessionType": "3",
        "sessionId": "200337",
        "userId": "d17f03e571ff4add9bd82f3552cb3fbc",
        "waitTime": 0,
        "isAnswer": 2
    }
}
```

**失败响应**:
```json
{
    "code": "非0",
    "reason": "错误原因"
}
```

## 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| YUNRUAN_HOST | u.im-cc.com | 云软API域名 |
| PORT | 5000 | 服务端口 |
| DEBUG | false | 调试模式 |

## 运行方式

### 开发环境
```bash
pip install -r requirements.txt
python app.py
```

### 生产环境
```bash
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker
```bash
docker build -t yunruan-service .
docker run -p 5000:5000 yunruan-service
```

## 健康检查

**地址**: `GET /health`

**响应**: `{"status": "ok"}`
