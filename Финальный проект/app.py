import json

class Record(): #класс для связи препода и ученика
    def __init__(self,id, client, teacher,date,time): #конструтор, описываем поля класса
        self.id = id
        self.client = client
        self.teacher = teacher
        self.date = date
        self.time = time

    def getToJson(self): #метод для преобразования свойст у объекта в словарь
        return {"client":self.client.id, 'teacher':self.teacher.id, "date":self.date, "time":self.time}

    def __str__(self): #переобпределяем метод str для печати объекта класса на экран в красивом формате
        return self.client+'-'+self.teacher

    def __repr__(self): #переобпределяем метод repr для печати объекта класса на экран в красивом формате
        return f'Records(id={self.id},client={self.client}, teacher={self.teacher},date={self.date},time={self.time})'

class Client(): #класс для создания объектов ученика и хранение инфмормации о нем
    def __init__(self, id, name, time, phone):
        self.id = id
        self.name = name
        self.time = time
        self.phone = phone

    def getToJson(self):
        return {"name":self.name, 'time':self.time, "phone":self.phone}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Client(id={self.id}, name={self.name}, time={self.time}, phone={self.phone})'

class Teacher(): #класс для создания объектов учителя и хранение инфмормации о нем и управлением
    def __init__(self,id, name, dates):
        self.id = id
        self.name = name
        self.dates = dates

    def write(self, teacher): #метод для записи ученика к учителю (объекту этого класса)
        db.records.append(Record(self,teacher,teacher.date,teacher.time))

    def getToJson(self):
        return {"name":self.name, 'dates':self.dates}

    def addDate(self, date): #Создание новой даты(ключа и занчения для), для свойства dates (словаря)
        self.dates[date] = []

    def addTime(self, date, time): #Добавление нового времени(элемент списка), для свойства dates (словаря, по ключу)
        self.dates[date].append(time)
    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Teacher(id={self.id},name={self.name}, dates={self.dates})'

class BaseDb(): #класс для работы со списком объектов класса Teacher, Client и Records
    def __init__(self):
        self.clients = [] #список с объектами класса Client
        self.teachers = [] #список с объектами класса Teacher
        self.records = [] #список с объектами класса Records

        with open('clients.json', 'r', encoding='utf-8') as f: #читаем клиентов из файла json
            self.clients_json = json.load(f) #записываем в свойства класса весь словарь со всеми клиентами
        for client_id in self.clients_json: #перебираем, создаем объект класса Cleitn и добавляем в список с клиентами
            self.clients.append(Client(client_id, self.clients_json[client_id]['name'], self.clients_json[client_id]['time'], self.clients_json[client_id]['phone']))


        with open('teachers.json', 'r', encoding='utf-8') as f: # аналогично как с клиентами
            self.teachers_json = json.load(f)
        for teacher_id in self.teachers_json:
            self.teachers.append(Teacher(teacher_id, self.teachers_json[teacher_id]["name"],self.teachers_json[teacher_id]["dates"]))


        with open('dates.json', 'r', encoding='utf-8') as f: #аналогично как с клиентами
            self.records_json = json.load(f)
        for record in self.records_json: #перебираем, создаем объект класса record и добавляем в список с записями
            c =self.getClientById(self.records_json[record]['client']) # поулчаем объект клиента по его айди
            t =self.getTeacherById(self.records_json[record]['teacher']) # поулчаем объект учителя по его айди
            if c != None and t != None :
                self.records.append(Record(record, c, t, self.records_json[record]['date'], self.records_json[record]['time']))

    def saveFile(self, filename, data): #метод для перезаписи конкретного файла
        with open(filename, 'w', encoding='utf-8') as f:
            return json.dump(data, f, ensure_ascii=False, indent=4)

    def write_client(self, teacher, name, phone, date, time): #метод для запися клиентов к учителю
        clinet_last_id = str(int(self.clients[len(self.clients)-1].id) + 1) #получаем айди последней записи в нашей "Бд" с клиентами
        c = Client(clinet_last_id, name, time, phone)#созадем объект клиента
        self.clients.append(c)#добавляем в список с клиентами
        record_last_id = str(int(self.records[len(self.records)-1].id) + 1) #получаем айди последней записи в нашей "Бд" с записями
        r = Record(record_last_id,c, teacher,date, time) #созадем объект записи
        self.records.append(r)#добавляем в список с записяси
        db.save()#сохраняем

    def save(self): #метод для сохранения всей бд по файлам
        self.teachers_json = {}
        for t in self.teachers:
            self.teachers_json[t.id] = t.getToJson()

        self.clients_json = {}
        for c in self.clients:
            self.clients_json[c.id] = c.getToJson()

        self.records_json = {}
        for r in self.records:
            self.records_json[r.id] = r.getToJson()
        self.saveFile('clients.json', self.clients_json)
        self.saveFile('dates.json', self.records_json)
        self.saveFile('teachers.json', self.teachers_json)

    def getClientByName(self, name): #метод для получения обхекта клиента по его имени
        for c in self.clients:
            if name == c.name: return c

    def getClientById(self, id): #метод для получения обхекта клиента по его айди
        for c in self.clients:
            if id == c.id: return c

    def getTeacherByName(self, name):#метод для получения обхекта тичера по его имени
        for t in self.teachers:
            if name == t.name: return t

    def getTeacherById(self, id): #метод для получения обхекта тичера по его айди
        for t in self.teachers:
            if id == t.id: return t

    def getAllTeacherDates(self, t): #метод для получения всех дат у объекта учителя
        dates = list(t.dates.keys())
        dates.sort()
        return dates
    def getAllTeachers (self): #метод для получения имен всех учителей
        teachers = []
        for t in self.teachers:
             teachers.append(t.name)
        return '- '+'\n- '.join(teachers)

    def getFreeTime(self, t, date): # анализирует все время у преподавателя (проверяет наличии записи у учеников к этому преподу на эту дату) и выводит только свободные часы
        busy_times = []
        for t2 in t.dates[date]:
            for r in self.records:
                if r.teacher == t:
                    if r.time == t2:
                        busy_times.append(t2)


        free_times = list(set(t.dates[date]).difference(set(busy_times)))
        return sorted(free_times, key=lambda d: tuple(map(int, d.split(":")))) #сортируем и возвращаем

db = BaseDb() #создаем объект класса бд

def write_client(): # функция записать ученика к преподу
    print('Наши преподаватели')
    print(db.getAllTeachers())

    while True:
        teacher_name = input('Введите фамилию преподавателя: ')
        t = db.getTeacherByName(teacher_name)
        if t == None:
            print("Такого преподавлятеля не существует!")
        else:
            break
    free_dates = db.getAllTeacherDates(t)
    print('Выберите дату из возможных:', ', '.join(free_dates))

    while True:
        teacher_date = input('Введите дату: ')

        if teacher_date not in free_dates:
            print('Текущая дата недоступна, попробуйте снова!')
        else:
            break

    free_times = db.getFreeTime(t,teacher_date)
    if len(free_times) > 0:
        print("Свободное время у", teacher_name, ', '.join(free_times))
        while True:
            teacher_time = input('Введите время (0 - выход): ')

            if teacher_time in free_times:
                client_name = input('Введите вашу фамилию и имя: ')
                client_phonenumber = input('Введите ваш номер телефона: ')
                db.write_client(t,client_name, client_phonenumber,teacher_date,teacher_time )
                print("Вы успешно записались!")
                break
            else:
                print("Не верно введено время, попробуйте снова!")
    else:
        print("У преподавателя", teacher_name, "на эту дату", teacher_date,
              "нет свободного времени (выберите другую дату)")

def edit_teacher(): # Редактировать распсиание
    while True:
        teacher_name = input('Введите вашу фамилию: ')
        t = db.getTeacherByName(teacher_name)
        if t == None:
            print("Такого преподавлятеля не существует!")
        else:
            break
    while True:
        teacher_date = input('Введите дату, например 12.12.2022 (0 - выйти): ')
        if teacher_date == '0':
            break
        if teacher_date not in t.dates:
            t.addDate(teacher_date)
        while True:
            teacher_hour = input('Введите свободное время (0 - выйти): ')
            if teacher_hour == '0':
                break
            t.addTime(teacher_date,teacher_hour)
        db.save()
    print("Расписание успешно обновлено!")

def view_clients(): # Посмотреть своих учеников
    while True:
        teacher_name = input('Введите вашу фамилию: ')
        t = db.getTeacherByName(teacher_name)
        shudele = {}
        if t != None:
            for d in t.dates: #перебираем все даты
                for r in db.records: #перебираем все запсии
                    if r.teacher == t: #проверяем конкретного учителя у записи
                        if d not in shudele: #проверем если такой даты нет ещё то создаем список
                            shudele[d] = []
                        for time in t.dates[d]:#перебираем все время в эту дату
                            if r.time == time:
                                shudele[d].append("    " + str(time) + " - " + str(r.client)) #добавляем время в список по ключу даты

            for d in shudele: #перебираем все даты поулчившиеся
                if len(shudele[d]) > 0:
                    print(d) #выводим дату
                    for t in shudele[d]:
                        print(t) #выводим время
            break

        else:
            print("Такой фамилии не существует!")

def teacher_write_client(): # Препод записывает ученика самостоятельно
    while True:
        teacher_name = input('Введите вашу фималию: ')
        t = db.getTeacherByName(teacher_name)
        if t == None:
            print("Такого преподавлятеля не существует!")
        else:
            break
    client_name = input('Введите фамилию ученика: ')
    c = db.getClientByName(client_name)

    while True:
        teacher_date = input('Введите дату, например 12.12.2022 (0 - выйти): ')
        if teacher_date == '0':
            break
        if teacher_date not in t.dates:
            t.addDate(teacher_date)
        while True:
            teacher_time = input('Введите свободное время (0 - выйти): ')
            if teacher_time == '0':
                break

            t.addTime(teacher_date,teacher_time)
            record_last_id = str(int(db.records[len(db.records) - 1].id) + 1)
            if c == None:
                db.write_client(t, client_name, '', teacher_date, teacher_time)
            c = db.getClientByName(client_name) #созадем объект клиента
            r = Record(record_last_id, c, t, teacher_date, teacher_time) #создаем объект хаписи использую учителя и созданный объект клиента
            db.records.append(r)
            db.save() #сохраняем

            print("Расписание успешно обновлено!")

def print_price():
    print("""\nПрайслист:
Пробное занятие- 400 руб
50 минут урок- 1000 руб (абонемент на 4 урока- 3700 руб, 8 уроков- 6900 руб)
1 час урок- 1100 руб (абонемент на 4 урока- 4000 руб, на 8 уроков- 7000)
Детские занятия- 800 руб (абонемент 4 занятия- 3000 руб.)\n""")

def main(): #меню для пользователя
    while True:
        print('1 - записаться на занятие\n2 - для преподавателей\n3 - прайслист\n0 - выйти')
        answer = input("Ваш выбор: ")
        if answer =='0':
            break
        elif answer == '1':
            write_client()
        elif answer == '2':
            while True:
                print('1 - редактировать расписание\n2 - просмотреть свое расписание\n3 - записать ученика\n0 - выйти')
                answer2 = input("Ваш выбор: ")
                if answer2 == '0':
                    break
                elif answer2 == '1':
                    edit_teacher()
                elif answer2 == '2':
                    view_clients()
                elif answer2 == '3':
                    teacher_write_client()
        elif answer == '3':
            print_price()

main()
