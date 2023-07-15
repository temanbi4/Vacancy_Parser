from abc import ABC, abstractmethod
import requests
from src.vacancy import Vacancy
from src.vacancy_storage import JSONVacancyStorage


class VacancyAPI(ABC):
    @abstractmethod
    def connect_to_api(self):
        pass

    @abstractmethod
    def get_vacancies(self, search_query):
        pass



class HeadHunterAPI(VacancyAPI):
    def __init__(self):
        self.base_url = 'https://api.hh.ru'

    def get_vacancies(self, search_query):
        url = f'{self.base_url}/vacancies'
        params = {'text': search_query, 'per_page': 100}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()['items']


class SuperJobAPI(VacancyAPI):
    def __init__(self, api_key):
        self.base_url = 'https://api.superjob.ru/2.0'
        self.api_key = 'v3.r.137682939.5cd91634a0171c336eea416526733ac899ebe531.be4eb6f4ead27ffe6d9eb687fb4e6d3ad5237499'

    def connect_to_api(self):
        # Некоторый код для авторизации или настройки соединения, если необходимо
        pass

    def get_vacancies(self, search_query):
        url = f'{self.base_url}/vacancies'
        headers = {'X-Api-App-Id': self.api_key}
        params = {'keyword': search_query, 'per_page': 100, 'count': 100}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()['objects']
def search_vacancies(storage):
    platform = input("Выберите платформу (1 - HeadHunter, 2 - SuperJob): ")
    search_query = input("Введите поисковый запрос: ")

    if platform == '1':
        api_obj = HeadHunterAPI()  # Используем переданный объект API
    elif platform == '2':
        api_obj = SuperJobAPI()  # Используем переданный объект API
    else:
        print("Неверный выбор платформы.")
        return

    vacancies = api_obj.get_vacancies(search_query)
    for vacancy_data in vacancies:
        vacancy = Vacancy(
            title=vacancy_data['name'],
            link=vacancy_data['link'],
            salary=vacancy_data['salary'],
            description=vacancy_data['description']
        )
        storage.add_vacancy(vacancy)

if __name__ == "__main__":
    file_path = 'vacancies.json'
    storage = JSONVacancyStorage(file_path)

    while True:
        print("1. Поиск вакансий")
        print("2. Получить вакансии по зарплате")
        print("3. Удалить вакансию")
        print("0. Выйти")

        choice = input("Выберите действие: ")

        if choice == '1':
            search_vacancies(storage)
        elif choice == '2':
            min_salary = int(input("Введите минимальную зарплату: "))
            max_salary = int(input("Введите максимальную зарплату: "))
            vacancies = storage.get_vacancies_by_salary(min_salary, max_salary)
            for vacancy in vacancies:
                print(vacancy)
        elif choice == '3':
            title = input("Введите название вакансии для удаления: ")
            vacancy = Vacancy(title=title, link='', salary=0, description='')
            storage.delete_vacancy(vacancy)
        elif choice == '0':
            break
        else:
            print("Неверный выбор.")