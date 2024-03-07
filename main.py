import uuid
import json


class Employee:
    def __init__(self, name, title, department, ID=None):
        self.ID = ID if ID else uuid.uuid4()
        self.name = name
        self.title = title
        self.department = department

    def details(self):
        return f"{self.ID}, {self.name}, {self.title}, {self.department}"

    def __str__(self) -> str:
        return f"{self.ID} - {self.name}"

    def __json__(self):
        return {
            'ID': str(self.ID),
            'name': self.name,
            'title': self.title,
            'department': self.department
        }


class Department:
    def __init__(self, department_name, employees_list=[]):
        self.department_name = department_name
        self.employees_list = employees_list

    def add_employee(self, employee):
        self.employees_list.append(employee)

    def remove_employee(self, employee_name):
        updated_employees_list = filter(
            lambda emp: emp.name != employee_name, self.employees_list)
        self.employees_list = list(updated_employees_list)
        print('Removed employee:', employee_name)

    def list_all_employees(self):
        for employee in self.employees_list:
            print(employee)

    def __json__(self):
        return {
            'department_name': self.department_name,
            'employees_list': [emp.__json__() for emp in self.employees_list]
        }


class DataEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Department):
            return o.__json__()
        elif isinstance(o, Employee):
            return o.__json__()
        else:
            return super().default(o)


def object_decoder(obj):
    decoded_obj = {}
    for key in obj:
        department_name = obj[key]['department_name']
        employees_list = obj[key]['employees_list']
        emp_object_list = []
        for emp in employees_list:
            emp_object_list.append(Employee(
                name=emp['name'],
                title=emp['title'],
                department=emp['department'],
                ID=emp['ID']
            ))
        department = Department(
            department_name=department_name, employees_list=emp_object_list)
        decoded_obj[key] = department
    return decoded_obj


def read_json_data():
    company_data = {}
    with open('saved_data.json', 'r') as file:
        jsondata = file.read()
        if jsondata.strip() != "":
            company_data = object_decoder(json.loads(jsondata))
    return company_data


def save_json_data(company):
    with open('saved_data.json', 'w') as file:
        file.write(json.dumps(company, cls=DataEncoder, indent=4))
    print('Saved data')


# Company data
company = read_json_data()


def app_department_to_company(department):
    company[department.department_name] = department
    print('Added department to company')


def remove_department_from_company(department):
    if department.department_name in company:
        del company[department.department_name]
    print('Removed department from company')


def display_all_departments():
    for key, department in company.items():
        print(department.department_name)


def add_new_employee_handler():
    if len(company.keys()) == 0:
        raise Exception(
            'No department available in the company. Add a department first')

    employee_name = input('Enter employee name: ')
    employee_title = input('Enter employee title: ')

    if not employee_name or not employee_title:
        raise Exception('Invalid detail entered')

    print('Select department')
    display_all_departments()
    department_name = input('Enter department name: ')

    if department_name not in company.keys():
        raise Exception('Invalid department entered')

    employee = Employee(employee_name, employee_title, department_name)
    company[department_name].add_employee(employee)
    save_json_data(company)


def remove_employee_handler():
    print('Select department')
    display_all_departments()
    department_name = input('Enter department name: ')
    if department_name not in company.keys():
        raise Exception('Department doesn\'t exists')

    department = company[department_name]
    department.list_all_employees()
    employee_name = input('Enter employee name: ')
    department.remove_employee(employee_name)
    save_json_data(company)


def display_department():
    display_all_departments()


def add_new_department_handler():
    department_name = input('Enter department name: ')
    if department_name in company.keys():
        raise Exception('Department already exists')

    department = Department(department_name)
    app_department_to_company(department)
    save_json_data(company)


def add_employee_to_department_handler():
    add_new_employee_handler()


def remove_employee_from_department():
    remove_employee_handler()


def display_department_details():
    print('Select department')
    display_all_departments()
    department_name = input('Enter department name: ')
    department = company.get(department_name)
    if department is None:
        raise Exception('Department doesn\'t exists')

    print('Department name:', department.department_name)
    print('Employees:')
    department.list_all_employees()


def main():
    while True:
        print("=" * 100)
        print("Menu:")
        print("1. Add Employee")
        print("2. Remove Employee")
        print("3. Display Department")
        print("4. Add a new Department")
        print("5. Add employee to department")
        print("6. Remove employee from department")
        print("7. View department details")
        print("8. Exit")

        option = input('Enter option (1-8): ')

        print("=" * 100)

        try:
            if option == "1":
                add_new_employee_handler()
            elif option == "2":
                remove_employee_handler()
            elif option == "3":
                display_department()
            elif option == "4":
                add_new_department_handler()
            elif option == "5":
                add_employee_to_department_handler()
            elif option == "6":
                remove_employee_from_department()
            elif option == "7":
                display_department_details()
            elif option == "8":
                print('Exiting app...')
                break
            else:
                print('INVALID INPUT')
        except Exception as e:
            print('Error', str(e))


if __name__ == '__main__':
    main()
