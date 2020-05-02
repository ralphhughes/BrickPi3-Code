# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

if __name__ == "__main__":
    print("Hello World")

class Test:
    a = None
    b = None

    def __init__(self, a):
        print(self.a)
        self.a = a
        self._x = 123
        self.__y = 123
        b = 'meow'

    def func1(self):
        print("a: {}".format(self.a))
        print("b: {}".format(self.b))