# import zmq
# import threading

# # IPC 地址（需唯一且可访问）
# ipc_address = "ipc:///tmp/pyzmq_p2p_example"

# def server():
#     """服务端：接收消息并回复"""
#     context = zmq.Context()
#     socket = context.socket(zmq.PAIR)  # 创建 PAIR 套接字（双向通信）
#     socket.bind(ipc_address)          # 绑定到指定 IPC 地址
    
#     print("Server: 等待连接...")
#     message = socket.recv_string()    # 接收客户端消息
#     print(f"Server: 收到消息: {message}")
    
#     socket.send_string("Server 已收到你的消息")  # 发送响应
#     socket.close()
#     context.term()

# def client():
#     """客户端：发送消息并接收回复"""
#     import time
#     time.sleep(1)  # 确保服务端先启动
    
#     context = zmq.Context()
#     socket = context.socket(zmq.PAIR)
#     socket.connect(ipc_address)       # 连接到服务端的 IPC 地址
    
#     socket.send_string("Hello from Client")  # 发送消息
#     reply = socket.recv_string()      # 接收响应
#     print(f"Client: 收到回复: {reply}")
    
#     socket.close()
#     context.term()

# if __name__ == "__main__":
#     # 启动服务端线程
#     server_thread = threading.Thread(target=server)
#     server_thread.start()
    
#     # 启动客户端线程
#     client_thread = threading.Thread(target=client)
#     client_thread.start()
    
#     # 等待线程结束
#     server_thread.join()
#     client_thread.join()



#########################################################


import zmq
import threading
import time

# 所有节点的 IPC 地址列表（你可以改为 TCP 地址用于网络通信）
node_addresses = [
    "ipc:///tmp/node0",
    "ipc:///tmp/node1",
    "ipc:///tmp/node2"
]

def node(node_id):
    context = zmq.Context()

    # ROUTER 套接字用于监听并接收来自其他节点的消息
    router_socket = context.socket(zmq.ROUTER)
    router_socket.setsockopt_string(zmq.IDENTITY, f"Node{node_id}")  # 设置唯一 ID
    router_socket.bind(node_addresses[node_id])  # 绑定自己的地址

    # DEALER 套接字用于连接其他节点以发送消息
    dealer_sockets = {}
    for i, addr in enumerate(node_addresses):
        if i != node_id:
            dealer = context.socket(zmq.DEALER)
            dealer.setsockopt_string(zmq.IDENTITY, f"Node{node_id}")
            dealer.connect(addr)
            dealer_sockets[i] = dealer

    print(f"[Node{node_id}] 启动并连接其他节点")

    # 接收线程：处理来自其他节点的消息
    def receiver():
        while True:
            sender_id = router_socket.recv_string()
            msg = router_socket.recv_string()
            print(f"[Node{node_id}] 收到来自 {sender_id} 的消息: {msg}")

    # 发送函数：循环发送消息给其他节点
    def send_messages():
        count = 0
        while True:
            for target_id, dealer in dealer_sockets.items():
                msg = f"Hello from Node{node_id} - {count}"
                dealer.send_string(msg)
                print(f"[Node{node_id}] 发送给 Node{target_id}: {msg}")
            count += 1
            time.sleep(2)

    # 启动接收线程
    threading.Thread(target=receiver, daemon=True).start()

    # 主线程执行发送任务
    send_messages()

if __name__ == "__main__":
    # 启动多个节点
    for i in range(len(node_addresses)):
        threading.Thread(target=node, args=(i,)).start()