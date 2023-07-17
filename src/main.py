from abc import ABC, abstractmethod
import requests
from src.vacancy import Vacancy
from src.vacancy_storage import JSONVacancyStorage
import os


# Абстрактный базовый класс, представляющий API для вакансий
class VacancyAPI(ABC):

    # Абстрактный метод для получения вакансий на основе поискового запроса
    @abstractmethod
    def get_vacancies(self, search_query):
        pass


# Класс, представляющий API HeadHunter и реализующий VacancyAPI
class HeadHunterAPI(VacancyAPI):
    def __init__(self):
        self.base_url = 'https://api.hh.ru'

    # Метод для получения вакансий из API HeadHunter на основе поискового запроса
    def get_vacancies(self, search_query):
        url = f'{self.base_url}/vacancies'
        params = {'text': search_query, 'per_page': 100}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()['items']


# Класс, представляющий API SuperJob и реализующий VacancyAPI
class SuperJobAPI(VacancyAPI):
    def __init__(self):
        self.base_url = 'https://api.superjob.ru/2.0'
        self.api_key = 'v3.r.137682939.5cd91634a0171c336eea416526733ac899ebe531.be4eb6f4ead27ffe6d9eb687fb4e6d3ad5237499'

    # Метод для подключения к API SuperJob и получения вакансий на основе поискового запроса
    def get_vacancies(self, search_query):
        url = f'{self.base_url}/vacancies'
        headers = {'X-Api-App-Id': self.api_key}
        params = {'keyword': search_query, 'per_page': 100, 'count': 100}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()['objects']


# Функция для поиска вакансий и сохранения их в JSON файл
def search_vacancies(storage):
    platform = input("Выберите платформу (1 - HeadHunter, 2 - SuperJob): ")
    search_query = input("Введите поисковый запрос: ")
    if os.path.exists(file_path):
        os.remove(file_path)

    if platform == '1':
        api_obj = HeadHunterAPI()  # Используем переданный объект API
        vacancies = api_obj.get_vacancies(search_query)
        for vacancy_data in vacancies:
            try:
                salary_data = vacancy_data['salary']
                salary_from = salary_data['from'] if salary_data and 'from' in salary_data else 0
                salary_to = salary_data['to'] if salary_data and 'to' in salary_data else 0

                snippet_data = vacancy_data.get('snippet')
                description = snippet_data.get('requirement', '') if snippet_data else ''

                vacancy = Vacancy(
                    title=vacancy_data['name'],
                    link='https://hh.ru/vacancy/' + vacancy_data["id"],
                    city=vacancy_data['area']['name'],
                    salary_from=salary_from,
                    salary_to=salary_to,
                    description=description
                )
                storage.add_vacancy(vacancy)
            except KeyError:
                pass

    elif platform == '2':
        api_obj = SuperJobAPI()  # Используем переданный объект API
        vacancies = api_obj.get_vacancies(search_query)
        for vacancy_data in vacancies:
            try:
                vacancy = Vacancy(
                    title=vacancy_data['profession'],
                    link=vacancy_data['link'],
                    city=vacancy_data['client']['town']['title'],
                    salary_from=vacancy_data['payment_from'],
                    salary_to=vacancy_data['payment_to'],
                    description=vacancy_data['candidat'][0:30]
                )
                storage.add_vacancy(vacancy)
            except KeyError:
                pass

    else:
        print("Неверный выбор платформы.")
        return


# Основная часть программы
if __name__ == "__main__":
    file_path = 'vacancies.json'
    storage = JSONVacancyStorage(file_path)

    print("1. Поиск вакансий")
    # print("2. Поиск вакансии по городу")
    print("0. Выйти")

    choice = input("Выберите действие: ")

    if choice == '1':
        search_vacancies(storage)
    elif choice == '0':
        quit()
    else:
        print("Неверный выбор.")

    print(f"Вакансии выгружены в Json файл. \n")
    print("1. Поиск вакансии по городу.")
    print("0. Выйти")
    choice = input("Выберите действие: ")

    if choice == '1':
        city = input("Введите город: ")
        vacancies = storage.get_vacancies_by_city(city)
        for vacancy in vacancies:
            print(vacancy)
    elif choice == '0':
        quit()
    else:
        print("Неверный выбор.")
