from requests import get, post, delete
from requests import put


def test_users():
    print(get('http://localhost:5000/api/v2/users').json())
    print(get('http://localhost:5000/api/v2/users/1').json())
    print(get('http://localhost:5000/api/v2/users/abc').json())  # Строка

    print(post('http://localhost:5000/api/v2/users', json={'name': 'Max', 'position': 'explorer',
                                                           'surname': 'Vasilev', 'age': 30, 'address': 'module_3',
                                                           'speciality': 'astrology',
                                                           'hashed_password': 'qwerty',
                                                           'email': 'maxv@mars.org'}).json())
    print(post('http://localhost:5000/api/v2/users').json())  # Не указаны поля
    print(post('http://localhost:5000/api/v2/users', json={'surname': 'Vasilev'}).json())  # Указаны не все поля

    print(delete('http://localhost:5000/api/v2/users/1').json())
    print(delete('http://localhost:5000/api/v2/users/10000').json())  # Несуществующий ID
    print(delete('http://localhost:5000/api/v2/users/abcdef').json())  # Строка

    print(put('http://localhost:5000/api/v2/users/1', json={'surname': 'Vasilev'}))
    print(put('http://localhost:5000/api/v2/users/1'))  # Не указаны поля


test_users()
