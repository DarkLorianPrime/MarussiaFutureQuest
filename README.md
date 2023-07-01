# Marussia skill (Future Quest)
# About
Сервис, реализующий механику навыков Маруси VK
# Built with
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
# RoadMap
- [x] Начать проект
- [x] Разработать систему State (локальных хранилищ для ответов)
- [x] Развернуть docker compose
- [x] Разделить общую структуру файлов на роуты
- [x] Сделать полноценную обертку над fastapi
- [x] Оптимизировать код
- [x] Написать документацию
# Examples
В этом разделе мы рассмотрим несколько основных примеров использования навыка, созданного с использованием FastAPI в рамках этого проекта.

👾 - Маруся

👨‍💻 - Собеседник
### Добавление вопроса
```
👨‍💻: Старт
👾:Привет! Для продолжения напиши "Категория"

👨‍💻: Категория
👾: Я задам 8 простых вопросов и по ним мы поймем куда тебе стоит двигаться.
Скажи "жду вопросы", если хочешь начать

👨‍💻: Жду вопросы
👾:В базе еще нет вопросов. Ты можешь добавить их командой: вопрос

👨‍💻: Вопрос
👾: Сообщи название своего вопроса

...

👾: Считаю шикарный вопрос. Сейчас сохраню

👨‍💻: Жду вопросы
👾: Вопрос категории: россия
    страна или город
    
👨‍💻: Страна
👾: Поздравляю с успешным прохождением теста. Вы - по праву IT специалист.

👨‍💻: Ы-ы-ы-ы
👾:Команда не распознана.
```

# Install
### Linux
Клонируем репозиторий:
```bash
$ git clone https://github.com/DarkLorianPrime/MarussiaFutureQuest
$ cd MarussiaFutureQuest
$ tree 
.
├── backend
│   ├── app
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── poetry.lock
│   │   ├── pyproject.toml
│   │   ├── routers
│   │   │   ├── common.py
│   │   │   ├── question_controller.py
│   │   │   └── question_creator.py
│   │   ├── service.py
│   │   ├── state.py
│   │   └── utils
│   │       ├── config.py
│   │       ├── core.py
│   │       ├── handler.py
│   │       ├── pydantic.py
│   │       ├── responses.py
│   │       └── states.py
│   └── Dockerfile
├── docker-compose.yaml
└── README.md
```
- Устанавливаем ENV
```bash
mv example.env .env
nano .env

--.env--
POSTGRES_HOST=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_NAME=
--------
```
- Запускаем docker-compose
```bash
$ docker-compose up -d --build
```
Вы должны увидеть надписи
```
Creating marussiafuturequest_database_1 ... done
Creating marussiafuturequest_backend_1  ... done
```

Сервис запущен и готов к работе. Можно настроить и протестировать: https://skill-debugger.marusia.mail.ru/

# Contacts
Grand developer - [@darklorianprime](https://vk.com/darklorianprime) - kasimov.alexander.ul@gmail.com