#1
class Vehice:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    def info(self):
        print(f'Марка: {self.brand}, модель: {self.model}')

class Car(Vehice):
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
    def info(self):
        print(f'Марка: {self.brand}, модель: {self.model}, Год: {self.year}')

#2
class Parent:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
    def get_full_name(self):
        print(f'Имя: {self.first_name}, фамилия: {self.last_name}')
class Mother(Parent):
    def __init__(self, first_name, last_name, child_count):
        self.first_name = first_name
        self.last_name = last_name
        self.child_count = child_count
    def get_child_count(self):
        print(f'Количество детей: {self.child_count}')
class Father(Parent):
    def __init__(self, first_name, last_name, child_count):
        self.first_name = first_name
        self.last_name = last_name
        self.child_count = child_count
    def get_child_count(self):
        print(f'Количество детей: {self.child_count}')
