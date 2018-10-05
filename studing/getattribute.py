class Color:
    red = 'red'

    def __getattr__(self, item):
        print("getattr is being called")
        return 'whatever'

    def __getattribute__(self, item):
        print("getattribute is being called")
        return super().__getattribute__(item)


color = Color()
print(color.red)
print(color.blue)
