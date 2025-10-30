import click
from flask import current_app
from app.db import db

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    with current_app.open_resource('schema.sql') as f:
        connection = db.connect()
        with connection.cursor() as cursor:
            # Читаем весь SQL файл
            sql_script = f.read().decode('utf8')
            
            # Разделяем скрипт на отдельные команды
            sql_commands = sql_script.split(';')
            
            # Выполняем каждую команду отдельно
            for command in sql_commands:
                command = command.strip()
                if command:  # Пропускаем пустые команды
                    cursor.execute(command)
                    
        connection.commit()
    click.echo('Initialized the database.')