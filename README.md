# Application Clone Twitter
Сервис микроблогов (аналог twitter)

<!--Установка-->
## Установка (Ubuntu 24.04.2 LTS)

1. Клонирование репозитория 

```git clone https://gitlab.skillbox.ru/daniil_baibakov/python_advanced_diploma.git```

2. Проверить, занят ли порт 80. В терминале ввести команду ```sudo netstat -lntp | grew -w "80"```. Если порт занят - освободить его.


3. Переход в директорию python_advanced_diploma:
```cd python_advanced_diploma```

4. Запуск приложения через Docker Compose (при разработке использовалась версия v2.33.0): 
```docker compose up```

<!--Пользовательская документация-->
## Документация
Пользовательская документация на backend доступна по ссылке [http:/localhost:5000/docs](http:/localhost:5000/docs).

<!--Фронтенд-->
## Фронтенд
Клиентское приложение открывается по ссылке [http:/localhost:80](http:/localhost:80).