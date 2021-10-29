from vkbottle.bot import Bot,Message
from vkbottle import Keyboard,KeyboardButtonColor, \
    Text, \
    GroupEventType,GroupTypes,VKAPIError
from vkbottle_types import BaseStateGroup
from vkbottle import CtxStorage, EMPTY_KEYBOARD
from datetime import date, timedelta

from db import MODULE_RASP_DB
dbusers = MODULE_RASP_DB('dbtimetable.db')

bot = Bot(token="ac9d7b04ae21a6ffb8fa8c0829be1b3720c631260c54a8dec86acd8203750f0755c0d720247ceca581938")
bot.on.vbml_ignore_case = True
ctx = CtxStorage()

#Клавиатура выбора
keyboardchoise = Keyboard(one_time=False)
keyboardchoise.add(Text("Студент",{"cmd":"studentGroup"}))
keyboardchoise.add(Text("Преподаватель",{"cmd":"teacherTest"}))

#Клавиатура главного меню
keyboardmain = Keyboard(one_time=False)
keyboardmain.add(Text("Расписание",{"cmd":"rasp"}),color=KeyboardButtonColor.PRIMARY)
keyboardmain.row()
keyboardmain.add(Text("Настройки",{"cmd":"settings"}))

#Клавиатура расписания
keyboardrasp = Keyboard(one_time=False)
keyboardrasp.add(Text("Сегодня",{"cmd":"today"}),color=KeyboardButtonColor.PRIMARY)
keyboardrasp.add(Text("Завтра",{"cmd":"tomorrow"}),color=KeyboardButtonColor.PRIMARY)
keyboardrasp.add(Text("Неделя",{"cmd":"week"}),color=KeyboardButtonColor.PRIMARY)
keyboardrasp.row()
keyboardrasp.add(Text("Назад",{"cmd":"main"}))

#Клавиатура настроек
keyboardsettings = Keyboard(one_time=False)
keyboardsettings.add(Text("Подписаться на рассылку",{"cmd":"sub"}),color=KeyboardButtonColor.POSITIVE)
keyboardsettings.add(Text("Отписаться от рассылки",{"cmd":"unsub"}),color=KeyboardButtonColor.NEGATIVE)
keyboardsettings.row()
keyboardsettings.add(Text("Сменить группу",{"cmd":"changeGroup"}))
keyboardsettings.row()
keyboardsettings.add(Text("Назад",{"cmd":"main"}))

#Клавиатура настроек препода
keyboardsettingsTeacher = Keyboard(one_time=False)
keyboardsettingsTeacher.add(Text("Подписаться на рассылку",{"cmd":"sub"}),color=KeyboardButtonColor.POSITIVE)
keyboardsettingsTeacher.add(Text("Отписаться от рассылки",{"cmd":"unsub"}),color=KeyboardButtonColor.NEGATIVE)
keyboardsettingsTeacher.row()
keyboardsettingsTeacher.add(Text("Назад",{"cmd":"main"}))



class RegData(BaseStateGroup):
    GROUP = 0



@bot.on.private_message(text='Начать')
@bot.on.private_message(text='Начало')
@bot.on.private_message(text='Старт')
@bot.on.private_message(payload={"cmd":"choise"})
async def choise(Message: Message):
    user = await bot.api.users.get(Message.from_id)
    firstName = user[0].first_name
    lastName = user[0].last_name
    userID = user[0].id

    if(not dbusers.user_exists(userID)): # если юзера нет в базе, добавляем его
        dbusers.add_user(userID, firstName, lastName)
    else: # если он уже есть, то просто обновляем ему статус подписки
        dbusers.update_userNotification(userID)

    await Message.answer("Выберите кем вы являетесь: Студент/Преподаватель",keyboard=keyboardchoise)

#@bot.on.private_message(text='Меню')
@bot.on.private_message(payload={"cmd":"main"})
async def mainmenu(Message: Message):
    await Message.answer("📍 Главное меню 📍",keyboard=keyboardmain) #Введите свою группу

#@bot.on.private_message(text='')
@bot.on.private_message(payload={"cmd":"rasp"})
async def rasp(Message: Message):
    await Message.answer("📄 Меню расписания 📄",keyboard=keyboardrasp)

#@bot.on.private_message(text='')
@bot.on.private_message(payload={"cmd":"settings"})
async def settings(Message: Message):
    user = await bot.api.users.get(Message.from_id)
    userID = user[0].id

    if (dbusers.get_userFromID(userID)[0][3] == 'Студент'):
        textAnswer = '⚙ Настройки ⚙\n\nВаша группа: ' + str(dbusers.get_userFromID(userID)[0][6])
        if (dbusers.user_checkNotify(userID)):
            textAnswer += '\nУведомления о расписании: Включены'
        else:
            textAnswer += '\nУведомления о расписании: Выключены'
        await Message.answer(textAnswer,keyboard=keyboardsettings)
    elif (dbusers.get_userFromID(userID)[0][3] == 'Преподаватель'):
        textAnswer = 'Настройки'
        if (dbusers.user_checkNotify(userID)):
            textAnswer += '\nУведомления о расписании: Включены'
        else:
            textAnswer += '\nУведомления о расписании: Выключены'
        await Message.answer(textAnswer,keyboard=keyboardsettingsTeacher)

#@bot.on.private_message(text='Преподаватель')
@bot.on.private_message(payload={"cmd":"teacherTest"})
async def teacherAdd(Message: Message):
    user = await bot.api.users.get(Message.from_id)
    name = user[0].first_name
    surname = user[0].last_name
    userID = user[0].id

    if (dbusers.teacher_existsSurName(surname, name)):
        dbusers.update_userStatus(userID, 'Преподаватель')
        await Message.answer("📍 Главное меню 📍\n\nВы успешно авторизованы!",keyboard=keyboardmain)
    else:
        await Message.answer("⚠ Вы не являетесь преподавателем! ⚠",keyboard=keyboardchoise)
    
@bot.on.private_message(payload={"cmd":"sub"})
async def userSub(Message: Message):
    user = await bot.api.users.get(Message.from_id)
    userID = user[0].id
    if(not dbusers.user_exists(userID)):
        # если юзера нет в базе, добавляем его
        firstName = user[0].first_name
        lastName = user[0].last_name

        dbusers.add_user(userID, firstName, lastName)
        await Message.answer("Выберите кем вы являетесь: Студент/Преподаватель",keyboard=keyboardchoise)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        user = await bot.api.users.get(Message.from_id)
        userID = user[0].id

        dbusers.update_userNotification(userID)
        await Message.answer("Спасибо за подписку на рассылку расписания😊",keyboard=keyboardmain)

@bot.on.private_message(payload={"cmd":"unsub"})
async def userUnsub(Message: Message):
    user = await bot.api.users.get(Message.from_id)
    userID = user[0].id
    if(not dbusers.user_exists(userID)):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        firstName = user[0].first_name
        lastName = user[0].last_name

        dbusers.add_user(userID, firstName, lastName)
        dbusers.update_userNotification(userID, False)
        await Message.answer("Вы и так не подписаны, и не зарегистрированы😔\nВыберите кем вы являетесь: Студент/Преподаватель",keyboard=keyboardchoise)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        dbusers.update_userNotification(userID, False)
        await Message.answer("Будем ждать вас снова😔",keyboard=keyboardmain)

@bot.on.private_message(payload={"cmd":"changeGroup"})
async def groupChange(Message: Message):
    await Message.answer("👥 Введите свою группу 👥",{"cmd":"studentGroup"},keyboard=EMPTY_KEYBOARD)

@bot.on.private_message(payload={"cmd":"today"})
async def raspToday(Message: Message):
    current_date = date.today()
    user = await bot.api.users.get(Message.from_id)
    firstName = user[0].first_name
    lastName = user[0].last_name
    userID = user[0].id #event.object.user_id

    if (dbusers.user_exists(userID)): #Пользователь есть в базе

        if (dbusers.get_userFromID(userID)[0][3] == 'Студент'): # если пользователь является студентом

            usergroup = dbusers.get_userFromID(userID)[0][6] #Узнать группу

            if (dbusers.timetableGroupDate_exists(usergroup, current_date)): #Если раписание на текущий день есть, для группы
                todayTimetable = dbusers.get_timetableFromGroupDate(usergroup, current_date)
                textTimetable = '✅ ' + str(todayTimetable[0][2]).upper() + ' ' + str(todayTimetable[0][8]) + ' ✅\n'# + '\nРасписание на сегодня:\n\n'
                startLesson = ''
                endLesson = ''
                startBreak = ''
                endBreak = ''

                for i in range(len(todayTimetable)):
                    if (dbusers.lessonTime_exists(todayTimetable[i][2], todayTimetable[i][3])):
                        lessonTime = dbusers.get_lessonTimeDayNumber(todayTimetable[i][2], todayTimetable[i][3])
                        startLesson = str(lessonTime[0][3])
                        endLesson = str(lessonTime[0][4])
                        startBreak = str(lessonTime[0][5])
                        endBreak = str(lessonTime[0][6])
                    textTimetable += (str(todayTimetable[i][3]) + '. ' + str(todayTimetable[i][5]) + '\nВремя: с ' + startLesson + ' до ' + endLesson + '\nПерерыв: с ' + startBreak + ' до ' + endBreak + '\nАудитория: ' + str(todayTimetable[i][4]) + '\nВид занятия: ' + str(todayTimetable[i][6]) + '\nПреподаватель: ' + str(todayTimetable[i][7]) + '\n\n')

                await Message.answer(textTimetable,keyboard=keyboardrasp)
            else: #Если группа не введена, либо нет расписания
                if (str(dbusers.get_userFromID(userID)[0][6]) == 'Неизвестно'): #Если группа пользователя не введена
                    await Message.answer("👥 Введите свою группу 👥",{"cmd":"studentGroup"},keyboard=EMPTY_KEYBOARD)
                else: #Если нет расписания
                    await Message.answer('Расписание на ' + str(current_date) + ' отсутствует',keyboard=keyboardrasp)

        elif (dbusers.get_userFromID(userID)[0][3] == 'Преподаватель'):

            teacherMiddleName = dbusers.get_teacherMiddleName(lastName, firstName)[0]
            teacherFullName = lastName + ' ' + firstName + ' ' + teacherMiddleName

            if (dbusers.timetableTeacherDate_exists(teacherFullName, current_date)): #Если раписание на текущий день есть, для преподов
                todayTimetable = dbusers.get_timetableFromTeacherDate(teacherFullName, current_date)
                textTimetable = '✅ ' + str(todayTimetable[0][2]).upper() + ' ' + str(todayTimetable[0][8]) + ' ✅\n'# + '\nРасписание на сегодня:\n\n'
                startLesson = ''
                endLesson = ''
                startBreak = ''
                endBreak = ''

                for i in range(len(todayTimetable)):
                    if (dbusers.lessonTime_exists(todayTimetable[i][2], todayTimetable[i][3])):
                        lessonTime = dbusers.get_lessonTimeDayNumber(todayTimetable[i][2], todayTimetable[i][3])
                        startLesson = str(lessonTime[0][3])
                        endLesson = str(lessonTime[0][4])
                        startBreak = str(lessonTime[0][5])
                        endBreak = str(lessonTime[0][6])
                    textTimetable += (str(todayTimetable[i][3]) + '. ' + str(todayTimetable[i][5]) + '\nВремя: с ' + startLesson + ' до ' + endLesson + '\nПерерыв: с ' + startBreak + ' до ' + endBreak + '\nАудитория: ' + str(todayTimetable[i][4]) + '\nВид занятия: ' + str(todayTimetable[i][6]) + '\nПреподаватель: ' + str(todayTimetable[i][7]) + '\n\n')

                await Message.answer(textTimetable,keyboard=keyboardrasp)
            else: #Если группа не введена, либо нет расписания
                '''if (str(dbusers.get_userFromID(userID)[0][6]) == 'Неизвестно'): #Если группа пользователя не введена
                    await Message.answer("Введите свою группу",{"cmd":"studentGroup"},keyboard=EMPTY_KEYBOARD)
                else: #Если нет расписания'''
                await Message.answer('Расписание на ' + str(current_date) + ' отсутствует',keyboard=keyboardrasp)

    else: #Пользователя нет в базе
        dbusers.add_user(userID, firstName, lastName) #Добавить пользователя
        await Message.answer("Вы не зарегистрированы!\nВыберите кем вы являетесь: Студент/Преподаватель",keyboard=keyboardchoise)

@bot.on.private_message(payload={"cmd":"tomorrow"})
async def raspTomorrow(Message: Message):
    current_date = date.today() + timedelta(days=1)
    user = await bot.api.users.get(Message.from_id)
    firstName = user[0].first_name
    lastName = user[0].last_name
    userID = user[0].id

    if (dbusers.user_exists(userID)): #Пользователь есть в базе

        if (dbusers.get_userFromID(userID)[0][3] == 'Студент'): # если пользователь является студентом

            usergroup = dbusers.get_userFromID(userID)[0][6] #Узнать группу

            if (dbusers.timetableGroupDate_exists(usergroup, current_date)): #Если раписание на текущий день есть, для группы
                todayTimetable = dbusers.get_timetableFromGroupDate(usergroup, current_date)
                textTimetable = '✅ ' + str(todayTimetable[0][2]).upper() + ' ' + str(todayTimetable[0][8]) + ' ✅\n'# + '\nРасписание на сегодня:\n\n'
                startLesson = ''
                endLesson = ''
                startBreak = ''
                endBreak = ''

                for i in range(len(todayTimetable)):
                    if (dbusers.lessonTime_exists(todayTimetable[i][2], todayTimetable[i][3])):
                        lessonTime = dbusers.get_lessonTimeDayNumber(todayTimetable[i][2], todayTimetable[i][3])
                        startLesson = str(lessonTime[0][3])
                        endLesson = str(lessonTime[0][4])
                        startBreak = str(lessonTime[0][5])
                        endBreak = str(lessonTime[0][6])
                    textTimetable += (str(todayTimetable[i][3]) + '. ' + str(todayTimetable[i][5]) + '\nВремя: с ' + startLesson + ' до ' + endLesson + '\nПерерыв: с ' + startBreak + ' до ' + endBreak + '\nАудитория: ' + str(todayTimetable[i][4]) + '\nВид занятия: ' + str(todayTimetable[i][6]) + '\nПреподаватель: ' + str(todayTimetable[i][7]) + '\n\n')

                await Message.answer(textTimetable,keyboard=keyboardrasp)
            else: #Если группа не введена, либо нет расписания
                if (str(dbusers.get_userFromID(userID)[0][6]) == 'Неизвестно'): #Если группа пользователя не введена
                    await Message.answer("👥 Введите свою группу 👥",{"cmd":"studentGroup"},keyboard=EMPTY_KEYBOARD)
                else: #Если нет расписания
                    await Message.answer('Расписание на ' + str(current_date) + ' отсутствует',keyboard=keyboardrasp)

        elif (dbusers.get_userFromID(userID)[0][3] == 'Преподаватель'):

            teacherMiddleName = dbusers.get_teacherMiddleName(lastName, firstName)[0]
            teacherFullName = lastName + ' ' + firstName + ' ' + teacherMiddleName

            if (dbusers.timetableTeacherDate_exists(teacherFullName, current_date)): #Если раписание на текущий день есть, для преподов
                todayTimetable = dbusers.get_timetableFromTeacherDate(teacherFullName, current_date)
                textTimetable = '✅ ' + str(todayTimetable[0][2]).upper() + ' ' + str(todayTimetable[0][8]) + ' ✅\n'# + '\nРасписание на сегодня:\n\n'
                startLesson = ''
                endLesson = ''
                startBreak = ''
                endBreak = ''

                for i in range(len(todayTimetable)):
                    if (dbusers.lessonTime_exists(todayTimetable[i][2], todayTimetable[i][3])):
                        lessonTime = dbusers.get_lessonTimeDayNumber(todayTimetable[i][2], todayTimetable[i][3])
                        startLesson = str(lessonTime[0][3])
                        endLesson = str(lessonTime[0][4])
                        startBreak = str(lessonTime[0][5])
                        endBreak = str(lessonTime[0][6])
                    textTimetable += (str(todayTimetable[i][3]) + '. ' + str(todayTimetable[i][5]) + '\nВремя: с ' + startLesson + ' до ' + endLesson + '\nПерерыв: с ' + startBreak + ' до ' + endBreak + '\nАудитория: ' + str(todayTimetable[i][4]) + '\nВид занятия: ' + str(todayTimetable[i][6]) + '\nПреподаватель: ' + str(todayTimetable[i][7]) + '\n\n')

                await Message.answer(textTimetable,keyboard=keyboardrasp)
            else: #Если группа не введена, либо нет расписания
                '''if (str(dbusers.get_userFromID(userID)[0][6]) == 'Неизвестно'): #Если группа пользователя не введена
                    await Message.answer("Введите свою группу",{"cmd":"studentGroup"},keyboard=EMPTY_KEYBOARD)
                else: #Если нет расписания'''
                await Message.answer('Расписание на ' + str(current_date) + ' отсутствует',keyboard=keyboardrasp)

    else: #Пользователя нет в базе
        dbusers.add_user(userID, firstName, lastName) #Добавить пользователя
        await Message.answer("Вы не зарегистрированы!\nВыберите кем вы являетесь: Студент/Преподаватель",keyboard=keyboardchoise)
        
@bot.on.private_message(payload={"cmd":"week"})
async def raspWeek(Message: Message):
    user = await bot.api.users.get(Message.from_id)
    firstName = user[0].first_name
    lastName = user[0].last_name
    userID = user[0].id



    if (dbusers.user_exists(userID)): #Пользователь есть в базе
        usergroup = dbusers.get_userFromID(userID)[0][6] #Узнать группу
        textTimetable = ''

        if (dbusers.get_userFromID(userID)[0][3] == 'Студент'): # если пользователь является студентом

            for j in range(7):
                current_date = date.today() + timedelta(days=j)

                if (dbusers.timetableGroupDate_exists(usergroup, current_date)): #Если раписание на текущий день есть, для группы
                    todayTimetable = dbusers.get_timetableFromGroupDate(usergroup, current_date)

                    textTimetable += '✅ ' + str(todayTimetable[0][2]).upper() + ' ' + str(todayTimetable[0][8]) + ' ✅\n'
                    startLesson = ''
                    endLesson = ''
                    startBreak = ''
                    endBreak = ''
                    for i in range(len(todayTimetable)):
                        if (dbusers.lessonTime_exists(todayTimetable[i][2], todayTimetable[i][3])):
                            lessonTime = dbusers.get_lessonTimeDayNumber(todayTimetable[i][2], todayTimetable[i][3])
                            startLesson = str(lessonTime[0][3])
                            endLesson = str(lessonTime[0][4])
                            startBreak = str(lessonTime[0][5])
                            endBreak = str(lessonTime[0][6])
                        textTimetable += (str(todayTimetable[i][3]) + '. ' + str(todayTimetable[i][5]) + '\nВремя: с ' + startLesson + ' до ' + endLesson + '\nПерерыв: с ' + startBreak + ' до ' + endBreak + '\nАудитория: ' + str(todayTimetable[i][4]) + '\nВид занятия: ' + str(todayTimetable[i][6]) + '\nПреподаватель: ' + str(todayTimetable[i][7]) + '\n\n')
                    textTimetable += '\n'
                else: #Если группа не введена, либо нет расписания
                    if (str(dbusers.get_userFromID(userID)[0][6]) == 'Неизвестно'): #Если группа пользователя не введена
                        await Message.answer("👥 Введите свою группу 👥",{"cmd":"studentGroup"},keyboard=EMPTY_KEYBOARD)
                        break
                    else: #Если нет расписания
                        textTimetable += '\nРасписание на ' + str(current_date) + ' отсутствует\n\n'
            await Message.answer(textTimetable,keyboard=keyboardrasp)

        elif (dbusers.get_userFromID(userID)[0][3] == 'Преподаватель'):

            teacherMiddleName = dbusers.get_teacherMiddleName(lastName, firstName)[0]
            teacherFullName = lastName + ' ' + firstName + ' ' + teacherMiddleName

            for j in range(7):
                current_date = date.today() + timedelta(days=j)

                if (dbusers.timetableTeacherDate_exists(teacherFullName, current_date)): #Если раписание на текущий день есть, для группы
                    todayTimetable = dbusers.get_timetableFromTeacherDate(teacherFullName, current_date)

                    textTimetable += '✅ ' + str(todayTimetable[0][2]).upper() + ' ' + str(todayTimetable[0][8]) + ' ✅\n'
                    startLesson = ''
                    endLesson = ''
                    startBreak = ''
                    endBreak = ''
                    for i in range(len(todayTimetable)):
                        if (dbusers.lessonTime_exists(todayTimetable[i][2], todayTimetable[i][3])):
                            lessonTime = dbusers.get_lessonTimeDayNumber(todayTimetable[i][2], todayTimetable[i][3])
                            startLesson = str(lessonTime[0][3])
                            endLesson = str(lessonTime[0][4])
                            startBreak = str(lessonTime[0][5])
                            endBreak = str(lessonTime[0][6])
                        textTimetable += (str(todayTimetable[i][3]) + '. ' + str(todayTimetable[i][5]) + '\nВремя: с ' + startLesson + ' до ' + endLesson + '\nПерерыв: с ' + startBreak + ' до ' + endBreak + '\nАудитория: ' + str(todayTimetable[i][4]) + '\nВид занятия: ' + str(todayTimetable[i][6]) + '\nПреподаватель: ' + str(todayTimetable[i][7]) + '\n\n')
                    textTimetable += '\n'
                else: #Если группа не введена, либо нет расписания
                    if (str(dbusers.get_userFromID(userID)[0][6]) == 'Неизвестно'): #Если группа пользователя не введена
                        await Message.answer("Введите свою группу",{"cmd":"studentGroup"},keyboard=EMPTY_KEYBOARD)
                        break
                    else: #Если нет расписания
                        textTimetable += '\nРасписание на ' + str(current_date) + ' отсутствует\n\n'
            await Message.answer(textTimetable,keyboard=keyboardrasp)

    else: #Пользователя нет в базе
        dbusers.add_user(userID, firstName, lastName) #Добавить пользователя
        await Message.answer("Вы не зарегистрированы!\nВыберите кем вы являетесь: Студент/Преподаватель",keyboard=keyboardchoise)

'''
@bot.on.private_message(payload={"cmd":"week"})
async def raspWeek(Message: Message):
    user = await bot.api.users.get(Message.from_id)
    firstName = user[0].first_name
    lastName = user[0].last_name
    userID = user[0].id

    if (dbusers.user_exists(userID)): #Пользователь есть в базе
        usergroup = dbusers.get_userFromID(userID)[0][6] #Узнать группу

        for j in range(7):
            current_date = date.today() + timedelta(days=j)

            if (dbusers.timetableGroupDate_exists(usergroup, current_date)): #Если раписание на текущий день есть, для группы
                todayTimetable = dbusers.get_timetableFromGroupDate(usergroup, current_date)
                textTimetable = str(todayTimetable[0][2]).upper() + ' ' + str(todayTimetable[0][8]) + '\n'# + '\nРасписание на сегодня:\n\n'
                for i in range(len(todayTimetable)):
                    textTimetable += (str(todayTimetable[i][3]) + '. ' + str(todayTimetable[i][5]) + '\nВремя: с ' + ' до ' + '\nАудитория: ' + str(todayTimetable[i][4]) + '\nВид занятия: ' + str(todayTimetable[i][6]) + '\nПреподаватель: ' + str(todayTimetable[i][7]) + '\n')

                await Message.answer(textTimetable,keyboard=keyboardrasp)
            else: #Если группа не введена, либо нет расписания
                if (str(dbusers.get_userFromID(userID)[0][6]) == 'Неизвестно'): #Если группа пользователя не введена
                    await Message.answer("Введите свою группу",{"cmd":"studentGroup"},keyboard=EMPTY_KEYBOARD)
                    break
                else: #Если нет расписания
                    await Message.answer('Расписание на ' + str(current_date) + ' отсутствует',keyboard=keyboardrasp)
    else: #Пользователя нет в базе
        dbusers.add_user(userID, firstName, lastName) #Добавить пользователя
        await Message.answer("Вы не зарегистрированы!\nВыберите кем вы являетесь: Студент/Преподаватель",keyboard=keyboardchoise)
'''

@bot.on.private_message(payload={"cmd":"studentGroup"})
async def student(Message: Message):
    user = await bot.api.users.get(Message.from_id)
    userID = user[0].id

    if (dbusers.user_exists(userID)): #Пользователь существует
        dbusers.update_userStatus(userID, 'Студент')
    else: #Пользователь не существует
        firstName = user[0].first_name
        lastName = user[0].last_name

        dbusers.add_user(userID, firstName, lastName)

    await Message.answer('👥 Введите вашу группу 👥',keyboard=EMPTY_KEYBOARD)
    await bot.state_dispenser.set(Message.peer_id, RegData.GROUP)
    #return 'Введите вашу группу'

@bot.on.private_message(state=RegData.GROUP)
async def inputGroup(Message: Message):
    groupName = Message.text.upper()
    user = await bot.api.users.get(Message.from_id)
    userID = user[0].id

    if (dbusers.group_exists(groupName)): #Группа существует
        if (dbusers.user_exists(userID)): #Пользователь существует
            dbusers.update_userGroup(userID, groupName)
            await Message.answer("📍 Главное меню 📍\n\nВы успешно авторизованы!",keyboard=keyboardmain)
        else: # Пользователь не существует
            firstName = user[0].first_name
            lastName = user[0].last_name

            dbusers.add_user(userID, firstName, lastName)

            dbusers.update_userGroup(userID, groupName)
            await Message.answer("📍 Главное меню 📍\n\nВы успешно авторизованы!",keyboard=keyboardmain)
    else: #Группа не существует
        await Message.answer("⚠ Введённая группа несуществует, повторите попытку ⚠",{"cmd":"studentGroup"},keyboard=EMPTY_KEYBOARD)



@bot.on.raw_event(GroupEventType.GROUP_JOIN,dataclass=GroupTypes.GroupJoin)
async def group_join(event: GroupTypes.GroupJoin):
    try:
        await bot.api.messages.send(
            peer_id=event.object.user_id,
            message="Привет, на связи МАС Бот. Я бот расписания ПВГУСА. \nЧто я умею? \nАвтоматически присылать расписание на сегодня, завтра и неделю для твоей группы. \n\nНапиши слово (Начать) что бы начать пользоваться ботом.",
            random_id=0
        )
    except VKAPIError(901):
        pass

@bot.on.raw_event(GroupEventType.GROUP_LEAVE,dataclass=GroupTypes.GroupLeave)
async def group_leave(event: GroupTypes.GroupLeave):
    try:
        await bot.api.messages.send(
            peer_id=event.object.user_id,
            message="Очень жаль, что ты решил отписаться :(",
            random_id=0
        )
    except VKAPIError(901):
        pass

bot.run_forever()