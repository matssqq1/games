import pyodbc
score = 10
level = 10
def baza(score, level):
    finish_score = score * level
    # Подключение к базе данных
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:/Users/a.ustinov/Documents/Database_Games.accdb')
    
    # Создание курсора для выполнения запросов
    cursor = conn.cursor()

    # Выполнение SQL-запроса
    cursor.execute('INSERT INTO table_name (finish_score) VALUES (?)', (finish_score,))
    conn.commit()

    # Выполнение SQL-запроса для чтения и записи в переменную score_tabl
    cursor.execute('SELECT finish_score FROM table_name')

    # Получение результатов запроса и запись их в переменную score_tabl
    score_tabl = []
    for row in cursor.fetchall():
        score_tabl.append(row.finish_score)
        print(row.finish_score)

    # Закрытие курсора и соединения
    cursor.close()
    conn.close()

    # Вернуть переменную score_tabl для дальнейшего использования
    return score_tabl

print(baza(score, level))