documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
        {"type": "Паспорт", "number": "5000 132456", "name": ""}
      ]


#########################################################
#Заведем в списке documents один словарь без ключа 'name'
##########################################################

directories = {
        '1': ['2207 876234', '11-2', '5455 028765'],
        '2': ['10006', '5400 028765', '5455 002299'],
        '3': []
      }

messages = ['\nДобро пожаловать в систему электронного документооборота ООО "Рога и Копыта"\n', 
            'Чтобы посмотреть перечень зарегистрированных документов нажмите [l]', 
            'Чтобы посмотреть документы, хранящиеся на полках введите [sp]', 
            'Чтобы вывести информацию о документе введите [p]', 
            'Чтобы вывести информацию о всех владельцах документов,введите [pa]', 
            'Чтобы найти документ на полке введите [s]', 
            'Чтобы добавить новый документ введите [a]', 'Чтобы удалить документ введите [d]', 
            'Чтобы переместить документ введите [m]', 'Чтобы добавить новую полку введите [as]', 
            'Чтобы выполнить инспекцию хранящихся документов, введите [i]',
            'Для выхода из системы введите [q]']

def request_number():
    return input('Введите номер документа: ')

def request_shelf():
    while not (shelf_number := is_positive_int(input('Введите номер полки: '))):
        print('Номер полки должен быть целым числом больше нуля')
    return shelf_number

def is_positive_int(value):
    try:
        if int(value) > 0:
            return value
    except ValueError:
        return False

def find_doc(doc_number, print_stat = True):
    for doc in documents:
        if doc['number'] == doc_number:
            return doc
    if print_stat:
        print(f'Документ № {doc_number} не найден в учетной системе!')
  

def find_shelf(doc_number):
    for shelf in directories.items():
        if doc_number in shelf[1]:
            return shelf
        else:
            print(f'Документ № {doc_number} не найден в учетной системе')

def print_shelf(doc_number = None):
  while not doc_number:
    doc_number = request_number()
    if not find_shelf(doc_number):
      doc_number = None
  shelf = find_shelf(doc_number)
  if shelf:
    print(f'Документ № {doc_number} находится на полке № {shelf[0]} позиция {shelf[1].index(doc_number)}')

def print_people(doc_number = None):
  if not doc_number:
    doc_number = request_number()
  doc = find_doc(doc_number)
  if doc:

##############НОВЫЙ ФУНКЦИОНАЛ К ДЗ 2.3#########################
    try:
          print(f'Документ № {doc_number} принадлежит пользователю {doc["name"]}')
    except KeyError:
          print(f'В системе отсутствуют данные о владельце документа № {doc["number"]}')
###############################################

def print_list():
  print('Перечень зарегистрированных документов\n')
  for doc in documents:
    print(' '.join([i for i in doc.values()]))

def request_attr(key):
    return input(f'Введите аттрибут документа {key}:')

def add_docs(number = None): 

  doc = dict.fromkeys(documents[0].keys())
  
  while True:
    for key in doc.keys():
      if number and key == 'number':
        doc[key] = number
        continue
      doc[key] = request_attr(key)
    
    if find_doc(doc['number'], False):
      print(f'Документ с указанным номером уже храниться в системе:')
    else:
      break

  documents.append(doc)
  
  if not number:
    add_doc_shelf(doc)
  
def add_doc_shelf(doc):
  while True:
    shelf_number = request_shelf()
    if shelf_number not in directories.keys():
      if input(f'Полка № {shelf_number} отсутствует, хотите создать новую полку № {shelf_number}? y/n?:') == 'y':
        add_shelf()
    else:
      break 
  directories[shelf_number].append(doc['number'])
  print(f'Документ № {doc["number"]} добавлен на полку {shelf_number} позиция {directories[shelf_number].index(doc["number"])}')

def del_doc_shelf(doc_number):
  shelf = find_shelf(doc_number)
  print(f'Документ № {doc_number} удален c полки {shelf[0]} позиция {shelf[1].index(doc_number)}')
  directories[shelf[0]].remove(doc_number)

def del_doc(doc_number = None):
  while not doc_number:
    doc_number = request_number()
    if not find_doc(doc_number):
      doc_number = None
  documents.remove(find_doc(doc_number))
  del_doc_shelf(doc_number)

def move_doc_shelf(doc_number = None):
  while not doc_number:
    doc_number = request_number()
    if not find_doc(doc_number):
      doc_number = None
  del_doc_shelf(doc_number)
  add_doc_shelf(find_doc(doc_number))

def add_shelf():
  while True:
    shelf_number = request_shelf()
    if shelf_number in directories.keys():
      print('Указанная полка уже существует')
    else:
      directories[shelf_number] = []
      print(f'Полка № {shelf_number} добавлена')
      break

def print_dir():
  print('Документы, хранящиеся на полках')
  for key in directories:
    print(key, directories[key])

##############НОВЫЙ ФУНКЦИОНАЛ К ДЗ 2.3#########################

def print_all_people():

    for doc in documents:
        print_people(doc['number'])

def cleaner_dict():

    for doc in documents:
        for key in list(doc):
            if not doc[key]:
                doc.pop(key)

def inspection_doc():

  not_found_docs = []

  for shelf in directories.items():
    for number in shelf[1]:
      if not find_doc(number, False):
        not_found_docs.append(number)

  if not_found_docs:
    print(f'Перечень документов без описания:')

    for doc in not_found_docs:
      print(f'{doc}')

    if input(f'Хотите добавить недостающие аттрибуты документа? y/n:') == 'y':
      for number in not_found_docs:
        print(f'Документ №{number}:')
        add_docs(number)
      print(f'Недостающие атрибуты документов успешно внесены в систему')
    
  else:
    print(f'Документы без описания отсутствуют\n')

################################################################

def main_menu():

    while True:

      cleaner_dict()

      print("\n".join([msg for msg in messages]))
      command = input('\nВведите команду:')

      if command not in commands.keys():
          print('Незарегистрированная команда, повторите ввод')
          continue

      if command == 'q':
          break

      else:
          commands[command]()

commands = {'l': print_list, 'sp': print_dir, 'p': print_people, 's': print_shelf, 'a': add_docs, 'd': del_doc, 'm': move_doc_shelf, 'as': add_shelf, 'i': inspection_doc, 'pa': print_all_people, 'q': None}


if __name__ == '__main__':

    main_menu()
