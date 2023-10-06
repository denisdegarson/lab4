import random
import csv
from faker import Faker
from faker.providers import BaseProvider

class New_Provider(BaseProvider):
    def female_middle_name(self):
        female_middle_names = [
            "Іванівна",
            "Петрівна",
            "Володимирівна",
            "Андріївна",
            "Олександрівна",
            "Вікторівна",
            "Сергіївна",
            "Федорівна",
            "Михайлівна",
            "Дмитрівна"
        ]
        return random.choice(female_middle_names)

    def male_middle_name(self):
        male_middle_names = [
            "Петрович",
            "Іванович",
            "Олександрович",
            "Юрійович",
            "Юрійович",
            "Вікторович",
            "Іванович",
            "Анатолійович",
            "Олегович",
            "Олексійович"
        ]
        return random.choice(male_middle_names)
def create_table():
    fake = Faker('uk_UA')
    fake.add_provider(New_Provider)
    count = 2000
    table = []
    for i in range(count):
        if i < count * 0.4:
            gender = "Жіноча"
            name = fake.first_name_female()
            middle_name = fake.female_middle_name()

        else:
            gender = "Чоловіча"
            name = fake.first_name_male()
            middle_name = fake.male_middle_name()

        birthdate = fake.date_of_birth(minimum_age=15, maximum_age=85)
        record = {
            "Прізвище": fake.last_name(),
            "Ім’я": name,
            "По батькові": middle_name,
            "Стать": gender,
            "Дата народження": birthdate.strftime('%d.%m.%Y'),
            "Посада": fake.job(),
            "Місто проживання": fake.city(),
            "Адреса проживання": fake.address(),
            "Телефон": fake.phone_number(),
            "Email": fake.email()
        }
        table.append(record)
    try:
        with open('employees.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=table[0].keys())

            writer.writeheader()

            for record in table:
                writer.writerow(record)

        print("Дані були успішно записані у файл 'employees.csv'.")

    except Exception as e:
        print(f"Сталася помилка при відкритті/записі файлу CSV: {e}")


if __name__ == '__main__':
    create_table()
