@@ -0,0 +1,344 @@
import re
import datetime
import sys
import os
import csv


def clear_screen():
    """Clear Screen"""
    try:
        os.system('cls')

    except:
        os.system('clear')


def show_menu():
    """A menu to choose whether to add a new entry or lookup previous entries"""
    print("""What do you want to do?\n
        [A]dd new entry
        [S]earch an entry
        [Q]uit""")

    menu_input = input("Please select the first character of the option: ")

    if menu_input.lower().strip() == 'a':
        add_entry()

    elif menu_input.lower().strip() == 's':
        search_entry()

    elif menu_input.lower().strip() == 'q':
        sys.exit()

    else:
        print('Please select an option')
        show_menu()


def add_entry():
    """Add a new work log, provide task name, a number of minutes spent, provide additional notes"""
    name = time = notes = date = ''

    while not name or name.isspace():
        name = input('Please enter the name task or 9 to main menu: ')
        if name == '9':
            show_menu()

    while not time:
        try:
            time = int(input('Please enter time spent on: '))
        except ValueError:
            print('Please enter a valid number')
    notes = input('Please enter any note about the task (optional): ')

    if notes.isspace():
        notes = None
    date = datetime.datetime.now().strftime('%m/%d/%Y')

    """save information to csv file"""
    with open("work_log.csv", 'a+', newline='') as csvfile:
        fieldnames = ['name', 'time', 'notes', 'date']
        wl_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        wl_writer.writeheader()
        wl_writer.writerow({'name': name, 'time': time, 'notes': notes, 'date': date})
        saved = input('Task is saved, save another task? [Y/N]')
        if saved.lower() == 'y':
            add_entry()
        else:
            show_menu()


def search_entry():
    """Pick option to find a previous entry by four options: Date, time spent, exact search, pattern"""
    search_menu = input('''Please enter what option you want to search:
  [D]ate
  [T]ime spent
  [E]xact search
  [P]attern
  [M]ain menu\n''')

    if search_menu.lower().strip() == 'd':
        date_search()

    elif search_menu.lower().strip() == 't':
        time_search()

    elif search_menu.lower().strip() == 'e':
        exact_search()

    elif search_menu.lower().strip() == 'p':
        pattern_search()

    elif search_menu.lower().strip() == 'm':
        show_menu()

    else:
        print('Please enter a valid option')
        search_entry()


def date_input(date):
    while len(date) == 0:
        try:
            input_string = input('>>>')
            date.append(datetime.datetime.strptime(input_string, '%m/%d/%Y'))
        except ValueError:
            print('Date must be valid and in format MM/DD/YY')


def date_search():
    """search by exact date or range date"""
    date1 = []
    date2 = []
    date_option = None

    while not date_option:
        date_option = input('''Please enter the option to search:
    [1] - Search by a specific date
    [2] - Search by a range of date\n
    ''')
        if date_option not in ['1', '2']:
            print('Not valid option')
            date_option = None

    print('Enter {} date in format MM/DD/YYYY'.format('start' if date_option == '2' else ''))

    date_input(date1)
    if date_option == '2':
        print('Input end date in format MM/DD/YY')
        while not date2:
            date_input(date2)
            if date1[0].timestamp() > date2[0].timestamp():
                print('''First date must be ealier than end date.
        Please enter valid date again.''')
                date2 = []

    search_result = []

    with open('work_log.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        if date_option == '1':
            for row in reader:
                if (datetime.datetime.strptime(row['date'], '%m/%d/%Y') == date1[0]):
                    search_result.append(row)

        elif date_option == '2':
            for row in reader:
                if ((datetime.datetime.strptime(row['date'], '%m/%d/%Y').timestamp() >= date1[0].timestamp()) and (
                        datetime.datetime.strptime(row['date'], '%m/%d/%Y').timestamp() <= date2[0].timestamp())):
                    search_result.append(row)

    result_option(search_result)


def time_search():
    """Search by time spent"""
    search_time = None
    search_result = []

    while not search_time:
        search_time = input('Please enter time spent in minutes: ')
        try:
            search_time = int(search_time)
        except ValueError:
            print('Please enter a valid number')
            search_time = None
        else:
            search_time = str(search_time)

    with open('work_log.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['time'] == search_time:
                search_result.append(row)

    result_option(search_result)


def exact_search():
    """Search by exact search"""
    string_search = None
    search_result = []

    print('Enter text to start searching')

    while not string_search or string_search.isspace():
        string_search = input('>>> ')
    with open('work_log.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if ((row['name'].find(string_search) > -1) or (row['notes'].find(string_search) > -1)):
                search_result.append(row)

    result_option(search_result)


def pattern_search():
    """Search by pattern"""
    pattern = None
    search_result = []

    print('Please enter the pattern')

    while not pattern:
        pattern = input('>>> ')
        try:
            pattern = re.compile(pattern)
        except re.error:
            print('Please enter a valid pattern')
            pattern = None

    with open('work_log.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (re.search(pattern, row['name'])
                    or re.search(pattern, row['time'])
                    or re.search(pattern, row['date'])
                    or re.search(pattern, row['notes'])):
                search_result.append(row)
        result_option(search_result)


def result_option(search_result):
    """Find result or not"""
    if len(search_result) == 0:
        print('No result')
        a = input('Enter s to search again, other keys to get back to menu: ')
        if a.lower() == 's':
            search_entry()
        else:
            show_menu()

    else:
        display_result(search_result)


def display_result(results):
    """Display search result"""
    count = 1
    for result in results:
        print('''Result {} of {}\n
    Task name: {}, Spent time: {}, Date: {}, Notes: {}\n'''.format(count, len(results), result['name'], result['time'],
                                                                   result['date'], result['notes']))
        selection = None
        print('Please select one option')
        while not selection:
            selection = input('''
      [E]dit
      [D]elete
      [M]enu
      {}\n'''.format('[N]ext' if count < len(results) else ''))
        if selection.lower() == 'e':
            edit(result)
        if selection.lower() == 'd':
            delete(result)
        if selection.lower() == 'm':
            show_menu()
        if selection.lower() != 'n':
            selection = None
        count += 1

    print('There is no result left')


def edit(result_dict):
    """Edit result"""
    field_dict = {'1': 'name', '2': 'time', '3': 'date', '4': 'notes'}
    field = None

    while not field:
        field = input('''
    Please select field to edit:
    [1] Name
    [2] Time
    [3] Date
    [4] Notes
    [5] Go back to main menu\n''')
        if field == '5':
            show_menu()

    print('The current {} of the entry is {}'.format(field_dict[field], result_dict[field_dict[field]]))

    new_infor = None

    while not new_infor or new_infor.isspace():
        new_infor = input('Please enter new {}\n'.format(field_dict[field]))
        if field == '2':
            try:
                new_infor = int(new_infor)
            except ValueError:
                print('Please enter a valid number')
            else:
                new_infor = str(new_infor)
        if field == '3':
            try:
                datetime.datetime.strptime(new_infor, '%d/%m/%Y')
            except ValueError:
                print('Please enter a valid date follow format DD/MM/YYYY')
                new_infor = None

    edited = []

    with open('work_log.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row == result_dict:
                row[field_dict[field]] = new_infor
                edited.append(row)
            else:
                edited.append(row)

    with open('work_log.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'time', 'notes', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in edited:
            writer.writerow({'name': row['name'], 'time': row['time'], 'notes': row['notes'], 'date': row['date']})
    print('Entry edited')


def delete(result_dict):
    """Delete entry"""
    deleted = []

    with open('work_log.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row == result_dict:
                continue
            else:
                deleted.append(row)

    with open('work.log.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'time', 'notes', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in deleted:
            writer.writerow({'name': row['name'], 'time': row['time'], 'notes': row['notes'], 'date': row['date']})
    print('Entry is deleted')


if __name__ == '__main__':
    show_menu()
