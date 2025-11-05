import threading

class tail_rec_exec(tuple): pass

class tail_rec:
    def __init__(self, func):
        self.func = func

    def call(self, *args, **kwargs):
        return tail_rec_exec((self.func, args, kwargs))

    def __call__(self, *args, **kwargs):
        r = self.func(*args, **kwargs)
        while isinstance(r, tail_rec_exec):
            func, args, kwargs = r
            r = func(*args, **kwargs)
        return r

class smart_tail_rec(tail_rec):
    data = threading.local()
    data.calling = False

    def __call__(self, *args, **kwargs):
        if self.data.calling:
            return self.call(*args, **kwargs)
        try:
            self.data.calling = True
            return super().__call__(*args, **kwargs)
        finally:
            self.data.calling = False

if __name__ == '__main__':
    @tail_rec
    def my_sum(values, acc=0):
        if not values:
            return acc
        return my_sum.call(values[1:], acc + values[0])

    @smart_tail_rec
    def factorial(n, acc=1):
        if not n:
            return acc
        return factorial(n - 1, acc * n)

    @smart_tail_rec
    def even(n):
        if not n:
            return True
        return odd(n - 1)

    @smart_tail_rec
    def odd(n):
        if not n:
            return False
        return even(n - 1)

    print(my_sum(range(5000)))
    print(factorial(5000))
    print(factorial(5))
    print(even(5000))
    print(odd(5000))
    print(even(5001))
    print(odd(5001))
