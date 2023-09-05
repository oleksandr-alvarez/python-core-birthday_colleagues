from datetime import date, datetime, timedelta


def get_birthdays_per_week(users):

    if len(users) == 0:
        print('The provided list is empty')
        return {}

    from collections import namedtuple, defaultdict
    
    today = date.today()
    week_from_now = today + timedelta(weeks = 1)

    Colleague = namedtuple("Colleage", ['name', 'birthday'])
    list_of_colleagues = []
    birthday_passed_dct = {}
    birthday_far_away = {}

    dct = defaultdict(list)


    for user in users:
        user['birthday'] = datetime(today.year, user.get("birthday").month, user.get("birthday").day).date()
        list_of_colleagues.append(Colleague(**user))
    
    for colleague in list_of_colleagues:
        if today > colleague.birthday and \
            today > datetime(today.year + 1, \
                          colleague.birthday.month, \
                            colleague.birthday.day).date() > week_from_now:
            birthday_passed_dct[colleague.name] = colleague.birthday.strftime('%d %B')
            
        elif today <= colleague.birthday <= week_from_now or \
        today <= datetime(today.year + 1, \
                          colleague.birthday.month, \
                            colleague.birthday.day).date() <= week_from_now:
            if colleague.birthday.weekday() not in [5,6]:
                dct[colleague.birthday.strftime('%A')].append(colleague.name)   
            else:
                dct['Monday'].append(colleague.name)

        else:
            birthday_far_away[colleague.name] = colleague.birthday.strftime('%d %B')
    
    birthday_passed_dct = dict(sorted(birthday_passed_dct.items(), key=lambda x: datetime.strptime(x[1], '%d %B'), reverse=False)) 
    birthday_far_away = dict(sorted(birthday_far_away.items(), key=lambda x: datetime.strptime(x[1], '%d %B')))
    week_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dct = dict(sorted(dict(dct).items(), key=lambda x: week_names.index(x[0])))


    if len(birthday_passed_dct) == len(users):
        print("Birthdays of all colleagues have already passed")
        print(f'These colleagues are {birthday_passed_dct}')
        return {}
    elif len(birthday_far_away) == len(users):
        print("This week there are no colleagues who have birthdays")
        print(f'The colleagues who have birthdays in more than a week: {birthday_far_away}')
        return {}
    elif len(dct) > 0:
        return dict(dct)
    else:
        print('There are not birthdays this week')
        print(f"The passed birthdays are: {birthday_passed_dct}")
        print(f"Birthdays in more than a week: {birthday_far_away}")
        return {}

if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
