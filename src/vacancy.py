class Vacancy:
    def __init__(self, title, link, city, salary, description):
        self.title = title
        self.link = link
        self.city = city
        self.salary = salary
        self.description = description

    def __repr__(self):
        return f"Vacancy('{self.title}', '{self.link}', '{self.salary}', '{self.description}')"

    def __eq__(self, other):
        return self.salary == other.salary

    def __lt__(self, other):
        return self.salary < other.salary

