class Registor:
    def __init__(self, ohms):
        # 这个地方，也会调用这个属性的
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


class BoundedResistance(Registor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError("错误题目")
        self._ohms = ohms


class FixedResistance(Registor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")
        self._ohms = ohms


# r3 = BoundedResistance(10)
r4 = FixedResistance(1e3)
r4.ohms = 23
