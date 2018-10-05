class Color:
    red = 'red'

    def __getattr__(self, item):
        # 在实例没有item属性的时候，调用该方法
        print("getattr is being called")
        return 'whatever'

    def __getattribute__(self, item):
        # 实例有没有item属性，都会调用该方法
        print("getattribute is being called")
        return super().__getattribute__(item)


color = Color()
print(color.red)
print(color.blue)
