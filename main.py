import functools
import operator
import os
import customtkinter as ctk
import tkinter.messagebox as mb
import DataBase as DB
from PIL import Image

ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("System")

connection = DB.create_connection("health_center.sqlite")


class SampleApp(ctk.CTk):
    log_check = False
    role = ""
    login = ""

    def create_head(self, controller, doctor_page=False):

        def click_to_main():
            controller.show_frame("Main_Window")
            return

        def click_to_appointment():
            if SampleApp.log_check:
                if SampleApp.role == "Client":
                    controller.show_frame("Appointment_Window")
                else:
                    return
            else:
                controller.show_frame("Window_Sign_in")
            return

        def click_to_record():
            if SampleApp.log_check:
                if SampleApp.role == "Client":
                    controller.show_frame("Client_Record_Window")
                    return
                elif SampleApp.role == "Doctor":
                    controller.show_frame("Doctor_Record_Window")
            else:
                controller.show_frame("Window_Sign_in")
            return

        def click_sign_in():
            if not SampleApp.log_check:
                controller.show_frame("Window_Sign_in")
                return

            else:
                if SampleApp.role == "Client":
                    controller.show_frame("Client_Profile")
                    return

                elif SampleApp.role == "Doctor":
                    existing_records_btn.configure(text="Записанные пациенты")
                    controller.show_frame("Doctor_Profile")
                    return

                elif SampleApp.role == "Manager":
                    controller.show_frame("Manager_Profile")
                    return

            return

        head_frame = ctk.CTkFrame(self, border_width=1)
        head_frame.pack(side="top")

        main_window_btn = ctk.CTkButton(head_frame, text="Главная", width=125, height=30, command=click_to_main)
        main_window_btn.grid(column=0, row=0)

        make_appointment_btn = ctk.CTkButton(head_frame, text="Запись на приём", width=125, height=30,
                                             command=click_to_appointment)
        make_appointment_btn.grid(column=1, row=0)

        existing_records_btn = ctk.CTkButton(head_frame, text="Существующие записи", width=125, height=30,
                                             font=("Arial", 10), command=click_to_record)
        existing_records_btn.grid(column=2, row=0)

        sign_btn = ctk.CTkButton(head_frame, text="Профиль", width=125, height=30, font=("Arial", 12),
                                 command=click_sign_in)
        sign_btn.grid(column=3, row=0)

        if doctor_page:
            existing_records_btn.configure(text="Записанные пациенты")

    def __init__(self):
        ctk.CTk.__init__(self)
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (Main_Window, Window_Registration, Window_Sign_in,
                  Client_Profile, Appointment_Window, Client_Record_Window,
                  Doctor_Profile, Doctor_Record_Window,
                  Manager_Profile, Window_Add_Schedule, Window_Delete_Schedule, Window_Register_Doctor):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Main_Window")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class Main_Window(ctk.CTkFrame):
    def __init__(self, parent, controller):

        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        SampleApp.create_head(self, controller)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")

        img = ctk.CTkImage(Image.open(os.path.join(image_path, "health.png")), size=(200, 200))
        label_for_img = ctk.CTkLabel(self, text = "", image=img)
        label_for_img.pack(anchor = "nw", pady = 20, padx= 5)

        label_extra_info = ctk.CTkLabel(self, text = "Какая-то доп. информация", font=("Arial", 14))
        label_extra_info.pack(anchor = "w")

        label_main_info = ctk.CTkLabel(self, text = "Какая-то основная информация", font=("Arial", 14))
        label_main_info.place(x = 220, y = 45)

class Window_Sign_in(ctk.CTkFrame):

    fio = ""

    def __init__(self, parent, controller):

        def clear_entry():
            login_entry.delete(0, "end")
            password_entry.delete(0, "end")
            return

        def client_connection_fio():
            first_name = DB.execute_read_query(connection, """SELECT First_Name FROM Clients WHERE login =?""",
                                               (SampleApp.login,))
            first_name = ''.join(first_name[0])
            second_name = DB.execute_read_query(connection, """SELECT Second_Name FROM Clients WHERE login =?""",
                                                (SampleApp.login,))
            second_name = ''.join(second_name[0])
            patronymic = DB.execute_read_query(connection, """SELECT Patronymic FROM Clients WHERE login =?""",
                                               (SampleApp.login,))
            patronymic = ''.join(patronymic[0])
            Window_Sign_in.fio = second_name + " " + first_name + " " + patronymic

        def doctor_connection_fio():
            first_name = DB.execute_read_query(connection, """SELECT First_Name FROM Doctors WHERE login =?""",
                                               (SampleApp.login,))
            first_name = ''.join(first_name[0])
            second_name = DB.execute_read_query(connection, """SELECT Second_Name FROM Doctors WHERE login =?""",
                                                (SampleApp.login,))
            second_name = ''.join(second_name[0])
            patronymic = DB.execute_read_query(connection, """SELECT Patronymic FROM Doctors WHERE login =?""",
                                               (SampleApp.login,))
            patronymic = ''.join(patronymic[0])
            Window_Sign_in.fio = second_name + " " + first_name + " " + patronymic

        def manager_connection_fio():
            first_name = DB.execute_read_query(connection, """SELECT First_Name FROM Managers WHERE login =?""",
                                               (SampleApp.login,))
            first_name = ''.join(first_name[0])
            second_name = DB.execute_read_query(connection, """SELECT Second_Name FROM Managers WHERE login =?""",
                                                (SampleApp.login,))
            second_name = ''.join(second_name[0])
            patronymic = DB.execute_read_query(connection, """SELECT Patronymic FROM Managers WHERE login =?""",
                                               (SampleApp.login,))
            patronymic = ''.join(patronymic[0])
            Window_Sign_in.fio = second_name + " " + first_name + " " + patronymic

        def sign_in():
            login = login_entry.get()
            password = password_entry.get()
            authorization_client = DB.execute_read_query(connection,
                                                         """SELECT * FROM Clients WHERE login =? AND password =?""",
                                                         (login, password))
            if authorization_client:
                SampleApp.log_check = True
                SampleApp.role = "Client"
                SampleApp.login = login
                client_connection_fio()
                controller.show_frame("Client_Profile")
                clear_entry()
                return

            authorization_doctor = DB.execute_read_query(connection,
                                                         """SELECT * FROM Doctors WHERE login =? AND password =?""",
                                                         (login, password))
            if authorization_doctor:
                SampleApp.log_check = True
                SampleApp.role = "Doctor"
                SampleApp.login = login
                doctor_connection_fio()
                controller.show_frame("Doctor_Profile")
                clear_entry()
                return

            authorization_manager = DB.execute_read_query(connection,
                                                          """SELECT * FROM Managers WHERE login =? AND password =?""",
                                                          (login, password))
            if authorization_manager:
                SampleApp.log_check = True
                SampleApp.role = "Manager"
                SampleApp.login = login
                manager_connection_fio()
                controller.show_frame("Manager_Profile")
                clear_entry()
                return

            mb.showwarning("Ошибка", "Неверный логин или пароль")
            return

        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        SampleApp.create_head(self, controller)

        sign_in_frame = ctk.CTkFrame(self, border_width=2, height= 300, width=250)
        sign_in_frame.pack(anchor = "center", pady = 60)

        login_entry = ctk.CTkEntry(sign_in_frame,placeholder_text = "Логин", font=("Arial", 14))
        login_entry.pack(anchor = "n", pady = 40, padx = 20)

        password_entry = ctk.CTkEntry(sign_in_frame,placeholder_text = "Пароль",show="*", font=("Arial", 14))
        password_entry.pack(anchor = "n", padx = 20)

        sign_in_btn = ctk.CTkButton(sign_in_frame, text = "Войти", font=("Arial", 14), command = sign_in)
        sign_in_btn.pack(anchor = "n", pady = 30, padx = 20)

        to_register_label = ctk.CTkLabel(sign_in_frame, text_color="#42AAFF", text = "Нет аккаунта? Зарегистрироваться",
                                         font=("Arial", 12))
        to_register_label.pack(anchor = "n", pady = 5, padx = 20)
        to_register_label.bind("<Button-1>", lambda e: controller.show_frame("Window_Registration"))

class Window_Registration(ctk.CTkFrame):
    def __init__(self, parent, controller):

        def register():
            fio = fio_entry.get()
            login = login_entry.get()
            password = password_entry.get()
            password_again = password_again_entry.get()

            if fio.replace(" ", "") == "" or login.replace(" ", "") == "" or password.replace(" ", "") == "":
                mb.showwarning("Ошибка", "Введите все поля")
                return

            if len(fio.split()) != 3 or fio.replace(" ", "").isalpha() == False:
                mb.showwarning("Ошибка", "Неверно введено ФИО")
                return

            if password != password_again:
                mb.showwarning("Ошибка", "Пароли не совпадают")
                return

            authorization_client = DB.execute_read_query(connection, """SELECT * FROM Clients WHERE login = ?""",
                                                         (login,))
            if authorization_client:
                mb.showwarning("Ошибка", "Логин уже зарегистрирован")
                return

            authorization_doctor = DB.execute_read_query(connection, """SELECT * FROM Doctors WHERE login =?""",
                                                         (login,))
            if authorization_doctor:
                mb.showwarning("Ошибка", "Логин уже зарегистрирован")
                return

            authorization_manager = DB.execute_read_query(connection, """SELECT * FROM Managers WHERE login =?""",
                                                          (login,))
            if authorization_manager:
                mb.showwarning("Ошибка", "Логин уже зарегистрирован")
                return

            fio = fio.split()
            Window_Sign_in.fio = fio[0] + " " + fio[1] + " " + fio[2]
            SampleApp.login = login
            SampleApp.role = "Client"
            SampleApp.log_check = True
            DB.execute_query_insert(connection,
                                    """INSERT INTO Clients (Login, Password, First_Name, Second_Name, Patronymic)
                                     VALUES (?,?,?,?,?)""", (login, password, fio[1], fio[0], fio[2]))
            controller.show_frame("Client_Profile")
            return

        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        SampleApp.create_head(self, controller)

        register_frame = ctk.CTkFrame(self, border_width=2, height= 400, width=250)
        register_frame.pack(anchor = "center", pady = 60)

        fio_entry = ctk.CTkEntry(register_frame, placeholder_text = "ФИО", font=("Arial", 14))
        fio_entry.pack(anchor = "n", pady = 20, padx = 40)

        login_entry = ctk.CTkEntry(register_frame, placeholder_text = "Логин", font=("Arial", 14))
        login_entry.pack(anchor = "n", padx = 20)

        password_entry = ctk.CTkEntry(register_frame, placeholder_text="Пароль", show="*", font=("Arial", 14))
        password_entry.pack(anchor="n", padx=20, pady=20)

        password_again_entry = ctk.CTkEntry(register_frame, placeholder_text="Повторите пароль", show="*",
                                            font=("Arial", 14))
        password_again_entry.pack(anchor="n", padx=20)

        register_btn = ctk.CTkButton(register_frame, text = "Зарегистрироваться", font=("Arial", 14), command = register)
        register_btn.pack(anchor = "n", pady = 15, padx = 20)

        to_sign_in_label = ctk.CTkLabel(register_frame, text_color="#42AAFF", text = "Есть аккаунт? Войти",
                                        font=("Arial", 12))
        to_sign_in_label.pack(anchor = "n", pady = 5, padx = 20)
        to_sign_in_label.bind("<Button-1>", lambda e: controller.show_frame("Window_Sign_in"))

class Client_Profile(ctk.CTkFrame):

    def __init__(self, parent, controller):

        def quit():
            SampleApp.log_check = False
            SampleApp.login = ""
            SampleApp.role = ""
            fio_entry.configure(state = "normal")
            login_entry.configure(state = "normal")
            fio_entry.delete(0, "end")
            login_entry.delete(0, "end")
            controller.show_frame("Window_Sign_in")
            self.bind("<Enter>", loading_fio)

        def loading_fio(event):
            fio_entry.configure(placeholder_text=Window_Sign_in.fio)
            fio_entry.configure(state = "disabled")
            login_entry.configure(placeholder_text=SampleApp.login)
            login_entry.configure(state = "disabled")
            self.unbind("<Enter>")

        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        SampleApp.create_head(self, controller)

        self.bind("<Enter>", loading_fio)

        info_frame = ctk.CTkFrame(self)
        info_frame.pack(side = "left", pady = 20, padx = 10, anchor = "nw")

        fio_label = ctk.CTkLabel(info_frame, text = "ФИО")
        fio_label.pack(anchor = "w", pady=5)

        fio_entry = ctk.CTkEntry(info_frame, font=("Arial", 14), placeholder_text="", placeholder_text_color="white", width = 350)
        fio_entry.pack(anchor = "w", pady=5)

        login_label = ctk.CTkLabel(info_frame, text = "Логин")
        login_label.pack(anchor = "w", pady=5)

        login_entry = ctk.CTkEntry(info_frame, font=("Arial", 14), placeholder_text="", placeholder_text_color="white", width=350)
        login_entry.pack(anchor="w", pady=5)

        quit_btn = ctk.CTkButton(self, text="Выйти из аккаунта", font=("Arial", 12),
                                 command=quit)
        quit_btn.pack(anchor = "ne", pady=20)

class Doctor_Profile(ctk.CTkFrame):
    def __init__(self, parent, controller):

        def loading_doctor_info(event):
            entry_fio_doctor.configure(placeholder_text=Window_Sign_in.fio)
            entry_fio_doctor.configure(state = "disabled")
            entry_login_doctor.configure(placeholder_text=SampleApp.login)
            entry_login_doctor.configure(state = "disabled")
            specialization = DB.execute_read_query(connection, """SELECT Specialization FROM Doctors WHERE login = ?""",
                                                   (SampleApp.login,))
            spec = ''.join(specialization[0])
            entry_specialization_doctor.configure(placeholder_text=spec)
            entry_specialization_doctor.configure(state = "disabled")
            self.unbind("<Enter>")
            frame_doctor_info.unbind("<Enter>")
            entry_login_doctor.unbind("<Enter>")

        def quit():
            SampleApp.log_check = False
            SampleApp.login = ""
            SampleApp.role = ""
            controller.show_frame("Window_Sign_in")
            entry_fio_doctor.configure(state = "normal")
            entry_login_doctor.configure(state = "normal")
            entry_fio_doctor.delete(0, "end")
            entry_login_doctor.delete(0, "end")
            entry_specialization_doctor.configure(state = "normal")
            entry_specialization_doctor.delete(0, "end")
            self.bind("<Enter>", loading_doctor_info)
            frame_doctor_info.bind("<Enter>", loading_doctor_info)
            entry_login_doctor.bind("<Enter>", loading_doctor_info)
            return

        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.bind("<Enter>", loading_doctor_info)

        SampleApp.create_head(self, controller, True)

        quit_btn = ctk.CTkButton(self, text="Выйти из аккаунта", font=("Arial", 12), command=quit)
        quit_btn.pack(side="right", anchor="ne", pady=20)

        frame_doctor_info = ctk.CTkFrame(self)
        frame_doctor_info.pack(side = "left", anchor = "nw", pady = 20)

        frame_doctor_info.bind("<Enter>", loading_doctor_info)

        label_fio_doctor = ctk.CTkLabel(frame_doctor_info, text = "ФИО")
        label_fio_doctor.pack(anchor = "w", pady=5, padx = 5)

        entry_fio_doctor = ctk.CTkEntry(frame_doctor_info, placeholder_text="", placeholder_text_color="white", width = 350)
        entry_fio_doctor.pack(anchor = "w", pady=5, padx=5)

        label_specialization_doctor = ctk.CTkLabel(frame_doctor_info, text = "Специализация")
        label_specialization_doctor.pack(anchor = "w", pady=5, padx=5)

        entry_specialization_doctor = ctk.CTkEntry(frame_doctor_info, placeholder_text="", placeholder_text_color="white", width = 350)
        entry_specialization_doctor.pack(anchor = "w", pady=5, padx=5)

        label_login_doctor = ctk.CTkLabel(frame_doctor_info, text = "Логин")
        label_login_doctor.pack(anchor = "w", pady=5, padx=5)

        entry_login_doctor = ctk.CTkEntry(frame_doctor_info, placeholder_text="", placeholder_text_color="white", width = 350)
        entry_login_doctor.pack(anchor = "w", pady=5, padx=5)
        entry_login_doctor.bind("<Enter>", loading_doctor_info)

class Manager_Profile(ctk.CTkFrame):
    def __init__(self, parent, controller):

        def add_schedule():
            controller.show_frame("Window_Add_Schedule")
            return

        def delete_schedule():
            controller.show_frame("Window_Delete_Schedule")
            return

        def register_doctor():
            controller.show_frame("Window_Register_Doctor")
            return

        def quit():
            SampleApp.log_check = False
            SampleApp.login = ""
            SampleApp.role = ""
            fio_entry.configure(state="normal")
            login_entry.configure(state="normal")
            fio_entry.delete(0, "end")
            login_entry.delete(0, "end")
            controller.show_frame("Window_Sign_in")
            self.bind("<Enter>", loading_fio)

        def loading_fio(event):
            fio_entry.configure(placeholder_text=Window_Sign_in.fio)
            fio_entry.configure(state = "disabled")
            login_entry.configure(placeholder_text=SampleApp.login)
            login_entry.configure(state = "disabled")
            self.unbind("<Enter>")

        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        SampleApp.create_head(self, controller)

        self.bind("<Enter>", loading_fio)

        info_frame = ctk.CTkFrame(self)
        info_frame.pack(side="left", pady=20, padx=10, anchor="nw")

        fio_label = ctk.CTkLabel(info_frame, text="ФИО")
        fio_label.pack(anchor="w", pady=5, padx=5)

        fio_entry = ctk.CTkEntry(info_frame, font=("Arial", 14), placeholder_text="", placeholder_text_color="white",
                                 width=300)
        fio_entry.pack(anchor="w", pady=5, padx=5)

        login_label = ctk.CTkLabel(info_frame, text="Логин")
        login_label.pack(anchor="w", pady=5, padx=5)

        login_entry = ctk.CTkEntry(info_frame, font=("Arial", 14), placeholder_text="", placeholder_text_color="white",
                                   width=300)
        login_entry.pack(anchor="w", pady=5, padx=5)

        frame_with_btn = ctk.CTkFrame(self)
        frame_with_btn.pack(side="left", pady=20, padx=10, anchor="nw")

        add_btn = ctk.CTkButton(frame_with_btn, text="Добавить расписание", font=("Arial", 12), command=add_schedule)
        add_btn.pack(anchor="n", pady=10, padx=5)

        delete_btn = ctk.CTkButton(frame_with_btn, text="Удалить расписание", font=("Arial", 12),
                                   command=delete_schedule)
        delete_btn.pack(anchor="n", pady=10, padx=5)

        register_btn = ctk.CTkButton(frame_with_btn, text="Зарегистрировать\nврача", font=("Arial", 12),
                                     command=register_doctor)
        register_btn.pack(anchor="n", pady=10, padx=5)

        quit_btn = ctk.CTkButton(frame_with_btn, text="Выйти из аккаунта", font=("Arial", 12),
                                 command=quit)
        quit_btn.pack(anchor="n", pady=10, padx=5)

class Appointment_Window(ctk.CTkFrame):
    def __init__(self, parent, controller):

        def loading_spec(event):
            spec_select = DB.execute_read_query(connection, """SELECT Specialization FROM Doctors""")
            specialization = ""
            for line in spec_select:
                line = ''.join(line)
                specialization += line + " "
            specialization = specialization.split()
            specialization = list(set(specialization))
            specialization_menu.configure(values=specialization)
            choice_frame.unbind("<Enter>")
            return

        def spec_callback(specialization_menu: str):
            doctor_select = DB.execute_read_query(connection, """SELECT Id, First_Name, Second_Name, Patronymic 
            FROM Doctors WHERE Specialization =?""", (specialization_menu,))
            right_doctors = []
            for line in doctor_select:
                line = functools.reduce(operator.add, (str(line[0]) + ". " + line[1] + " " + line[2] + " " + line[3]))
                right_doctors.append(line)
            doctor_menu.configure(values=right_doctors)
            return

        def doctor_callback(doctor_menu: str):
            fio_doctor = doctor_menu.split()
            fio_doctor[0] = fio_doctor[0].replace(".", "")
            time_select = DB.execute_read_query(connection, """SELECT Work_Time FROM Doctors
            WHERE Id=?""", (int(fio_doctor[0]),))
            time = "".join(time_select[0])
            time = time.split()
            time_menu.configure(values=time)
            pass

        def confirm():
            if specialization_menu.get() == "Выбор услуги" or doctor_menu.get() == "Выбор доктора"\
                    or time_menu.get() == "Выбор времени":
                mb.showwarning("Ошибка", "Все поля должны быть выбраны")
                return
            id_client_select = DB.execute_read_query(connection, """SELECT Id FROM Clients where Login =?""",
                                              (SampleApp.login,))
            id_client = id_client_select[0][0]
            doctor = doctor_menu.get()
            doctor = doctor.split()
            doctor[0] = doctor[0].replace(".", "")
            check_select = DB.execute_read_query(connection, """SELECT * FROM Schedule
             WHERE id_Client =? and appoint_time=?""",
                                                 (id_client, time_menu.get()))
            if len(check_select) != 0:
                mb.showwarning("Ошибка", "Запись на данное время уже есть")
                return
            else:
                DB.insert_schedule_table(connection, id_client, int(doctor[0]), specialization_menu.get(), time_menu.get())
                mb.showinfo("Успешно", "Вы успешно записались на приём")
                specialization_menu.set("Выбор услуги")
                doctor_menu.set("Выбор доктора")
                time_menu.set("Выбор времени")
            return

        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        SampleApp.create_head(self, controller)

        choice_frame = ctk.CTkFrame(self)
        choice_frame.pack(pady=20, padx=10, anchor="nw")
        choice_frame.bind("<Enter>", loading_spec)

        specialization_label = ctk.CTkLabel(choice_frame, text="Выбор услуги", font=("Arial", 18))
        specialization_label.pack(anchor="w", pady=10, padx=15)

        specialization_menu = ctk.CTkOptionMenu(choice_frame, values=[], width=350, command = spec_callback)
        specialization_menu.pack(anchor="w", pady=10, padx=15)
        specialization_menu.set("Выбор услуги")

        doctor_lablel = ctk.CTkLabel(choice_frame, text="Выбор доктора", font=("Arial", 18))
        doctor_lablel.pack(anchor="w", pady=10, padx=15)

        doctor_menu = ctk.CTkOptionMenu(choice_frame, values=[], width=350, command=doctor_callback)
        doctor_menu.pack(anchor="w", pady=10, padx=15)
        doctor_menu.set("Выбор доктора")

        time_label = ctk.CTkLabel(choice_frame, text="Выбор времени", font=("Arial", 18))
        time_label.pack(anchor="w", pady=10, padx=15)

        time_menu = ctk.CTkOptionMenu(choice_frame, values=[], width=350)
        time_menu.pack(anchor="w", pady=10, padx=15)
        time_menu.set("Выбор времени")

        confirm_btn = ctk.CTkButton(self, text="Подтвердить", fg_color="green", hover_color="#00b300", command=confirm, font=("Arial", 14))
        confirm_btn.pack(anchor="nw", padx=15)

class Client_Record_Window(ctk.CTkFrame):
    def __init__(self, parent, controller):

        def cancel_record():
            answer = mb.askquestion("Внимание", "Вы уверены, что хотите отменить запись?")
            if answer == "yes":
                time = records_tabview.get()
                records_tabview.delete(time)
                time_memory.remove(time)
                DB.delete_record(connection, SampleApp.login, time, SampleApp.role)
                return
            else:
                return

        def create_record(tabv):
            time = ''.join(tabv[4])
            doctor_select = DB.execute_read_query(connection, """SELECT  Second_Name, First_Name, Patronymic FROM Doctors
            WHERE id=?""", (tabv[2],))
            records_tabview.add(time)
            time_memory.append(time)
            doctor = ' '.join(doctor_select[0])

            info_label = ctk.CTkLabel(records_tabview.tab(time), text=doctor + ", " + ''.join(tabv[3]))
            info_label.pack(anchor="nw", pady=10, padx=15)

            cancel_btn = ctk.CTkButton(records_tabview.tab(time), hover_color="#ff3333", fg_color="#ff0000",
                                       text="Отменить запись", command=cancel_record)
            cancel_btn.pack(anchor="nw", pady=50, padx=15)
            return

        def loading_data(event):
            self.unbind("<Enter>")
            record_select = DB.execute_read_query(connection, """SELECT * FROM Schedule
                            JOIN Clients ON Schedule.id_Client = Clients.id WHERE Clients.Login=?""",
                                                  (SampleApp.login,))
            for tabv in record_select:
                create_record(tabv)
            return

        def update_records():
            for tab_name in time_memory:
                records_tabview.delete(tab_name)
            time_memory.clear()
            loading_data("<Enter>")
            return

        time_memory = []

        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        SampleApp.create_head(self, controller)
        self.bind("<Enter>", loading_data)

        records_tabview = ctk.CTkTabview(self)
        records_tabview.pack(pady=20, padx=10, anchor="nw")

        update_btn = ctk.CTkButton(self, text="Обновить расписание", command=update_records)
        update_btn.pack(anchor="nw", pady=10, padx=15)

class Doctor_Record_Window(ctk.CTkFrame):
    def __init__(self, parent, controller):

        def cancel_record():
            answer = mb.askquestion("Внимание", "Вы уверены, что хотите отменить запись?")
            if answer == "yes":
                time = records_tabview.get()
                records_tabview.delete(time)
                time_memory.remove(time)
                DB.delete_record(connection, SampleApp.login, time, SampleApp.role)
                return
            else:
                return

        def create_record(tabv):
            time = ''.join(tabv[4])
            client_select = DB.execute_read_query(connection, """SELECT Second_Name, First_Name, Patronymic FROM Clients
            WHERE id=?""", (tabv[1],))
            records_tabview.add(time)
            time_memory.append(time)
            client = ' '.join(client_select[0])

            info_label = ctk.CTkLabel(records_tabview.tab(time), text=client)
            info_label.pack(anchor="nw", pady=10, padx=15)

            cancel_btn = ctk.CTkButton(records_tabview.tab(time), hover_color="#ff3333", fg_color="#ff0000",
                                       text="Отменить запись", command=cancel_record)
            cancel_btn.pack(anchor="nw", pady=50, padx=15)
            return

        def loading_data(event):
            self.unbind("<Enter>")
            record_select = DB.execute_read_query(connection, """SELECT * FROM Schedule
                            JOIN Doctors ON Schedule.id_Doctor = Doctors.id WHERE Doctors.Login=?""",
                                                  (SampleApp.login,))
            for tabv in record_select:
                create_record(tabv)
            return

        def update_records():
            for tab_name in time_memory:
                records_tabview.delete(tab_name)
            time_memory.clear()
            loading_data("<Enter>")
            return

        time_memory = []

        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        SampleApp.create_head(self, controller)
        self.bind("<Enter>", loading_data)

        records_tabview = ctk.CTkTabview(self)
        records_tabview.pack(pady=20, padx=10, anchor="nw")

        update_btn = ctk.CTkButton(self, text="Обновить расписание", command=update_records)
        update_btn.pack(anchor="nw", pady=10, padx=15)

class Window_Add_Schedule(ctk.CTkFrame):
    def __init__(self, parent, controller):

        def update_doctors(event):
            doctors_list = []
            doctors_select = DB.execute_read_query(connection, """SELECT Id, Second_Name, First_Name, Patronymic 
            FROM Doctors""")
            for doctor in doctors_select:
                doctors_list.append(str(doctor[0]) + ". " + doctor[1] + " " + doctor[2] + " " + doctor[3])
            doctors_menu.configure(values=doctors_list)
            return

        def add_time():
            if doctors_menu.get() == "Выберите врача" or time_menu.get() == "Выберите время":
                mb.showerror("Ошибка", "Выберите врача и время")
                return
            data_doctor = doctors_menu.get()
            data_doctor = data_doctor.split()
            data_doctor[0] = data_doctor[0].replace(".", "")
            answer = DB.update_doctor_work_time(connection, data_doctor[0], time_menu.get())
            if answer == "no":
                return
            else:
                mb.showinfo("Успешно", "Вы успешно добавили рабочее время")
                time_menu.set("Выберите время")
            return

        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        SampleApp.create_head(self, controller)
        add_frame = ctk.CTkFrame(self)
        add_frame.pack(pady=20, padx=10, anchor="nw")

        doctors_menu = ctk.CTkOptionMenu(add_frame, values=[], width=350)
        doctors_menu.pack(anchor="w", pady=10, padx=15)
        doctors_menu.set("Выберите врача")

        doctors_menu.bind("<Enter>", update_doctors)

        time_menu = ctk.CTkOptionMenu(add_frame, values=["10:00", "11:00", "14:00", "15:00", "16:00"], width=350)
        time_menu.pack(anchor="w", pady=10, padx=15)
        time_menu.set("Выберите время")

        add_time_btn = ctk.CTkButton(self, text="Добавить время работы", command=add_time)
        add_time_btn.pack(anchor="nw", pady=10, padx=15)

class Window_Delete_Schedule(ctk.CTkFrame):
    def __init__(self, parent, controller):

        def update_doctors(event):
            doctors_list = []
            doctors_select = DB.execute_read_query(connection, """SELECT Id, Second_Name, First_Name, Patronymic 
                        FROM Doctors""")
            for doctor in doctors_select:
                doctors_list.append(str(doctor[0]) + ". " + doctor[1] + " " + doctor[2] + " " + doctor[3])
            doctors_menu.configure(values=doctors_list)
            return

        def callback_doctor(doctors_menu: str):
            time_menu.set("Выберите время")
            doctors_menu = doctors_menu.split()
            doctors_menu[0] = doctors_menu[0].replace(".", "")
            work_time_select = DB.execute_read_query(connection, """SELECT Work_Time FROM Doctors WHERE Id=?""",
                                                     (doctors_menu[0],))
            work_time = work_time_select[0][0]
            if work_time == None:
                time_menu.configure(values=[])
                return
            work_time = work_time.split()
            work_time.sort()
            time_menu.configure(values=work_time)
            return

        def delete_schedule():
            if doctors_menu.get() == "Выберите врача" or time_menu.get() == "Выберите время":
                mb.showerror("Ошибка", "Выберите врача и время")
                return
            answer = mb.askquestion("Внимание", "Вы уверены, что хотите удалить рабочее время врача?")
            if answer == "yes":
                data_doctor = doctors_menu.get()
                data_doctor = data_doctor.split()
                data_doctor[0] = data_doctor[0].replace(".", "")
                DB.delete_doctor_work_time(connection, data_doctor[0], time_menu.get())
                mb.showinfo("Успешно", "Время успешно удалено")
                doctors_menu.set("Выберите врача")
                time_menu.set("Выберите время")
                time_menu.configure(values=[])
                return
            else:
                return

        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        SampleApp.create_head(self, controller)

        delete_sched_frame = ctk.CTkFrame(self)
        delete_sched_frame.pack(pady=20, padx=10, anchor="nw")

        doctors_menu = ctk.CTkOptionMenu(delete_sched_frame, values=[], width=350, command=callback_doctor)
        doctors_menu.pack(anchor="w", pady=10, padx=15)
        doctors_menu.set("Выберите врача")

        doctors_menu.bind("<Enter>", update_doctors)

        time_menu = ctk.CTkOptionMenu(delete_sched_frame, values=[], width=350)
        time_menu.pack(anchor="w", pady=10, padx=15)
        time_menu.set("Выберите время")

        delete_time_btn = ctk.CTkButton(self, text="Удалить время работы", command=delete_schedule)
        delete_time_btn.pack(anchor="nw", pady=10, padx=15)

class Window_Register_Doctor(ctk.CTkFrame):
    def __init__(self, parent, controller):

        def reg_doctor():
            fio = fio_entry.get()
            login = login_entry.get()
            password = password_entry.get()
            specialization = specialization_entry.get()

            if fio.replace(" ", "") == "" or login.replace(" ", "") == "" or password.replace(" ", "") == "" or\
                    specialization.replace(" ", "") == "":
                mb.showerror("Ошибка", "Введите все поля")
                return

            if len(fio.split()) != 3 or fio.replace(" ", "").isalpha() == False:
                mb.showwarning("Ошибка", "Неверно введено ФИО")
                return

            authorization_client = DB.execute_read_query(connection, """SELECT * FROM Clients WHERE login = ?""",
                                                         (login,))
            if authorization_client:
                mb.showwarning("Ошибка", "Данный логин уже зарегистрирован")
                return

            authorization_doctor = DB.execute_read_query(connection, """SELECT * FROM Doctors WHERE login =?""",
                                                         (login,))
            if authorization_doctor:
                mb.showwarning("Ошибка", "Данный логин уже зарегистрирован")
                return

            authorization_manager = DB.execute_read_query(connection, """SELECT * FROM Managers WHERE login =?""",
                                                          (login,))
            if authorization_manager:
                mb.showwarning("Ошибка", "Данный логин уже зарегистрирован")
                return
            fio = fio.split()
            DB.insert_doctors_table(connection, login, password, fio[1], fio[0], specialization, fio[2])
            mb.showinfo("Успешно", "Вы успешно зарегистрировали врача")
            return

        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        SampleApp.create_head(self, controller)

        frame_for_register = ctk.CTkFrame(self)
        frame_for_register.pack(pady=20, padx=10, anchor="nw")

        fio_entry = ctk.CTkEntry(frame_for_register, placeholder_text="Введите ФИО", width=350)
        fio_entry.pack(anchor="w", pady=10, padx=15)

        specialization_entry = ctk.CTkEntry(frame_for_register, placeholder_text="Введите специализацию", width=350)
        specialization_entry.pack(anchor="w", pady=10, padx=15)

        login_entry = ctk.CTkEntry(frame_for_register, placeholder_text="Введите логин", width=350)
        login_entry.pack(anchor="w", pady=10, padx=15)

        password_entry = ctk.CTkEntry(frame_for_register, placeholder_text="Введите пароль", width=350)
        password_entry.pack(anchor="w", pady=10, padx=15)

        register_btn = ctk.CTkButton(self, text="Регистрация", command=reg_doctor)
        register_btn.pack(anchor="nw", pady=10, padx=15)

app = SampleApp()
app.geometry("500x500")
app.resizable(width=False, height=False)
app.mainloop()
