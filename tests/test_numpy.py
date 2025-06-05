import numpy as np
import sys
import time

# 1. 基础数据结构创建
# 列表（可变）
py_list = [[1, 2, 3], [4, 5, 6]]
# 元组（不可变）
py_tuple = ((1, 2, 3), (4, 5, 6))
# numpy数组（可变，同质）
np_array = np.array(py_list)

print("=== 基础信息对比 ===")
print(f"列表类型: {type(py_list)}")
print(f"元组类型: {type(py_tuple)}")
print(f"数组类型: {type(np_array)}\n")

print("=== 数据结构内容 ===")
print(f"列表: {py_list}")
print(f"元组: {py_tuple}")
print(f"数组:\n{np_array}\n")

# 2. 可变性对比
print("=== 可变性测试 ===")
# 列表修改
py_list[0][0] = 100
print(f"修改后的列表: {py_list}")

# 元组修改（会抛出异常）
try:
    py_tuple[0] = (100, 2, 3)
except TypeError as e:
    print(f"元组修改错误: {e}")

# 数组修改
np_array[0,0] = 100
print(f"修改后的数组:\n{np_array}\n")

# 3. 内存效率对比
print("=== 存占用对比 ===")
print(f"列表内存占用: {sys.getsizeof(py_list)} bytes")
print(f"数组内存占用: {np_array.nbytes} bytes (实际数据) + {sys.getsizeof(np_array)} bytes (对象)\n")

# 4. 操作支持对比
print("=== 操作支持对比 ===")
# 数学运算
list_squared = [[x**2 for x in row] for row in py_list]
array_squared = np_array**2

print(f"列表平方运算: {list_squared}")
print(f"数组平方运算:\n{array_squared}\n")

# 5. 性能对比测试
print("=== 性能对比测试 ===")
size = 1000000
# 创建测试数据
list_data = list(range(size))
array_data = np.arange(size)

# 列表求和
start = time.time()
sum(list_data)
print(f"列表求和耗时: {time.time()-start:.5f}s")

# 数组求和
start = time.time()
np.sum(array_data)
print(f"数组求和耗时: {time.time()-start:.5f}s")