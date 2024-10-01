import psycopg2
from flask import redirect
from flask_login import UserMixin
from psycopg2 import sql

from src.config import db, Users


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    @staticmethod
    def get(id):
        user_data = db.session.query(Users).filter_by(id=id).first()
        if user_data:
            return User(user_data.id, user_data.name, user_data.password)
        return None

def connect_db(user_db, password_db, host_db, port_db, database_db):
    """функция для подключения к бд"""
    try:
        connection = psycopg2.connect(
            user=user_db,
            password=password_db,
            host=host_db,
            port=port_db,
            database=database_db
        )
        return connection
    except Exception as e:
        print(f"Ошибка: {e}")


def add_db(item):
    """функция для добавления данных в бд"""
    try:
        db.session.add(item)
        db.session.commit()
        return redirect('/home')
    except Exception as e:
        print(f'Ошибка: {e}')

def get_users(name, user_db, password_db, host_db, port_db, database_db):
    """Поиск пользователя по имени в бд."""
    connection = connect_db(user_db, password_db, host_db, port_db, database_db)
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE name = %s"
        cursor.execute(query, (name,))

        user = cursor.fetchone()
        if user:
            return user
        else:
            print("Пользователь не найден.")
            return None
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def create_database(db_name, user, password, host='localhost', port='5432'):
    try:
        connection = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"База данных '{db_name}' успешно создана.")

    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == '__main__':
    db_name = input("Введите имя базы данных: ")
    user = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    create_database(db_name, user, password)

