import sys

# 存储一个整数
integer_value = 4
int_memory_size = sys.getsizeof(integer_value)

# 存储一个对象的引用（这里我们用一个简单的列表作为例子）
object_reference = []
ref_memory_size = sys.getsizeof(object_reference)

print(f"Memory size of integer: {int_memory_size} bytes")
print(f"Memory size of object reference: {ref_memory_size} bytes")