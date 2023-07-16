class Vacancy:
    def __init__(self, title, link, city, salary_from, salary_to, description):
        self.title = title
        self.link = link
        self.city = city
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description

    def __repr__(self):
        return f"Vacancy('{self.title}', '{self.link}', '{self.salary_from}', '{self.description}')"

    def __eq__(self, other):
        return self.salary_from == other.salary

    def __lt__(self, other):
        return self.salary_from < other.salary

