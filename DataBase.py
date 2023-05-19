import sqlite3
import tkinter.messagebox as mb
from sqlite3 import Error
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_query_insert(connection, query, data):
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query, extra_data=()):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, extra_data)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def create_db(connection):

    create_clients_table = """
    CREATE TABLE IF NOT EXISTS Clients (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      Login TEXT NOT NULL,
      Password TEXT NOT NULL,
      First_Name TEXT NOT NULL,
      Second_Name TEXT NOT NULL,
      Patronymic TEXT
    );
    """
    create_doctors_table = """
    CREATE TABLE IF NOT EXISTS Doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Login TEXT NOT NULL,
    Password TEXT NOT NULL,
    First_Name TEXT NOT NULL,
    Second_Name TEXT NOT NULL,
    Patronymic TEXT,
    Specialization TEXT NOT NULL,
    Work_Time TIME
    );
    """
    create_managers_table = """
    CREATE TABLE IF NOT EXISTS Managers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Login TEXT NOT NULL,
    Password TEXT NOT NULL,
    First_Name TEXT NOT NULL,
    Second_Name TEXT NOT NULL,
    Patronymic TEXT
    );
    """
    create_schedule_table = """
    CREATE TABLE IF NOT EXISTS Schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_Client INTEGER NOT NULL,
    id_Doctor INTEGER NOT NULL,
    Direction TEXT NOT NULL,
    appoint_time TIME NOT NULL,
    FOREIGN KEY (id_Client) REFERENCES Clients (id)
    FOREIGN KEY (id_Doctor) REFERENCES Doctors (id)
    );
    """
    execute_query(connection, create_clients_table)
    execute_query(connection, create_doctors_table)
    execute_query(connection, create_managers_table)
    execute_query(connection, create_schedule_table)

def first_insert_table(connection):
    create_clients = """
    INSERT INTO
      Clients (Login, Password, First_Name, Second_Name, Patronymic)
    VALUES
      ('123', '123', 'Матвей', 'Новодничий', 'Александрович');
    """
    create_doctors = """
    INSERT INTO
      Doctors (Login, Password, First_Name, Second_Name, Patronymic, Specialization, Work_Time)
    VALUES
      ('321', '321', 'Анна', 'Яковлева', 'Евгеньевна', 'ЛОР', '10:00');
    """
    create_managers = """
    INSERT INTO
      Managers (Login, Password, First_Name, Second_Name, Patronymic)
    VALUES
      ('1', '1', 'Данил', 'Степанов', 'Сергеевич');
    """
    create_schedule = """
    INSERT INTO
      Schedule (id_Client, id_Doctor, Direction, appoint_time)
    VALUES
      ('1', '1', 'ЛОР', '10:00');
    """
    execute_query(connection, create_clients)
    execute_query(connection, create_doctors)
    execute_query(connection, create_managers)
    execute_query(connection, create_schedule)

def insert_clients_table(connection, lg, passwd, f_n, s_n, ptn = (None,)):
    create_clients = """
    INSERT INTO
    Clients (Login, Password, First_Name, Second_Name, Patronymic)
    VALUES
    (?,?,?,?,?);
    """
    data_tuple = (lg, passwd, f_n, s_n, ptn)
    execute_query_insert(connection, create_clients, data_tuple)

def insert_doctors_table(connection, lg, passwd, f_n, s_n, spec, ptn = None, w_t = None):
    create_doctors = """
    INSERT INTO
    Doctors (Login, Password, First_Name, Second_Name, Patronymic, Specialization, Work_Time)
    VALUES
    (?, ?, ?, ?, ?, ?, ?);
    """
    execute_query_insert(connection, create_doctors, (lg, passwd, f_n, s_n, ptn, spec, w_t))

def insert_managers_table(connection, lg, passwd, f_n, s_n, ptn = (None,)):
    create_managers = """
    INSERT INTO
    Managers (Login, Password, First_Name, Second_Name, Patronymic)
    VALUES
    (?, ?, ?, ?, ?);
    """
    data_tuple = (lg, passwd, f_n, s_n, ptn)
    execute_query_insert(connection, create_managers, data_tuple)

def insert_schedule_table(connection, id_c, id_d, dir, a_t):
    create_schedule = """
    INSERT INTO
    Schedule (id_Client, id_Doctor, Direction, appoint_time)
    VALUES
    (?, ?, ?, ?);
    """
    data_tuple = (id_c, id_d, dir, a_t)
    execute_query_insert(connection, create_schedule, data_tuple)

def update_doctor_work_time(connection, id, w_t):
    cursor = connection.cursor()
    select_wt = """SELECT Work_Time FROM Doctors WHERE Id = ?"""
    data = (id,)
    cursor.execute(select_wt, data)
    select_result = cursor.fetchall()
    wt_str = ""
    if select_result[0][0] == None:
        update_wt = """Update Doctors set Work_Time =? WHERE Id =?"""
        cursor.execute(update_wt, (w_t, id))
        connection.commit()
        return "yes"
    else:
        for list in select_result:
            temp_str = ''.join(list)
            wt_str = wt_str + temp_str + " "
        if w_t in wt_str:
            mb.showwarning("Предупреждение", "Заданное рабочее время уже существует!")
            return "no"
        wt_str = wt_str + w_t
        data_tuple = (wt_str, id)
        update_wt = """Update Doctors set Work_Time = ? WHERE id = ?"""
        cursor.execute(update_wt, data_tuple)
        connection.commit()
        return "yes"

def delete_doctor_work_time(connection, id, w_t):
    cursor = connection.cursor()
    select_wt = """SELECT Work_Time FROM Doctors WHERE Id = ?"""
    data = (id,)
    cursor.execute(select_wt, data)
    select_result = cursor.fetchall()
    wt_str = ""
    for list in select_result:
        temp_str = ''.join(list)
        wt_str = wt_str + temp_str + " "
    wt_str = wt_str[:-1]
    wt_str = wt_str.replace(" " + w_t, "")
    wt_str = wt_str.replace(w_t, "")
    data_tuple = (wt_str, id)
    update_wt = """Update Doctors set Work_Time = ? WHERE Id = ?"""
    cursor.execute(update_wt, data_tuple)
    connection.commit()


def delete_record(connection, login, time, role):
    cursor = connection.cursor()
    if role == "Client":
        id_client_select = """SELECT id FROM Clients WHERE Login =?"""
        cursor.execute(id_client_select, (login,))
        id_result = cursor.fetchall()
        id_client = id_result[0][0]
        delete_schedule = """DELETE FROM Schedule WHERE id_Client =? AND appoint_time =?"""
        cursor.execute(delete_schedule, (id_client, time))
    elif role == "Doctor":
        id_doctor_select = """SELECT id FROM Doctors WHERE Login =?"""
        cursor.execute(id_doctor_select, (login,))
        id_result = cursor.fetchall()
        id_doctor = id_result[0][0]
        delete_schedule = """DELETE FROM Schedule WHERE id_Doctor =? AND appoint_time =?"""
        cursor.execute(delete_schedule, (id_doctor, time))
    else:
        return
    connection.commit()
