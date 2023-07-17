import json
from abc import ABC, abstractmethod

class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_city(self, city):
        pass

class JSONVacancyStorage(VacancyStorage):
    def __init__(self, file_path):
        """
        Конструктор класса JSONVacancyStorage.

        Args:
            file_path (str): Путь к файлу, в который будут сохраняться вакансии в формате JSON.
        """
        self.file_path = file_path

    def add_vacancy(self, vacancy):
        """
        Метод для добавления новой вакансии в JSON файл.

        Args:
            vacancy (Vacancy): Объект вакансии, который необходимо сохранить.
        """
        # Прочитаем существующие данные из файла (если они есть)
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Если файл не существует или не является JSON, создадим пустой список
            data = []

        # Добавляем новую вакансию в список
        data.append(vacancy.__dict__)

        # Записываем обновленные данные в файл
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_vacancies_by_city(self, city):
        """
        Метод для получения списка вакансий по указанному городу.

        Args:
            city (str): Город, по которому необходимо произвести фильтрацию вакансий.

        Returns:
            list: Список вакансий, отфильтрованных по указанному городу.
        """
        with open(self.file_path, 'r') as file:
            data = json.load(file)

        # Фильтруем вакансии по указанному городу
        filtered_vacancies = [vacancy for vacancy in data if vacancy.get('city') == city]

        return filtered_vacancies
