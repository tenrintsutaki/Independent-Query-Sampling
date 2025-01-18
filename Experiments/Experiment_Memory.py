import sys


if __name__ == '__main__':
    a = 1000000
    l = [0 for i in range(a)]
    print(sys.getsizeof(a))  # 输出会是 28 字节或更多，取决于 Python 版本和系统架构
    print(sys.getsizeof(l) // (1024 * 1024)) # 8 MB