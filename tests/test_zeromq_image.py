import zmq
import threading
import pyarrow as pa
from dora import Node
import json
import base64
import cv2
import numpy as np

# IPC Address
ipc_address = "ipc:///tmp/dora-zeromq"

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect(ipc_address)
socket.setsockopt(zmq.RCVTIMEO, 100)  # 设置接收超时（毫秒）

running_server = True
images = {}  # 缓存每个 event_id 的最新帧
lock = threading.Lock()  # 线程锁

def recv_server():
    """接收数据线程"""
    while running_server:
        try:
            # message = socket.recv_json()
            # event_id = message["event_id"]
            # encoded_buffer = message["buffer"]

            # # 解码 base64 数据
            # buffer_bytes = base64.b64decode(encoded_buffer)
            # # received_buffer = pa.Buffer.from_pybytes(buffer_bytes)

            # # 处理接收到的数据
            # print(f"Received event: {event_id}")
            # print(f"Buffer size: {len(buffer_bytes)} bytes")

            # # 转换为 numpy 数组用于 OpenCV 解码
            # # img_data = received_buffer.to_pybytes()
            # img_array = np.frombuffer(buffer_bytes, dtype=np.uint8)
            # frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            # if frame is not None:
            #     with lock:
            #         images[event_id] = frame


            message_parts = socket.recv_multipart()
            if len(message_parts) < 2:
                continue  # 协议错误

            event_id = message_parts[0].decode('utf-8')
            buffer_bytes = message_parts[1]

            # 解码图像
            img_array = np.frombuffer(buffer_bytes, dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if frame is not None:
                with lock:
                    images[event_id] = frame
        except zmq.Again:
            # 接收超时，继续循环
            print(f"Received Timeout")
            continue
        except Exception as e:
            print("recv error:", e)
            break



def display_loop():
    """显示循环"""
    global running_server
    last_shown = {}  # 记录已显示的帧

    while running_server:
        with lock:
            for event_id, frame in images.items():
                if event_id not in last_shown or not np.array_equal(last_shown[event_id], frame):
                    window_name = f"Event ID: {event_id}"
                    try:
                        cv2.imshow(window_name, frame)
                        last_shown[event_id] = frame.copy()
                    except Exception as e:
                        print(f"Display error for {event_id}: {e}")

        if cv2.waitKey(30) == ord('q'):
            running_server = False
            break

if __name__ == "__main__":
    print("Starting receiver server...")
    try:
        # 启动接收线程
        recv_thread = threading.Thread(target=recv_server, daemon=True)
        recv_thread.start()

        # 启动显示循环
        display_loop()

    except KeyboardInterrupt:
        print("Shutting down...")
        running_server = False
        cv2.destroyAllWindows()
