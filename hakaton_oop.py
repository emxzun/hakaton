import json


def read(file_name='user.json'):
    with open(file_name) as file:
        return json.load(file)

def validate_password(password):
    if len(password) < 8:
        raise Exception('Пароль слишком короткий')

    if password.isdigit() or password.isalpha():
        raise Exception('пароль должен состоять из букв и цифр!')

class RegisterMixin:

    def register(self, name, password):
        data = read()
        new_id = self.__find_max_id(data)
        self.validate_username(name, data)
        validate_password(password)

        user = {
            'id': new_id,
            'name': name,
            'password': password
        }

        data.append(user)

        with open('user.json', 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return 'Successfully registered'

    def validate_username(self, name, data):
        if data:
            names = [i['name'] for i in data] # [1, 2, 3]
            if name in names:
                raise Exception('Такой юзер уже существует!')
    
    def __find_max_id(self, data):
        if data:
            ids = [i['id'] for i in data] # [1, 2, 3]
            return max(ids) + 1 # 3 + 1
        return 1


class LoginMixin:
    def login(self, name, password):
        data = read()
        if data:
            names = [i['name'] for i in data]
            if not name in names:
                raise Exception('Нет такого юзера в БД!')
        if data:
            passwords = [i['password'] for i in data]
            if not password in passwords:
                raise Exception('Неверный пароль')
        return 'Вы успешно залогинились'


class ChangePasswordMixin:
    def change_password(self, name, old_password, new_password):
        data = read()
        validate_password(new_password)
        new = {'password': new_password}
        if data:
            for user in data:
                if name == user['name']:
                    if old_password != user['password']:
                        raise Exception('Старый пароль указан неверно')
                with open('user.json', 'r+') as file:
                    pas = json.load(file)
                    pas[0]['password'] = new_password
                with open('user.json', 'w') as file2:
                    json.dump(pas, file2, indent=4)
                return 'Password changed successfully!'
            



 

class ChangeUsernameMixin:
    def change_name(self, old_name, new_name):
        data = read()
        if data:
            names = [i['name'] for i in data]
            if not old_name in names:
                raise Exception('Нет такого зарегистрированного юзера в БД!')
        if data:
            names = [i['name'] for i in data]
            if new_name in names:
                raise Exception('Пользователь с таким именем уже существует!')
            with open('user.json', 'r+') as file:
                pas = json.load(file)
                pas[0]['name'] = new_name
            with open('user.json', 'w') as file2:
                json.dump(pas, file2, indent=4)
                return 'Username changed successfully!'


class User(RegisterMixin, LoginMixin, ChangePasswordMixin, ChangeUsernameMixin):
    pass

user1 = User()
user2 = User()
user3 = User()
# print(user1.register('John', 'john123123'))
# print(user2.register('Rick', 'rick123123'))
# print(user3.register('Sam', 'sam123123'))


class CheckOwnerMixin:
    def check(self, owner):
        data = read()
        for i in data:
            if i['name'] != owner:
                raise Exception('Нет такого пользователя!')
        def __new__(cls, *args):
            return super().__new__(cls)
    

class Post(CheckOwnerMixin):
    def __init__(self, title, description, price, quantity, owner):
        self.title = title
        self.description = description
        self.price = price
        self.quantity = quantity
        self.owner = owner

# user = Post('title', 'description', 'price', 'quantity', 'owner')
# user.check('Sam')
# print(user)