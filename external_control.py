from flask import Flask, request, jsonify
from datetime import datetime

from agent import FILE_NAME


import asyncio

app = Flask(__name__)

loop: asyncio.AbstractEventLoop | None = None

msg_queue = asyncio.Queue(maxsize=1)


@app.route('/api/delivery/notification', methods=['POST'])
def handle_notification():
    # 获取 JSON 数据
    data = request.json

    # 验证必需字段
    required_fields = ['platform', 'location', 'phone', 'image_url', 'timestamp', 'original_sms']
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {','.join(required_fields)}"}), 400

    try:
        # 打印接收到的数据（实际使用时可以替换为数据库存储或其他处理）
        print("\n" + "=" * 50)
        print(f"[{datetime.now().isoformat()}] 收到外卖通知:")
        print(f"平台: {data['platform']}")
        print(f"位置: {data['location']}")
        print(f"电话: {data['phone']}")
        print(f"图片URL: {data['image_url']}")
        print(f"时间戳: {data['timestamp']}")
        print(f"原始短信: {data['original_sms']}")
        print("=" * 50)

        # 这里可以添加其他处理逻辑，如：
        # 1. 保存到数据库
        # 2. 发送给其他服务
        # 3. 触发通知等

        with open(FILE_NAME, "w", encoding="utf-8") as txt:
            txt.write(
                "Please go to (0.96, -2.02) and fetch me a screwdriver, then go to (0.37, -1.09) (yaw angle -180 degrees) here and give me the screwdriver.")

        return jsonify({
            "status": "success",
            "message": "Notification processed. Thank you kiwi agent :)",
            # "received_data": data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def main():
    app.run(host='0.0.0.0', port=17111, debug=True)


if __name__ == '__main__':
    main()
