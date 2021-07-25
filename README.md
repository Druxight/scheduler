# Get started
1. Input your schedule into `schedule.json`
2. Create bot in BotFather and insert TOKEN into `schedule_bot.py`
3. Setup your bot using BotFather commands (e.g. description, about, commands, image, etc.)
4. If you want, you can change text messages in `schedule_bot.py`
5. Test your bot using `python schedule_bot.py`
6. Host it in the Internet (e.g. free hosting in heroku - [tutorial](https://teletype.in/@cozy_codespace/Hk70-Ntl4))

# How to fill `schedule.json`?
```
{
    "Понеділок": {                                  <--- Day name
        "1": {                                      <--- Number of lesson
            "1": {                                  <--- Lesson in first week
                "Назва": "Програмування 1",         <--- Lesson title
                "Тип заняття": "лекц.",             <--- Lesson type
                "Корпус": 55,                       <--- Building number
                "Аудиторія": "ВФ",                  <--- Classroom
                "Викладач": "проф. Нікельман П.О."  <--- Teacher's name
            },
            "2": {                                  <--- Lesson in second week
                "Назва": "Українська мова",         <--- Lesson title
                "Тип заняття": "пр.",               <--- Lesson type
                "Корпус": 87,                       <--- Building number
                "Аудиторія": "257-3",               <--- Classroom
                "Викладач": "доц. Іванова С.В."     <--- Teacher's name
            }
        },
        ...
        "5": {                                      <--- Number of lesson
            "1": "",                                <--- Lesson in first week | If you haven't lesson, stay ""
            "2": ""                                 <--- Lesson in second week | If you haven't lesson, stay ""
        }
    },
    ...                                             <--- Continue filling all weekdays, when you have lessons
    ...
    "П'ятниця": {                                   <--- Day name
        "1": {                                      <--- Number of lesson
          ...
        },
    ...
    }
}
```

# License
[MIT License](./LICENSE)
