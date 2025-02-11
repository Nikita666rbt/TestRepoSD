import sqlite3

class ORMMapper:
    def __init__(self, target_class, db_name='database.db'):
        """
        Инициализирует ORMMapper.
        :param target_class: Класс, на основе которого будет создана таблица.
        :param db_name: Имя файла базы данных (по умолчанию database.db).
        """
        self.target_class = target_class
        self.db_name = db_name

    def convert_to_db(self):
        """
        Создает таблицу в базе данных на основе структуры target_class.
        """
        # Получаем имя таблицы (используем имя класса)
        table_name = self.target_class.__name__

        # Получаем атрибуты класса, игнорируя магические и служебные
        fields = {
            name: typ
            for name, typ in self.target_class.__annotations__.items()
        }

        if not fields:
            raise ValueError("Класс не содержит аннотированных полей.")

        # Определяем SQL-типы на основе аннотаций
        sql_field_types = {
            int: "INTEGER",
            str: "TEXT",
            float: "REAL",
            bool: "INTEGER"
        }

        # Создаем список столбцов с типами
        columns = []
        for field_name, field_type in fields.items():
            sql_type = sql_field_types.get(field_type, "TEXT")  # По умолчанию TEXT
            columns.append(f"{field_name} {sql_type}")

        # Генерируем SQL-запрос для создания таблицы
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(columns)}
        );
        """

        # Подключаемся к базе данных и выполняем запрос
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            conn.commit()

        print(f"Таблица '{table_name}' успешно создана в базе данных '{self.db_name}'.")


# Пример использования

# Определяем класс с аннотациями типов
class User:
    id: int
    name: str
    age: int
    is_active: bool

# Создаем экземпляр ORMMapper и конвертируем класс в таблицу
mapper = ORMMapper(User)
mapper.convert_to_db()
