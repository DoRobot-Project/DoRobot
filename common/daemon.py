import zmq
import time
import random
import threading

class Daemon:
    def __init__(self, node_id: str, coordinator_address="ipc:///tmp/coordinator", ipc_address=None):
        self.node_id = node_id.encode()  # 转换为 bytes
        self.coordinator_address = coordinator_address
        self.ipc_address = ipc_address or f"ipc:///tmp/node{random.randint(0, 999)}"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.IDENTITY, self.node_id)  # 设置唯一标识
        self.socket.connect(self.coordinator_address)
        print(f"Daemon {self.node_id} 启动，地址: {self.ipc_address}")

    def start(self):
        # 注册到 Coordinator
        self.socket.send(b"REGISTER")
        print(f"{self.node_id} 已注册到 Coordinator")

        # 发送心跳线程
        threading.Thread(target=self.send_heartbeat, daemon=True).start()

        # 监听任务
        while True:
            try:
                task = self.socket.recv()
                print(f"{self.node_id} 收到任务: {task}")
                self.process_task(task)
            except Exception as e:
                print(f"{self.node_id} 任务处理出错: {e}")

    def send_heartbeat(self):
        while True:
            time.sleep(3)  # 每3秒发送一次心跳
            self.socket.send(b"HEARTBEAT")
            print(f"{self.node_id} 发送心跳")

    def process_task(self, task):
        # 模拟任务处理
        time.sleep(2)
        result = f"TASK_RESULT: {task.decode()}"
        self.socket.send(result.encode())

if __name__ == "__main__":
    daemon = Daemon(node_id="node0")
    daemon.start()