class BuilderBaseClass:
    '''
    этот базовый класс нужен для того, чтобы нащ метод позволяющий класть что-то на любой увроень вложенности
    был у всех будущих билдеров, которые он него отнаследуются
    '''
    def __init__(self):
        self.result = {}
    def update_inner_value(self,key,value):
        '''
        проарпгрейженая функция update_inner_generator для обновления обполей объекта на любом уровне вложенности
        '''
        if not isinstance(key,list): #случай для верхнего уровня, для кейса когда ключ есть строка по факту
            self.result[key] = value
        else:
            temp = self.result #определяем где ммы сейчас находимся
            for item in key[:-1]: #удаляем из выборки последний элемент, потому что именно ему будет присваиваться последнее значение
                if item not in temp.keys(): #если такого ключа нет
                    temp[item] = {}  # то создаем пустой объект
                temp = temp[item] #и потом в любом случае проваливаемся на уровень вниз
            temp[key[-1]] = value #когда мы провалились до нужного элемента то кладем туда наше значение, или перетираем или создаем
        return self

    def build(self):
        return self.result