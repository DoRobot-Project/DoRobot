import zmq
import threading
import time

class Coordinator:
    def __init__(self, bind_address="ipc:///tmp/DoRobot-coordinator"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)  # 支持多客户端连接
        self.socket.bind(bind_address)
        self.nodes = {}  # 存储节点信息: {node_id: last_heartbeat_time}
        self.lock = threading.Lock()
        print(f"DoRobot-Coordinator Start, IPC Address: {bind_address}")

    def start(self):
        # 启动心跳检查线程
        threading.Thread(target=self.heartbeat_monitor, daemon=True).start()
        # 处理客户端请求
        while True:
            ident, msg = self.socket.recv_multipart()
            print(f"收到消息来自 {ident}: {msg}")
            if msg == b"REGISTER":
                self.register_node(ident)
            elif msg.startswith(b"TASK_RESULT"):
                self.handle_task_result(ident, msg)
            else:
                self.forward_task(ident, msg)

    def register_node(self, node_id):
        with self.lock:
            self.nodes[node_id] = time.time()
            print(f"节点 {node_id} 注册成功")

    def heartbeat_monitor(self):
        while True:
            time.sleep(5)  # 每5秒检查一次
            now = time.time()
            with self.lock:
                dead_nodes = [node_id for node_id, last_time in self.nodes.items() if now - last_time > 10]
                for node_id in dead_nodes:
                    print(f"节点 {node_id} 已离线，触发故障恢复")
                    del self.nodes[node_id]

    def forward_task(self, node_id, task):
        # 简单示例：直接回复任务结果
        self.socket.send_multipart([node_id, b"TASK_ACK"])

    def handle_task_result(self, node_id, result):
        print(f"节点 {node_id} 完成任务，结果: {result}")

if __name__ == "__main__":
    coord = Coordinator()
    coord.start()