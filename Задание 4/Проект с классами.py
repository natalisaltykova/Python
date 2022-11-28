class Head:
    def __init__(self,tvor,nauch):
        self.tvor = tvor
        self.nauch = nauch
    def start():
        tvor = int(input('Введите количество мероприятий: '))
        nauch = int(input('Введите количество научных статей: '))
        tvor1 = tvor * 150
        nauch1 = nauch * 250
        soc = 1500
        akad = 2620
        if int(input('Вы из малоимущей семьи или имеете другие основания для социальной стипендии').lower() == "да"):
            print('Ваша стипендия составляет: ', akad + tvor1 + nauch1 + soc, "рублей")
        else:
            print('Ваша стипендия составляет: ', akad + tvor1 + nauch1, "рублей")
Head.start()