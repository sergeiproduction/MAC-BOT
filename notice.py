from asyncio.events import get_event_loop
from asyncio.tasks import create_task, gather
from db import MODULE_RASP_DB as db
import vk_api
import asyncio
from vk_api.longpoll import VkLongPoll
from datetime import date, datetime, timedelta


token = "ac9d7b04ae21a6ffb8fa8c0829be1b3720c631260c54a8dec86acd8203750f0755c0d720247ceca581938"
vk = vk_api.VkApi(token=token)
db = db('dbtimetable.db')
longpoll = VkLongPoll(vk)
is_mailing = False

def sender(user_id, message):    
     vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})

async def mailing():
    users = db.get_usersIDActiveNotify()
    for user in users:         
        #sender(user, f"Здарова, {user} чел")

        current_date = date.today() + timedelta(days=1)
        #user = await bot.api.users.get(Message.from_id)
        #firstName = user[0].first_name
        #lastName = user[0].last_name
        userID = user[0]
        firstName = db.get_userFromID(userID)[0][1]
        lastName = db.get_userFromID(userID)[0][2]

        if (db.user_exists(userID)): #Пользователь есть в базе

            if (db.get_userFromID(userID)[0][3] == 'Студент'): # если пользователь является студентом

                usergroup = db.get_userFromID(userID)[0][6] #Узнать группу

                if (db.timetableGroupDate_exists(usergroup, current_date)): #Если раписание на текущий день есть, для группы
                    todayTimetable = db.get_timetableFromGroupDate(usergroup, current_date)
                    textTimetable = 'Ежедневная рассылка расписания\n\n' + '✅ ' + str(todayTimetable[0][2]).upper() + ' ' + str(todayTimetable[0][8]) + ' ✅\n'# + '\nРасписание на сегодня:\n\n'
                    startLesson = ''
                    endLesson = ''
                    startBreak = ''
                    endBreak = ''

                    for i in range(len(todayTimetable)):
                        if (db.lessonTime_exists(todayTimetable[i][2], todayTimetable[i][3])):
                            lessonTime = db.get_lessonTimeDayNumber(todayTimetable[i][2], todayTimetable[i][3])
                            startLesson = str(lessonTime[0][3])
                            endLesson = str(lessonTime[0][4])
                            startBreak = str(lessonTime[0][5])
                            endBreak = str(lessonTime[0][6])
                        textTimetable += (str(todayTimetable[i][3]) + '. ' + str(todayTimetable[i][5]) + '\nВремя: с ' + startLesson + ' до ' + endLesson + '\nПерерыв: с ' + startBreak + ' до ' + endBreak + '\nАудитория: ' + str(todayTimetable[i][4]) + '\nВид занятия: ' + str(todayTimetable[i][6]) + '\nПреподаватель: ' + str(todayTimetable[i][7]) + '\n\n')

                    sender(user, textTimetable)
                else: #Если группа не введена, либо нет расписания
                    if (str(db.get_userFromID(userID)[0][6]) == 'Неизвестно'): #Если группа пользователя не введена
                        print('У ' + lastName + ' ' + firstName + ' не введена группа')
                        #sender(user, 'Чтобы получать ежедневную рассылку расписания, пожалуйста введите группу. Если вы не хотите ее получать, отпишитесь в настройках')
                    else: #Если нет расписания
                        sender(user, 'Расписание на ' + str(current_date) + ' отсутствует')

            elif (db.get_userFromID(userID)[0][3] == 'Преподаватель'):

                teacherMiddleName = db.get_teacherMiddleName(lastName, firstName)[0]
                teacherFullName = lastName + ' ' + firstName + ' ' + teacherMiddleName

                if (db.timetableTeacherDate_exists(teacherFullName, current_date)): #Если раписание на текущий день есть, для преподов
                    todayTimetable = db.get_timetableFromTeacherDate(teacherFullName, current_date)
                    textTimetable = 'Ежедневная рассылка расписания\n\n' + '✅ ' + str(todayTimetable[0][2]).upper() + ' ' + str(todayTimetable[0][8]) + ' ✅\n'# + '\nРасписание на сегодня:\n\n'
                    startLesson = ''
                    endLesson = ''
                    startBreak = ''
                    endBreak = ''

                    for i in range(len(todayTimetable)):
                        if (db.lessonTime_exists(todayTimetable[i][2], todayTimetable[i][3])):
                            lessonTime = db.get_lessonTimeDayNumber(todayTimetable[i][2], todayTimetable[i][3])
                            startLesson = str(lessonTime[0][3])
                            endLesson = str(lessonTime[0][4])
                            startBreak = str(lessonTime[0][5])
                            endBreak = str(lessonTime[0][6])
                        textTimetable += (str(todayTimetable[i][3]) + '. ' + str(todayTimetable[i][5]) + '\nВремя: с ' + startLesson + ' до ' + endLesson + '\nПерерыв: с ' + startBreak + ' до ' + endBreak + '\nАудитория: ' + str(todayTimetable[i][4]) + '\nВид занятия: ' + str(todayTimetable[i][6]) + '\nПреподаватель: ' + str(todayTimetable[i][7]) + '\n\n')

                    sender(user, textTimetable)
                else: #Если группа не введена, либо нет расписания
                    sender(user, 'Расписание на ' + str(current_date) + ' отсутствует')

        else: #Пользователя нет в базе
            print('Всмысле нет в базе?')
            #db.add_user(userID, firstName, lastName) #Добавить пользователя
            #await Message.answer("Вы не зарегистрированы!\nВыберите кем вы являетесь: Студент/Преподаватель",keyboard=keyboardchoise)
        
async def main():      
    task_mailing = create_task(mailing())
    await gather(task_mailing)

async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        
        datenow = datetime.now()
        sendHour = 20 #Время отправки
        sendMinute = 00 #Время отправки

        print(f"Часов {datenow.hour} минут {datenow.minute} секунд {datenow.second} микросекунд {datenow.microsecond}") #Время рассылки

        if datenow.hour == sendHour and datenow.minute == sendMinute: #Если время совпадает
            await main() #Запуск цикла рассылки
            await asyncio.sleep(wait_for)


if __name__ == "__main__":
    loop = get_event_loop() #Инициализация цикла
    loop.run_until_complete(scheduled(40)) #Запуск поллинга, каждые 45 секунд программа проверяет наступило ли заданное время, и если да, запускает рассылку