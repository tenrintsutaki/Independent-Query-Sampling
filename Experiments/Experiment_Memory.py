import sys


if __name__ == '__main__':
    a = 1000000
    print(sys.getsizeof(a))  # 输出会是 28 字节或更多，取决于 Python 版本和系统架构