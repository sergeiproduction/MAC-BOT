import sqlite3
from datetime import date

class MODULE_RASP_DB:

    def __init__(self, database):
        #Подключение к БД и сохранение курсора соединения
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        

    def get_auditories(self):
        #Получение всех аудиторий
        with self.connection:
            return self.cursor.execute("SELECT `au_auditoryName` FROM `au_auditories`").fetchall()

    def auditory_exists(self, au_auditoryName):
        #Проверка есть ли аудитория в базе
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `au_auditories` WHERE `au_auditoryName` = ?", (au_auditoryName,)).fetchall()
            return bool(len(result))

    def auditories_count(self):
        #Подсчёт количества аудиторий
        with self.connection:
            count_string = self.cursor.execute("SELECT COUNT(*) as count FROM `au_auditories`").fetchone()
            count_auditories = int(count_string[0])
            return count_auditories

    def add_auditory(self, au_auditoryName):
        #Добавление новой аудитории
        with self.connection:
            au_ID = self.auditories_count() + 1
            return self.cursor.execute("INSERT INTO `au_auditories` (`au_ID`, `au_auditoryName`) VALUES(?,?)", (au_ID, au_auditoryName))



    def get_groups(self):
        #Получение всех групп
        with self.connection:
            return self.cursor.execute("SELECT `gr_groupName` FROM `gr_groups`").fetchall()

    def group_exists(self, gr_groupName):
        #Проверка есть ли группа в базе
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `gr_groups` WHERE `gr_groupName` = ?", (gr_groupName,)).fetchall()
            return bool(len(result))

    def groups_count(self):
        #Подсчёт количества групп
        with self.connection:
            count_string = self.cursor.execute("SELECT COUNT(*) as count FROM `gr_groups`").fetchone()
            count_groups = int(count_string[0])
            return count_groups

    def add_group(self, gr_groupName):
        #Добавление новой группы
        with self.connection:
            gr_ID = self.groups_count() + 1
            return self.cursor.execute("INSERT INTO `gr_groups` (`gr_ID`, `gr_groupName`) VALUES(?,?)", (gr_ID, gr_groupName))



    def get_subjects(self):
        #Получение всех предметов
        with self.connection:
            return self.cursor.execute("SELECT `su_subjectName` FROM `su_subjects`").fetchall()

    def subject_exists(self, su_subjectName):
        #Проверка есть ли предмет в базе
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `su_subjects` WHERE `su_subjectName` = ?", (su_subjectName,)).fetchall()
            return bool(len(result))

    def subjects_count(self):
        #Подсчёт количества предметов
        with self.connection:
            count_string = self.cursor.execute("SELECT COUNT(*) as count FROM `su_subjects`").fetchone()
            count_subjects = int(count_string[0])
            return count_subjects

    def add_subject(self, su_subjectName):
        #Добавление нового предмета
        with self.connection:
            su_ID = self.subjects_count() + 1
            return self.cursor.execute("INSERT INTO `su_subjects` (`su_ID`, `su_subjectName`) VALUES(?,?)", (su_ID, su_subjectName))



    def get_lessonTypes(self):
        #Получение всех видов занятий
        with self.connection:
            return self.cursor.execute("SELECT `ty_lessonType` FROM `ty_typeLesson`").fetchall()

    def lessonType_exists(self, ty_lessonType):
        #Проверка есть ли вид занятия в базе
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `ty_typeLesson` WHERE `ty_lessonType` = ?", (ty_lessonType,)).fetchall()
            return bool(len(result))

    def lessonTypes_count(self):
        #Подсчёт количества видов занятий
        with self.connection:
            count_string = self.cursor.execute("SELECT COUNT(*) as count FROM `ty_typeLesson`").fetchone()
            count_lessonTypes = int(count_string[0])
            return count_lessonTypes

    def add_lessonType(self, ty_lessonType):
        #Добавление нового вида занятия
        with self.connection:
            ty_ID = self.lessonTypes_count() + 1
            return self.cursor.execute("INSERT INTO `ty_typeLesson` (`ty_ID`, `ty_lessonType`) VALUES(?,?)", (ty_ID, ty_lessonType))



    def get_lessonTime(self):
        #Получение расписания звонков по дням недели
        with self.connection:
            return self.cursor.execute("SELECT * FROM `le_lessonTime`").fetchall()

    def get_lessonTimeDayNumber(self, le_dayOfWeek, le_numberLesson):
        #Получение расписания звонков на нужную пару
        with self.connection:
            return self.cursor.execute("SELECT * FROM `le_lessonTime` WHERE `le_dayOfWeek` = ? AND `le_numberLesson` = ?", (le_dayOfWeek,le_numberLesson)).fetchall()

    def lessonTime_exists(self, le_dayOfWeek, le_numberLesson):
        #Проверка есть ли расписание пары в определенный день недели
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `le_lessonTime` WHERE `le_dayOfWeek` = ? AND `le_numberLesson` = ?", (le_dayOfWeek,le_numberLesson)).fetchall()
            return bool(len(result))

    def lessonTime_count(self):
        #Подсчёт количества расписаний звонков
        with self.connection:
            count_string = self.cursor.execute("SELECT COUNT(*) as count FROM `le_lessonTime`").fetchone()
            count_lessonTime = int(count_string[0])
            return count_lessonTime

    def add_lessonTime(self, le_dayOfWeek, le_numberLesson, le_startLesson = '00:00', le_endLesson = '00:00', le_startBreak = '00:00', le_endBreak = '00:00'):
        #Добавление нового расписания звонка
        with self.connection:
            return self.cursor.execute("INSERT INTO `le_lessonTime` (`le_dayOfWeek`, `le_numberLesson`, `le_startLesson`, `le_endLesson`, `le_startBreak`, `le_endBreak`) VALUES(?,?,?,?,?,?)", (le_dayOfWeek, le_numberLesson, le_startLesson, le_endLesson, le_startBreak, le_endBreak))

    def update_lessonTime(self, le_dayOfWeek, le_numberLesson, le_startLesson = '00:00', le_endLesson = '00:00', le_startBreak = '00:00', le_endBreak = '00:00'):
        #Обновление времени пары
        with self.connection:
            return self.cursor.execute("UPDATE `le_lessonTime` SET `le_startLesson` = ?, `le_endLesson` = ?, `le_startBreak` = ?, `le_endBreak` = ? WHERE `le_dayOfWeek` = ? AND `le_numberLesson` = ?", (le_startLesson, le_endLesson, le_startBreak, le_endBreak, le_dayOfWeek, le_numberLesson))



    def get_teachers(self):
        #Получение всех учителей
        with self.connection:
            return self.cursor.execute("SELECT * FROM `te_teachers`").fetchall()

    def get_teacherFromID(self, te_ID):
        #Получение ФИО учителя по ID
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `te_teachers` WHERE `te_ID` = ?", (te_ID,)).fetchall()
            if (bool(len(result))):
                teacherName = str(result[0][1] + ' ' + result[0][2] + ' ' + result[0][3])
            else:
                teacherName = 'Такого учителя не существует!'
            return teacherName

    def get_teacherIDFromSurname(self, te_surname):
        #Получение ID учителя по фамилии
        with self.connection:
            result = self.cursor.execute("SELECT `te_ID` FROM `te_teachers` WHERE `te_surname` = ?", (te_surname,)).fetchone()
            return int(result[0])

    def get_teacherMiddleName(self, te_surname, te_name):
        #Получение отчества учителя по фамилии
        with self.connection:
            return self.cursor.execute("SELECT `te_middleName` FROM `te_teachers` WHERE `te_surname` = ? AND `te_name` = ?", (te_surname, te_name)).fetchone()

    def teacher_existsFromName(self, te_surname = 'Неизвестно', te_name = 'Неизвестно', te_middleName = 'Неизвестно'): #Добавил по умолчанию неизвестно, если у преподавателя будет только имя и фамилия, но его все равно можно будет легко достать из бд
        #Проверка есть ли такой учитель в бд
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `te_teachers` WHERE `te_surname` = ? AND `te_name` = ? AND `te_middleName` = ?", (te_surname,te_name,te_middleName)).fetchall()
            return bool(len(result))

    def teacher_exists(self, te_ID):
        #Проверка есть ли такой учитель в бд
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `te_teachers` WHERE `te_ID` = ?", (te_ID,)).fetchall()
            return bool(len(result))

    def teacher_existsSurName(self, te_surname, te_name):
        #Проверка есть ли такой учитель в бд по имени и фамилии
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `te_teachers` WHERE `te_surname` = ? AND `te_name` = ?", (te_surname, te_name)).fetchall()
            return bool(len(result))

    def teachers_count(self):
        #Подсчёт количества учителей
        with self.connection:
            count_string = self.cursor.execute("SELECT COUNT(*) as count FROM `te_teachers`").fetchone()
            count_teachers = int(count_string[0])
            return count_teachers

    def add_teacher(self, te_surname = 'Неизвестно', te_name = 'Неизвестно', te_middleName = 'Неизвестно'):
        #Добавление нового учителя
        with self.connection:
            return self.cursor.execute("INSERT INTO `te_teachers` (`te_surname`, `te_name`, `te_middleName`) VALUES(?,?,?)", (te_surname, te_name, te_middleName))

    def update_teacher(self, te_ID, te_surname = 'Неизвестно', te_name = 'Неизвестно', te_middleName = 'Неизвестно'):
        #Обновление ФИО учителя
        with self.connection:
            return self.cursor.execute("UPDATE `te_teachers` SET `te_surname` = ?, `te_name` = ?, `te_middleName` = ? WHERE `te_ID` = ?", (te_surname, te_name, te_middleName, te_ID))
    


    def get_usersAll(self):
        #Получение всех пользователей
        with self.connection:
            return self.cursor.execute("SELECT * FROM `us_users`").fetchall()

    def get_userFromID(self, us_ID):
        #Получение всех данных пользователя по ID
        with self.connection:
            return self.cursor.execute("SELECT * FROM `us_users` WHERE `us_ID` = ?", (us_ID,)).fetchall()

    def get_usersID(self):
        #Получение id всех пользователей
        with self.connection:
            result = self.cursor.execute("SELECT `us_ID` FROM `us_users`").fetchall()
            return result

    def get_usersActiveNotify(self, us_notification = True):
        #Получение всех пользователей с включенной подпиской на уведомления
        with self.connection:
            return self.cursor.execute("SELECT * FROM `us_users` WHERE `us_notification` = ?", (us_notification,)).fetchall()

    def get_usersIDActiveNotify(self, us_notification = True):
        #Получение id всех пользователей
        with self.connection:
            return self.cursor.execute("SELECT `us_ID` FROM `us_users` WHERE `us_notification` = ?", (us_notification,)).fetchall()

    def get_usersActiveSub(self):
        #Получение всех пользователей с активной подпиской
        with self.connection:
            current_date = date.today()
            return self.cursor.execute("SELECT * FROM `us_users` WHERE `us_daysLeftSub` >= ?", (current_date,)).fetchall()

    def get_userNameFromID(self, us_ID):
        #Получение имени и фамилии пользователя по ID
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `us_users` WHERE `us_ID` = ?", (us_ID,)).fetchall()
            if (bool(len(result))):
                userName = str(result[0][1] + ' ' + result[0][2])
            else:
                userName = 'Такого пользователя не существует!'
            return userName

    def user_exists(self, us_ID):
        #Проверка есть ли пользователь в базе
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `us_users` WHERE `us_ID` = ?", (us_ID,)).fetchall()
            return bool(len(result))

    def user_checkNotify(self, us_ID):
        #Проверка включены ли уведомления у пользователя
        with self.connection:
            us_notification = True
            result = self.cursor.execute("SELECT * FROM `us_users` WHERE `us_notification` = ? AND `us_ID` = ?", (us_notification, us_ID)).fetchall()
            return bool(len(result))

    def user_checkSub(self, us_ID):
        #Проверка наличия подписки у пользователя
        with self.connection:
            current_date = date.today()
            result = self.cursor.execute("SELECT * FROM `us_users` WHERE `us_daysLeftSub` >= ? AND `us_ID` = ?", (current_date, us_ID)).fetchall()
            return bool(len(result))

    def users_count(self):
        #Подсчёт количества пользователей
        with self.connection:
            count_string = self.cursor.execute("SELECT COUNT(*) as count FROM `us_users`").fetchone()
            count_users = int(count_string[0])
            return count_users

    def add_user(self, us_ID, us_name = 'Неизвестно', us_surname = 'Неизвестно', us_status = 'Студент', us_notification = True, us_daysLeftSub = '2010-01-01', us_group = 'Неизвестно'):
        #Добавление нового пользователя. ID пользователя в идеале брать из ВК
        with self.connection:
            return self.cursor.execute("INSERT INTO `us_users` (`us_ID`, `us_name`, `us_surname`, `us_status`, `us_notification`, `us_daysLeftSub`, `us_group`) VALUES(?,?,?,?,?,?,?)", (us_ID, us_name, us_surname, us_status, us_notification, us_daysLeftSub, us_group))

    def update_user(self, us_ID, us_name = 'Неизвестно', us_surname = 'Неизвестно', us_status = 'Студент', us_notification = True, us_daysLeftSub = '2010-01-01', us_group = 'Неизвестно'):
        #Обновление всех данных пользователя по id
        with self.connection:
            return self.cursor.execute("UPDATE `us_users` SET `us_name` = ?, `us_surname` = ?, `us_status` = ?, `us_notification` = ?, `us_daysLeftSub` = ?, `us_group` = ? WHERE `us_ID` = ?", (us_name, us_surname, us_status, us_notification, us_daysLeftSub, us_group, us_ID))

    def update_userName(self, us_ID, us_name = 'Неизвестно'):
        #Обновление имени пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `us_users` SET `us_name` = ? WHERE `us_ID` = ?", (us_name, us_ID))

    def update_userSurname(self, us_ID, us_surname = 'Неизвестно'):
        #Обновление фамилии пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `us_users` SET `us_surname` = ? WHERE `us_ID` = ?", (us_surname, us_ID))

    def update_userStatus(self, us_ID, us_status = 'Студент'):
        #Обновление статуса пользователя Студент/Преподаватель
        with self.connection:
            return self.cursor.execute("UPDATE `us_users` SET `us_status` = ? WHERE `us_ID` = ?", (us_status, us_ID))

    def update_userNotification(self, us_ID, us_notification = True):
        #Обновление статуса подписки на уведомления
        with self.connection:
            return self.cursor.execute("UPDATE `us_users` SET `us_notification` = ? WHERE `us_ID` = ?", (us_notification, us_ID))

    def update_userDaysLeftSub(self, us_ID, us_daysLeftSub = '2010-01-01'):
        #Обновление даты окончания подписки
        with self.connection:
            return self.cursor.execute("UPDATE `us_users` SET `us_daysLeftSub` = ? WHERE `us_ID` = ?", (us_daysLeftSub, us_ID))

    def update_userGroup(self, us_ID, us_group = 'Неизвестно'):
        #Обновление группы пользователя
        with self.connection:
            return self.cursor.execute("UPDATE `us_users` SET `us_group` = ? WHERE `us_ID` = ?", (us_group, us_ID))



    def get_timetableFromGroup(self, ti_group):
        #Получение всего расписания для группы
        with self.connection:
            return self.cursor.execute("SELECT * FROM `ti_timetable` WHERE `ti_group` = ?", (ti_group,)).fetchall()

    def get_timetableFromAuditory(self, ti_auditory):
        #Получение всего расписания для аудитории
        with self.connection:
            return self.cursor.execute("SELECT * FROM `ti_timetable` WHERE `ti_auditory` = ?", (ti_auditory,)).fetchall()

    def get_timetableFromTeacher(self, ti_teacher):
        #Получение всего расписания для преподавателя
        with self.connection:
            return self.cursor.execute("SELECT * FROM `ti_timetable` WHERE `ti_teacher` = ?", (ti_teacher,)).fetchall()

    def get_timetableFromGroupDate(self, ti_group, ti_lessonDate = '2010-01-01'):
        #Получение всего расписания для группы на определенную дату
        with self.connection:
            return self.cursor.execute("SELECT * FROM `ti_timetable` WHERE `ti_group` = ? AND `ti_lessonDate` = ?", (ti_group, ti_lessonDate)).fetchall()

    def get_timetableFromAuditoryDate(self, ti_auditory, ti_lessonDate = '2010-01-01'):
        #Получение всего расписания для аудитории на определенную дату
        with self.connection:
            return self.cursor.execute("SELECT * FROM `ti_timetable` WHERE `ti_auditory` = ? AND `ti_lessonDate` = ?", (ti_auditory, ti_lessonDate)).fetchall()

    def get_timetableFromTeacherDate(self, ti_teacher, ti_lessonDate = '2010-01-01'):
        #Получение всего расписания для преподавателя на определенную дату
        with self.connection:
            return self.cursor.execute("SELECT * FROM `ti_timetable` WHERE `ti_teacher` = ? AND `ti_lessonDate` = ?", (ti_teacher, ti_lessonDate)).fetchall()

    def get_timetableFromGroupDateNum(self, ti_group, ti_lessonNumber = 1, ti_lessonDate = '2010-01-01'):
        #Возращает одну пару по ее номеру, группе и дате
        with self.connection:
         return self.cursor.execute("SELECT * FROM `ti_timetable` WHERE `ti_group` = ? AND `ti_lessonDate` = ? AND `ti_lessonNumber` = ?", (ti_group, ti_lessonDate, ti_lessonNumber)).fetchone()

    def get_timetableIDFromGroupDate(self, ti_group, ti_lessonNumber = 1, ti_lessonDate = '2010-01-01'):
        with self.connection:
            rows = self.cursor.execute("SELECT `ti_ID` FROM `ti_timetable` WHERE `ti_group` = ? AND `ti_lessonDate` = ? AND `ti_lessonNumber` = ?", (ti_group, ti_lessonDate, ti_lessonNumber)).fetchall()
            for row in rows:
                return row[0]

    def timetableGroupDate_exists(self, ti_group, ti_lessonDate = '2010-01-01'):
        #Проверка есть ли раписание на заданный день у группы в базе
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `ti_timetable` WHERE `ti_group` = ? AND `ti_lessonDate` = ?", (ti_group, ti_lessonDate)).fetchall()
            return bool(len(result))
    
    def timetableGroupDate_exist(self, ti_group, ti_subject, ti_number, ti_lessonType, ti_lessonDate = '2010-01-01'):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `ti_timetable` WHERE `ti_group` = ? AND `ti_lessonDate` = ?  AND `ti_lessonNumber` = ? AND `ti_lessonType` = ? AND `ti_subject` = ?",
                 (ti_group, ti_lessonDate, ti_number, ti_lessonType, ti_subject)).fetchall()
            return bool(len(result))

    def timetableAuditoryDate_exists(self, ti_auditory, ti_lessonDate = '2010-01-01'):
        #Проверка есть ли раписание на заданный день у аудитории в базе
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `ti_timetable` WHERE `ti_auditory` = ? AND `ti_lessonDate` = ?", (ti_auditory, ti_lessonDate)).fetchall()
            return bool(len(result))

    def timetableTeacherDate_exists(self, ti_teacher, ti_lessonDate = '2010-01-01'):
        #Проверка есть ли раписание на заданный день у преподавателя в базе
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `ti_timetable` WHERE `ti_teacher` = ? AND `ti_lessonDate` = ?", (ti_teacher, ti_lessonDate)).fetchall()
            return bool(len(result))

    def add_timetable(self, ti_group, ti_dayOfWeek, ti_lessonNumber, ti_auditory, ti_subject, ti_lessonType, ti_teacher, ti_lessonDate):
        #Добавление новой пары
        with self.connection:
            return self.cursor.execute("INSERT INTO `ti_timetable` (`ti_group`, `ti_dayOfWeek`, `ti_lessonNumber`, `ti_auditory`, `ti_subject`, `ti_lessonType`, `ti_teacher`, `ti_lessonDate`) VALUES(?,?,?,?,?,?,?,?)", (ti_group, ti_dayOfWeek, ti_lessonNumber, ti_auditory, ti_subject, ti_lessonType, ti_teacher, ti_lessonDate))

    def update_timetableGroup(self, ti_ID, ti_group):
        #Обновление группы по ID
        with self.connection:
            return self.cursor.execute("UPDATE `ti_timetable` SET `ti_group` = ? WHERE `ti_ID` = ?", (ti_group, ti_ID))

    def update_timetableDayOfWeek(self, ti_ID, ti_dayOfWeek):
        #Обновление дня недели по ID
        with self.connection:
            return self.cursor.execute("UPDATE `ti_timetable` SET `ti_dayOfWeek` = ? WHERE `ti_ID` = ?", (ti_dayOfWeek, ti_ID))

    def update_timetableLessonNumber(self, ti_ID, ti_lessonNumber):
        #Обновление номера пары по ID
        with self.connection:
            return self.cursor.execute("UPDATE `ti_timetable` SET `ti_lessonNumber` = ? WHERE `ti_ID` = ?", (ti_lessonNumber, ti_ID))

    def update_timetableAuditory(self, ti_ID, ti_auditory):
        #Обновление аудитории по ID
        with self.connection:
            return self.cursor.execute("UPDATE `ti_timetable` SET `ti_auditory` = ? WHERE `ti_ID` = ?", (ti_auditory, ti_ID))

    def update_timetableSubject(self, ti_ID, ti_subject):
        #Обновление предмета по ID
        with self.connection:
            return self.cursor.execute("UPDATE `ti_timetable` SET `ti_subject` = ? WHERE `ti_ID` = ?", (ti_subject, ti_ID))

    def update_timetableLessonType(self, ti_ID, ti_lessonType):
        #Обновление вида занятия по ID
        with self.connection:
            return self.cursor.execute("UPDATE `ti_timetable` SET `ti_lessonType` = ? WHERE `ti_ID` = ?", (ti_lessonType, ti_ID))

    def update_timetableTeacher(self, ti_ID, ti_teacher):
        #Обновление id преподавателя по ID
        with self.connection:
            return self.cursor.execute("UPDATE `ti_timetable` SET `ti_teacher` = ? WHERE `ti_ID` = ?", (ti_teacher, ti_ID))

    def update_timetableLessonDate(self, ti_ID, ti_lessonDate):
        #Обновление даты пары по ID
        with self.connection:
            return self.cursor.execute("UPDATE `ti_timetable` SET `ti_lessonDate` = ? WHERE `ti_ID` = ?", (ti_lessonDate, ti_ID))

    def update_timetable(self, ti_ID, ti_group, ti_dayOfWeek, ti_lessonNumber, ti_auditory, ti_subject, ti_lessonType, ti_teacher, ti_lessonDate):
        #Обновление расписания по ID
        with self.connection:
            return self.cursor.execute(
                "UPDATE `ti_timetable` SET `ti_lessonDate` = ?, `ti_group` = ?, `ti_dayOfWeek` = ?, `ti_lessonNumber` = ?, `ti_auditory` = ?, `ti_subject` = ?, `ti_lessonType` = ?, `ti_teacher` = ? WHERE `ti_ID` = ?",
                 (ti_lessonDate, ti_group, ti_dayOfWeek, ti_lessonNumber, ti_auditory, ti_subject, ti_lessonType, ti_teacher, ti_ID))



    def close(self):
        #Закрытие соединения с БД
        self.connection.close()