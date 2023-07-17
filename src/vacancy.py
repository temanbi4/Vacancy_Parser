class Vacancy:
    def __init__(self, title, link, city, salary_from, salary_to, description):
        """
        Конструктор класса Vacancy.

        Args:
            title (str): Название вакансии.
            link (str): Ссылка на вакансию.
            city (str): Город, в котором расположена вакансия.
            salary_from (int): Минимальная зарплата для вакансии.
            salary_to (int): Максимальная зарплата для вакансии.
            description (str): Описание вакансии.
        """
        self.title = title
        self.link = link
        self.city = city
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description

    def __repr__(self):
        """
        Метод, возвращающий строковое представление объекта Vacancy.

        Returns:
            str: Строковое представление объекта Vacancy.
        """
        return f"Vacancy('{self.title}', '{self.link}', '{self.salary_from}', '{self.description}')"

    def __eq__(self, other):
        """
        Метод для проверки равенства двух объектов Vacancy по полю salary_from.

        Args:
            other (Vacancy): Другой объект Vacancy для сравнения.

        Returns:
            bool: True, если значения полей salary_from у объектов равны, иначе False.
        """
        return self.salary_from == other.salary

    def __lt__(self, other):
        """
        Метод для сравнения двух объектов Vacancy по полю salary_from.

        Args:
            other (Vacancy): Другой объект Vacancy для сравнения.

        Returns:
            bool: True, если значение поля salary_from текущего объекта меньше значения поля salary_from другого объекта,
                  иначе False.
        """
        return self.salary_from < other.salary
