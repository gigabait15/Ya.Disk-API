# Веб-интерфейс Яндекс.Диска
### Описание проекта:
Данный проект является Ввеб-интерфейсом реализации Flask и Яндекс.Диск API
***
### Струкрута проекта:
- `.gitignore` файл с игнорируемыми для пула в гит данными
- `README.md` файл с описание проекта
- ` req.txt` файл с зависимостями проекта
- `src` директория проекта
- `app.py` файл с логикой проекта
- `config.py` файл с настройками проекта
- `psql_db.py` файл с настройками БД
- `ya_api.py` файл для подключения к API Яндекс

***
### Установка
чтобы запустить проект, необходимо следовать следующим шагам:
1. Клонировать репозиторий

-`git clone https://github.com/gigabait15/Ya.Disk-API.git`

2.Установить и запустить виртуальное окружение:

Если не установлено то в консоли прописать команду:
- `python -m venv .venv`

Если установлен:
- `.venv\Scripts\activate`

3.Установите необходимые зависимости:
- `pip install -r req.txt`

4.Создать БД и таблицы:
- `python src\psql_db.py`

***
### Запуск проекта

Для запуска приложения выполнить:
- `python src\app.py`

***
### Контакты
Если у вас есть вопросы или предложения, пожалуйста, свяжитесь со мной по адресу: Workkerbecov@yandex.ru
