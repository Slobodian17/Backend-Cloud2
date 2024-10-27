# Application_programming

# 4 lab application programming
Створення та розгортання проекту на flask версії 2.2.2
## Створення на налаштування віртуального середовища за допомогою vitualenv

Створення віртуального середовища
```shell
virtualenv + requirements.txt
◦ pip install virtualenv
◦ virtualenv venv
◦ source ./venv/bin/activate
◦ deactivate

створення файлу requirements.txt
>> pip freeze > requirements.txt        
>> pip install -r requirements.txt 
Залежності вказані у файлі requirements.txt

Доступні шляхи

На сайті поки що доступний лише шлях 
shell
api/v1/hello-world-10

перевірити роботу можна виконанням
curl -v -XGET http://localhost:5000/api/v1/hello-world-10
або у браузері

```