import csv
from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt


def calculate_age(birthdate):
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def load_csv_data():
    try:
        with open('employees.csv', mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data = list(csv_reader)
        return data
    except FileNotFoundError:
        print("Помилка: файл 'employees.csv' не знайдено.")
        return []
    except Exception as e:
        print(f"Сталася помилка: {e}")
        return []


def count_gender(data):
    gender_counts = defaultdict(int)
    for row in data:
        gender = row["Стать"]
        gender_counts[gender] += 1
    return gender_counts


def count_age_categories(data):
    age_categories = defaultdict(int)
    for row in data:
        birthdate = datetime.strptime(row["Дата народження"], '%d.%m.%Y')
        age = calculate_age(birthdate)
        if age < 18:
            category = "Молодший 18"
        elif 18 <= age <= 45:
            category = "18-45"
        elif 45 < age <= 70:
            category = "45-70"
        else:
            category = "Старше 70"
        age_categories[category] += 1
    return age_categories


def count_gender_age_categories(data):
    gender_age_counts = defaultdict(lambda: defaultdict(int))
    for row in data:
        gender = row["Стать"]
        birthdate = datetime.strptime(row["Дата народження"], '%d.%m.%Y')
        age = calculate_age(birthdate)
        if age < 18:
            category = "Молодший 18"
        elif 18 <= age <= 45:
            category = "18-45"
        elif 45 < age <= 70:
            category = "45-70"
        else:
            category = "Старше 70"
        gender_age_counts[gender][category] += 1
    return gender_age_counts


def plot_gender_pie(gender_counts):
    plt.figure(figsize=(8, 8))
    plt.pie(gender_counts.values(), labels=gender_counts.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("Розподіл за статтю")
    plt.show()


def plot_age_bar(age_categories):
    plt.figure(figsize=(10, 6))
    plt.bar(age_categories.keys(), age_categories.values())
    plt.xlabel("Вікова категорія")
    plt.ylabel("Кількість співробітників")
    plt.title("Розподіл за віком")
    plt.xticks(rotation=45)
    plt.show()


def plot_gender_age_bar(gender_age_counts):
    categories = list(gender_age_counts[list(gender_age_counts.keys())[0]].keys())
    bar_width = 0.35
    fig, ax = plt.subplots(figsize=(10, 6))
    for gender, counts in gender_age_counts.items():
        x = [i for i in range(len(categories))]
        y = list(counts.values())
        ax.bar([i + bar_width * list(gender_age_counts.keys()).index(gender) for i in x], y, bar_width, label=gender)
    ax.set_xlabel("Вікова категорія")
    ax.set_ylabel("Кількість співробітників")
    ax.set_title("Розподіл за віком та статтю")
    ax.set_xticks([i + bar_width for i in x])
    ax.set_xticklabels(categories)
    ax.legend()
    plt.show()


def main():
    data = load_csv_data()
    if not data:
        return

    gender_counts = count_gender(data)
    age_categories = count_age_categories(data)
    gender_age_counts = count_gender_age_categories(data)

    print("Розподіл за статтю:")
    for gender, count in gender_counts.items():
        print(f"{gender}: {count} співробітників")

    print("Розподіл за віком:")
    for category, count in age_categories.items():
        print(f"{category}: {count} співробітників")

    print("Розподіл за віком та статтю:")
    for gender, counts in gender_age_counts.items():
        print(f"{gender}:")
        for category, count in counts.items():
            print(f"  {category}: {count} співробітників")

    plot_gender_pie(gender_counts)
    plot_age_bar(age_categories)
    plot_gender_age_bar(gender_age_counts)


if __name__ == '__main__':
    main()
