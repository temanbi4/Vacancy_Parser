import json
from abc import ABC, abstractmethod
from src.vacancy import Vacancy
import os

class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, min_salary, max_salary):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass

class JSONVacancyStorage(VacancyStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def add_vacancy(self, vacancy):
        with open(self.file_path, 'a') as file:
            json.dump(vacancy.__dict__, file, ensure_ascii=False)
            file.write('\n')

    def get_vacancies_by_salary(self, min_salary, max_salary):
        vacancies = []
        with open(self.file_path, 'r') as file:
            for line in file:
                vacancy_data = json.loads(line)
                salary = vacancy_data['salary']
                if min_salary <= salary <= max_salary:
                    vacancies.append(Vacancy(**vacancy_data))
        return vacancies


    def delete_vacancy(self, vacancy):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        with open(self.file_path, 'w') as file:
            for line in lines:
                vacancy_data = json.loads(line)
                if vacancy_data['title'] != vacancy.title:
                    file.write(line)
