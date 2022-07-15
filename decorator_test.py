import time
from multiprocessing import Process, Queue
from functools import wraps

# 使用类装饰器会提示is not the same object as __main__.print_message
class Timer():
    def __init__(self, func):
        self.func = func
        print(wraps(func))
        self.__dict__.update()

    def __call__(self, *args, **kwargs):
        t0 = time.time()
        result = self.func(*args, **kwargs)
        print(time.time() - t0)
        return result

def timer(func):
    # 如果没有wraps会提示can't pickle
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        print(time.time() - t0)
        return result
    return wrapper

@Timer
def print_message(queue:Queue):
    while(True):
        message = queue.get()
        if message == -1:
            return
        print(message)

if __name__ == '__main__':
    q = Queue()
    process = Process(target=print_message, args=(q,))
    process.start()

    ls = [1, 2, 3, 5, 6, 7, -1]
    for item in ls:
        q.put(item)