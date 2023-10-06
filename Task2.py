import csv
from datetime import datetime
from openpyxl import Workbook


def calculate_age(birthdate):
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def create_xlsx():
    try:
        # Відкриваємо файл CSV для читання
        with open('employees.csv', mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            workbook = Workbook()

            all_sheet = workbook.active
            all_sheet.title = 'all'
            all_sheet.append(csv_reader.fieldnames)
            for row in csv_reader:
                all_sheet.append(list(row.values()))

            age_categories = ["younger_18", "18-45", "45-70", "older_70"]
            for age_category in age_categories:
                sheet = workbook.create_sheet(age_category)
                sheet.append(["№", "Прізвище", "Ім’я", "По батькові", "Дата народження", "Вік"])

            csv_file.seek(0)
            next(csv_reader)
            for row in csv_reader:
                birthdate = datetime.strptime(row["Дата народження"], '%d.%m.%Y')
                age = calculate_age(birthdate)
                if age < 18:
                    sheet = workbook["younger_18"]
                elif 18 <= age <= 45:
                    sheet = workbook["18-45"]
                elif 45 < age <= 70:
                    sheet = workbook["45-70"]
                else:
                    sheet = workbook["older_70"]
                sheet.append(
                    [len(sheet['A']), row["Прізвище"], row["Ім’я"], row["По батькові"], row["Дата народження"], age])

            workbook.save('employees.xlsx')
            print("Excel-файл 'employees.xlsx' був успішно створений.")

    except FileNotFoundError:
        print("Помилка: файл 'employees.csv' не знайдено.")
    except Exception as e:
        print(f"Сталася помилка: {e}")


if __name__ == '__main__':
    create_xlsx()
