from abc import ABC, abstractmethod
import requests
from src.vacancy import Vacancy
from src.vacancy_storage import JSONVacancyStorage
import os

class VacancyAPI(ABC):

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
    def __init__(self):
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
    if os.path.exists(file_path):
        os.remove(file_path)

    if platform == '1':
        api_obj = HeadHunterAPI()  # Используем переданный объект API
        vacancies = api_obj.get_vacancies(search_query)
        for vacancy_data in vacancies:
            vacancy = Vacancy(
                title=vacancy_data['name'],
                link='https://hh.ru/vacancy/' + vacancy_data["id"],
                city=vacancy_data['area']['name'],
                salary_from=vacancy_data['payment_from'],
                salary_to=vacancy_data['payment_to'],
                description=vacancy_data['candidat'][0:10]
            )
            storage.add_vacancy(vacancy)
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
                    description=vacancy_data['candidat'][0:10]
                )
                storage.add_vacancy(vacancy)
                print(vacancy)
            except KeyError:
                pass


    else:
        print("Неверный выбор платформы.")
        return


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