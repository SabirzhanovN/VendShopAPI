# Intrudaction
***

*Действия будут проводится в ОС Linux*

1. Склонируйте проект с гитхаба (https://github.com/SabirzhanovN/VendShopAPI)

```commandline
git clone https://github.com/SabirzhanovN/VendShopAPI.git
```

2. Войдите в папку VendShopAPI и создайте виртуальное окружение

```commandline
cd VendShopAPI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Запишите миграции в базу данных и создайте суперпользователя

```commandline
python manage.py migrate
python manage.py createsuperuser
```

4. Запустите тесты

```commandline
python manage.py test
```

5. Если ошибок нет, то запускайте сервер)

```commandline
python manage.py runserver
```
***
> Совет: Заполните сперва базу данных несколькими продуктами от имени администратора(Зарегайтесь в админ панели) 