#1
class Shape:
    def draw(self):
        print('Рисуем фигуру')
class Circle(Shape):
    def draw(self):
        print('Рисуем круг')
class Rectangle(Shape):
    def draw(self):
        print('Рисуем прямоугольник')
    
#2

class Counter:
    def __init__(self):
        self.count = 0
    def increment(self, value):
        self.count += value
    def get_value(self):
        return self.count
