class Color:
    red = 'red'
    blue = 'blue'

    def __getattr__(self, item):
        print("item is {}".format(item))
        print("getattr is being called")
        return 'whatever'

    def __getattribute__(self, item):
        print("getattribute is being called")
        return super().__getattribute__(item)


c = Color()
print(c.red)
print('*' * 10)
print(c.haha)
