class A:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return '<{}, {}>'.format(self.a, self.b)


if __name__ == '__main__':
    a = A(1, 2)
    print(a)
