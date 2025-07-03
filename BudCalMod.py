'''re-doing the budget calculator module because it got messy'''
import json
import math
import os
import calendar
import re
import pdfplumber
import random
from datetime import datetime

class Income:
    income_file_path = f'{os.getcwd()}\\budgeting_income.json'
    income_list = []
    pay_periods = {
        'weekly':7,
        'bi-weekly':14,
        'monthly':calendar.monthrange(
            datetime.today().year,datetime.today().month)[1]
    }

    def __init__(self, name, average_pay, payslips, pay_period):
        self.name = name
        self.average_pay = average_pay
        self.payslips = payslips
        self.pay_period = pay_period

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            "name":self.name,
            "average_pay":self.average_pay,
            "payslips":self.payslips,
            "pay_period":self.pay_period
        }
    
    @staticmethod
    def from_dict(data):
        return Income(
            name = data["name"],
            average_pay = data["average_pay"],
            payslips = data["payslips"],
            pay_period  = data["pay_period"]
            )
    
    @classmethod
    def get_incomes(cls):
        if not os.path.exists(cls.income_file_path):
            cls.income_list = []
        else:
            with open(cls.income_file_path, 'r') as f:
                try:
                    raw_data = json.load(f)
                    cls.income_list = [cls.from_dict(inc) for inc in raw_data]
                except json.JSONDecodeError:
                    cls.income_list = []
        return cls.income_list
    
    @classmethod
    def save_incomes(cls):
        serializable = [inc.to_dict() for inc in cls.income_list]
        with open(cls.income_file_path, 'w') as f:
            json.dump(serializable, f, indent = 4)

    @staticmethod
    def get_inc_name():
        return input("Enter name of new income: ")

    @staticmethod
    def get_average_pay(payslips):
        p = []
        for payslip in payslips:
            p.append(payslip.pay)
        return sum(p) / len(p)

    @staticmethod
    def get_inc_payslips(income_name):
        if not Payslip.inc_payslip_files(income_name):
            return []
        else:
            files = Payslip.inc_payslip_files(income_name)
            payslips = []
            for i, pdf in enumerate(files):
                file = pdf
                pay = Payslip.get_pay(Payslip.get_payslip_text(pdf))
                date = Payslip.get_date(pdf)
                payslips.append(Payslip(file, pay, date))
            return payslips

    @staticmethod
    def get_pay_period():
        while True:
            per = input(
                "Enter period ('weekly', 'bi-weekly', 'monthly'): "
            ).strip().capitalize()
            periods = ['Weekly', 'Bi-weekly', 'Monthly']
            if per in periods:
                if per == 'Weekly':
                    return [per, 1]
                elif per == 'Bi-weekly':
                    return [per, 2]
                elif per == 'Monthly':
                    return [per, 4]
            else:
                print("Invalid period. Try again.")

    @classmethod
    def add_income(cls):
        cls.get_incomes()
        while True:
            name = cls.get_inc_name()
            payslips = cls.get_inc_payslips(name)
            average_pay = cls.get_average_pay(payslips)
            pay_period = cls.get_pay_period()
            new_income = Income(name, average_pay, payslips, pay_period)
            cls.income_list.append(new_income)
            cls.save_incomes()
            break
        return cls.income_list
    
    @classmethod
    def delete_income(cls, income_num):
        cls.get_incomes()
        try:
            del cls.income_list[income_num]
            cls.save_incomes()
            return cls.income_list
        except ValueError:
            print("Invalid input. Try again.")
    
    @classmethod
    def edit_income(cls, income_num):
        cls.get_incomes()
        income = cls.income_list[income_num]
        while True:
            print("Select income attribute.")
            print(f"1. Name = {income.name}")
            print(f"2. Average Earnings = ${income.average_pay}")
            print(f"3. Pay Period = {income.pay_period[0]}")
            print("4. Back")
            while True:
                try:
                    att_to_edit = int(input("Select a number between 1 and 4: "))
                    if 1 <= att_to_edit <= 4:
                        break
                except ValueError:
                    print("Invalid input. Enter a number.")
            if att_to_edit == 1:
                income.name = cls.get_inc_name()
                cls.save_incomes()
            elif att_to_edit == 2:
                income.average_pay = cls.get_average_pay()
                cls.save_incomes()
            elif att_to_edit == 3:
                income.pay_period = cls.get_pay_period()
                cls.save_incomes()
            elif att_to_edit == 4:
                break
        return cls.income_list

class Expense:
    #add failsafes just in case there are no expense categories
    #(failsafes should not stop the code or create new cat
    # they should just output data in different format)
    expense_file_path = f'{os.getcwd()}\\budgeting expenses.json'
    expense_list = []
    expense_dict = {}

    def __init__(self, name, cost, time):
        self.name = name
        self.cost = cost
        self.time = dict(time)

    def __str__(self):
        return f"{self.name} > ${self.cost} > {self.time[0], {self.time[1]}}"
    
    def to_dict(self):
        return{
            "name":self.name,
            "cost":self.cost,
            "time":self.time
        }
    
    @staticmethod
    def from_dict(data):
        return Expense(
            name = data["name"],
            cost = data["cost"],
            time = data["time"]
        )
    
    @classmethod
    def get_expenses(cls):
        if not os.path.exists(cls.expense_file_path):
            cls.expense_list = {}
        else:
            with open(cls.expense_file_path, 'r') as f:
                try:
                    raw_data = json.load(f)
                    Category.get_categories()
                    data_names = Category.category_list[:]
                    data_list = [[cls.from_dict(e) for e in cat] for cat in raw_data[1]]
                    if len(data_names) and len(data_list) == len(raw_data[1]):
                        for i, cat in enumerate[data_names]:
                            cls.expense_dict.update({cat:data_list[i]})
                    else:
                        print("Unable to load expense dictionary.")
                        print("incorrect length detected.")
                    cls.expense_list = [cls.from_dict(exp) for exp in raw_data[2]]
                except json.JSONDecodeError:
                    cls.expense_dict = {}
                    cls.expense_list = []
        return
    
    @classmethod
    def save_expenses(cls):
        s1 = Category.category_list
        s2 = {}
        for i, cat in enumerate(Category.category_list):
            s2.update({f"{cat}":[exp.to_dict() for exp in exp_cat] for exp_cat in cls.expense_list[i]})
        if not cls.expense_list:
            s3 = []
        else:
            s3 = [e.to_dict() for e in cls.expense_list]
        serializable = [s1, s2, s3]
        with open(cls.expense_file_path, 'w') as f:
            json.dump(serializable, f, indent = 4)
        return
    
    @staticmethod
    def expense_name():
        return input("Enter the name of the new expense: ")

    @staticmethod
    def get_cost():
        while True:
            print("What is the cost of the new expense?")
            try:
                return float(input("Enter cost as float: "))
            except ValueError:
                print("Invalid input, try again.")

    @staticmethod
    def get_time_period():
        d_i_m = calendar.monthrange(
            datetime.today().year,datetime.today().month)[1]
        while True:
            print("How often do you pay this expense?")
            try:
                oft = float(input("Enter amount of (peroids) as float: "))
                break
            except ValueError:
                print("Invalid input, try again.")
        while True:
            per = input("Enter period 'Days' as 'D', 'Weeks' as 'W', 'Months' as 'M': ")
            per = per.capitalize()
            if per == "D":
                period = "days"
                break
            elif per == "W":
                period = "weeks"
                break
            elif per == "M":
                period = "months"
                break
            else:
                print("Invalid input, try again.")
        days = {'D':1, 'W':7, 'M':d_i_m}[per]
        p_days = math.ceil(oft * days)
        return {p_days:[period, oft]}

    @classmethod
    def view_all_expenses(cls):
        cls.get_expenses()
        for cat in cls.expense_dict:
            print(cat)
            for i, exp in enumerate(cat):
                print(f"{i}. {exp}")
            print()
        print("Uncategorised.")
        for i, e in enumerate(cls.expense_list):
            print(f"{i}. {e}")

    @classmethod
    def view_expenses(cls, cat):
        num = 0
        cls.get_expenses()
        if cat == cls.expense_list:
            print("Uncategorsed Expenses:")
            for i, exp in enumerate(cls.expense_list):
                print(f"{i}. {exp}")
                num += i
            print(f"{i + 1}. Back")
        else:
            print(f"{cls.expense_dict[cat]}")
            for l, e in enumerate(cls.expense_dict[cls.expense_dict[cat]]):
                print(f"{l}. {e}")
                num += l
            print(f"{l + 1}. Back")
        return num

    @classmethod
    def add_expense(cls):
        cls.get_expenses()
        while True:
            print("Create new expense.")
            new_exp = Expense(Expense.expense_name(), Expense.get_cost(), Expense.get_time_period())
            if not Category.category_list:
                print("No categories found, random category created.")
                Category.insert_categories()
            else:
                print("Where does this expense belong?")
                for i, cat in enumerate(Category.category_list):
                    print(f"{i}. {cat}")
                print(f"{len(Category.category_list) + 1}. No Category")
                print(f"{len(Category.category_list) + 2}. Back")
                try:
                    selection = int(input("Enter corresponding category number: "))
                    if selection == len(Category.category_list) + 1:
                        cls.expense_list.append(new_exp)
                    elif selection == len(Category.category_list) + 2:
                        break
                    elif selection not in range(0, len(Category.category_list)):
                        print("Invalid option, try again.")
                    else:
                        return cls.expense_dict[cls.expense_dict[selection]].append(new_exp)
                except ValueError:
                    print("Invalid input, try again.")


    @classmethod
    def delete_expense(cls):
        cls.get_expenses()
        while True:
            print("\nSelect a category to delete from:")
            for i, cat in enumerate(Category.category_list):
                print(f"{i}. {cat}")
            print(f"{len(Category.category_list) + 1}. Uncategorised")
            print(f"{len(Category.category_list) + 2}. Back")

            try:
                c = int(input("Enter number beside chosen category: "))
                if c == len(Category.category_list) + 2:
                    break
                elif not Category.category_list[c]:
                    print("Invalid input, try again")
                elif c == len(Category.category_list) + 1:
                    while True:
                        print("\nSelect an expense to delete.")
                        for j, ex in enumerate(cls.expense_list):
                            print(f"{j}. {ex}")
                        print(f"{len(cls.expense_list) + 1}. Back")
                        try:
                            choice = int(input("Enter number beside chosen expense: "))
                            if choice == len(cls.expense_list) + 1:
                                break
                            elif not cls.expense_list[choice]:
                                print("Invalid input, try again.")
                            else:
                                del cls.expense_list[choice]
                                return
                        except:
                            print("Invalid input, try again.")
                else:
                    while True:
                        cat_choice = Category.category_list[c]
                        print("\nSelect an expense to delete.")
                        for l, exp in enumerate(cls.expense_dict[cat_choice]):
                            print(f"{l}. {exp}")
                        print(f"{len(cls.expense_dict[cat_choice]) + 1}. Back")

                        try:
                            e = int(input("Enter number beside chosen expense: "))
                            if e == len(cls.expense_dict[cat_choice]) + 1:
                                break
                            elif not cls.expense_dict[cat_choice][e]:
                                print("Invalid input, try again")
                            else:
                                del cls.expense_dict[cat_choice][e]
                                return
                            
                        except ValueError:
                            print("Invalid input, try again.")
           
            except ValueError:
                print("Invalid input, try again.")

    @classmethod
    def edit_expenses(cls):
        cls.get_expenses()
        while True:
            print("\nSelect a category to edit expense from:")
            for i, cat in enumerate(Category.category_list):
                print(f"{i}. {cat}")
            print(f"{len(Category.category_list) + 1}. Uncategorised")
            print(f"{len(Category.category_list) + 2}. Back")

            try:
                c = int(input("Enter number beside chosen category: "))
                if c == len(Category.category_list) + 1:
                    break
                elif not Category.category_list[c]:
                    print("Invalid input, try again")
                else:
                    chosen_cat = Category.category_list[c]

                    while True:
                        print("\nSelect an expense to delete.")
                        for l, exp in enumerate(cls.expense_dict[chosen_cat]):
                            print(f"{l}. {exp}")
                        print(f"{len(cls.expense_list[chosen_cat]) + 1}. Back")

                        try:
                            e = int(input("Enter number beside chosen expense: "))
                            if e == len(cls.expense_list[chosen_cat]) + 1:
                                break
                            elif not cls.expense_list[chosen_cat][e]:
                                print("Invalid input, try again")
                            else:

                                chosen_exp = cls.expense_list[chosen_cat][e]
                                print("Choose which part of this expense you wish to edit: ")
                                print(f"""
====================
1. Name = {chosen_exp.name}
2. Cost = {chosen_cat.cost}
3. Time = {chosen_exp.time}
4. Back
====================
                                      """)
                                try:
                                    choice = int(input("Enter choice to edit: "))
                                    if choice == 4:
                                        break
                                    elif choice == 1:
                                        name = cls.expense_name()
                                        print(f"{chosen_exp.name} is now {name}")
                                        chosen_exp.name = name
                                    elif choice == 2:
                                        cost = cls.get_cost()
                                        print(f"{chosen_exp.cost} is now {cost}")
                                        chosen_exp.cost = cost
                                    elif choice == 3:
                                        time = cls.get_time_period()
                                        print(f"{chosen_exp.time} is now {time}")
                                        chosen_exp.time = time
                                    else:
                                        print("Invalid input, try again.")
                                except ValueError:
                                    print("Invalid input, try again.")

                        except ValueError:
                            print("Invalid input, try again.")

            except ValueError:
                print("Invalid input, try again.")

class Category:
    category_list = []

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @classmethod
    def get_categories(cls):
        with open(Expense.expense_file_path, 'r') as f:
            try:
                raw_data = json.load(f)
                if raw_data[0]:
                    cls.category_list = raw_data[0]
                else:
                    cls.category_list = []
            except json.JSONDecodeError:
                cls.category_list = []
        return cls.category_list
        
    @classmethod
    def insert_cat_list(cls):
        pass

    @classmethod
    def insert_categories(cls, decoded_data, num = 7):
        data = []
        keys = []
        new_expense_list = {}
        if not decoded_data:
            new_key = cls.rand_str(num)
            new_expense_list.update({new_key:[]})
        else:
            for i, cat in enumerate(decoded_data):
                try:
                    data.append(decoded_data.get(cat))
                except ValueError:
                    data.append([])
                try:
                    keys.append(decoded_data[i])
                except KeyError:
                    keys.append(cls.rand_str(num))
            new_expense_list.update({'categories' : keys})
            if len(keys) == len(data):
                for l in range(len(decoded_data)):
                    new_expense_list.update({keys [l] : data[l]})
                    print("categorie inserted", f"{keys[l]}")
                return new_expense_list
            else:
                print("something went wrong, insert_categories")
                return decoded_data

    @staticmethod
    def rand_str(str_len):
        chars_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890`~!@#$%^&*()-_=+|[{}]'\";:?.>,<"
        characters = []
        for c in chars_str:
            characters.append(c)
        new_str = ""
        for _ in range(str_len):
            new_str += characters[random.randrange(len(characters))]
        return new_str
    
    @classmethod
    def view_categories(cls):
        cls.get_categories()
        num = 0
        for i, cat in enumerate(cls.category_list):
            print(f"{i}. {cat}")
            num += i
        num = num + 1
        print(f"{num}. View All Expenses")
        print(f"{num + 1}. Back")
        return num
    
    @classmethod
    def add_category(cls):
        cls.get_categories
        while True:
            print("What is the name of the new category?")
            new = input("Enter new category here: ")
            new = str(new)
            if new not in cls.category_list:
                cls.category_list.append(new)
                Expense.expense_list.update({new:[]})
                print("new category succsesfully created.")
                break
            elif new in cls.category_list:
                print("category already exists, try again.")
            else:
                print("Error")
        return
    
    @classmethod
    def edit_category(cls):
        cls.get_categories()
        Expense.get_expenses()
        while True:
            print("Which category would you like to edit?")
            if len(cls.category_list) <= 0:
                print("No categories found.")
                break
            else:
                cls.view_categories()
                print(f"{len(cls.category_list) + 1}. Back")
                try:
                    cat = int(input("Enter number next to category: "))
                    if cat == len(cls.category_list) + 1:
                        break
                    else:
                        print("Would you like a random name generated?")
                        yn = input("Y/N: ")
                        yn = yn.capitalize()
                        if yn == "Y":
                            new = cls.rand_str(7)
                        elif yn == "N":
                            new = input("Enter this categories new name: ")
                        new = str(new)
                        print(f"{cls.category_list[cat - 1]} is now {new}")
                        data = Expense.expense_list[cls.category_list[cat - 1]]
                        old = cls.category_list[cat - 1]
                        cls.category_list[cat - 1] = new
                        del Expense.expense_list[old]
                        Expense.expense_list.update({new:data})
                        del cls.category_list[cat]
                        cls.category_list.append(new)
                        break
                except ValueError:
                    print("invalid input, try again.")

    @classmethod
    def delete_category(cls):
        cls.get_categories()
        Expense.get_expenses()
        while True:
            print("Select category to delete.")
            cls.view_categories()
            print(f"{len(cls.category_list) + 1}. Back")
            try:
                choice = int(input("Enter number beside category: "))
                for exp in Expense.expense_list[cls.category_list[choice - 1]]:
                    print(exp)
                print("would you like to save expenses within category?")
                print("If you choose not to all data will be lost.")
                yn = input("Y/N? : ")
                yn = yn.capitalize()
                if yn == "Y":
                    cat_name = cls.category_list[choice - 1]
                    cat_data = Expense.expense_list[cat_name]
                    del Expense.expense_list[cat_name]
                    del Category.category_list[choice - 1]
                    new = cls.rand_str(7)
                    Expense.expense_list.update({new:cat_data})
                    cls.category_list.append(new)
                    print("Data saved succsessfully.")
                    break
                elif yn == "N":
                    del Expense.expense_list[cls.category_list[choice - 1]]
                    del cls.category_list[choice - 1]
                    print("data deleted succsessfully.")
                    break
                else:
                    print("Invalid input, try again.")

            except ValueError:
                print("Invalid input, try again.")
        #eventually make it so the user can select certain ones to get rid of then add the others to randomly named category.
        pass

class Payslip:
    log = {}
    log_file = f'{os.getcwd()}\\payslip_log_file.json'
    directories = []

    def __init__(self, file, date, pay):
        self.file = file
        self.date = date
        self.pay = pay

    def __str__(self):
        return f"{self.date} = {self.pay}"
    
    def to_dict(self):
        return {
            "file":self.file,
            "date":self.date,
            "pay":self.pay
        }
    
    @staticmethod
    def from_dict(data):
        return Payslip(
            file = data["file"],
            date = data["date"],
            pay = data["pay"]
        )
    
    @classmethod
    def get_log(cls):
        log_data = {}
        if os.path.exists(cls.log_file):
            try:
                with open(cls.log_file, 'r') as f:
                    raw_data = json.load(f)
                    for name, payslips in raw_data.items():
                        log_data[name] = [cls.from_dict(p) for p in payslips]
            except json.JSONDecodeError:
                for inc in Income.get_incomes():
                    log_data.update({inc.name:[]})
                cls.log = log_data
        else:
            with open(cls.log_file, 'w') as f:
                for inc in Income.get_incomes():
                    log_data.update({inc.name:[]})
                    cls.log = log_data

        return log_data
    
    @classmethod
    def update_log(cls, new_files):
        os.chdir(cls.directories[1])
        serializable = {}
        for name, payslip_objs in new_files.items():
            serializable[f'{name}'] = [obj.to_dict() for obj in payslip_objs]
        with open(cls.log_file, 'w') as f:
            json.dump(serializable, f, indent = 4)
        os.chdir(cls.directories[0])
        return
    
    @staticmethod
    def get_pay(pdf_text):
        x = re.compile(r"Net Pay(?:ment:)?\s*.{1}(.*)")
        pay = re.search(x, pdf_text)
        return float(pay.group(1))
    
    @staticmethod
    def get_date(pdf_file):
        timestamp = os.path.getmtime(pdf_file)
        date_paid = datetime.fromtimestamp(timestamp).strftime("%d/%m%Y")
        return date_paid
    
    @classmethod
    def inc_payslip_files(cls, inc_name):
        cls.get_dir_paths()
        folder = f"{cls.directories[1]}\\{inc_name}"
        if not os.path.exists(folder):
            os.mkdir(folder)
            current_files = []
        else:
            try:
                current_files = [
                    os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".pdf")]
            except:
                current_files = []
        return current_files
    
    @staticmethod
    def get_payslip_text(pdf):
        with pdfplumber.open(pdf) as f:
            all_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text
        return all_text
    
    @classmethod
    def get_dir_paths(cls):
        try:
            main_directory = f"{os.getcwd()}"
            sub_directory = f"{main_directory}\\payslips"
        except:
            main_directory = f"{os.getcwd()}"
            sub_directory = os.mkdir(f"{main_directory}\\payslips")
        cls.directories = [main_directory, sub_directory]
        return
    
    @classmethod
    def test_files(old_files, new_files):
        files = []
        for i, new_file in enumerate(new_files):
            if new_file not in old_files:
                pay = Payslip.get_pay(new_file)
                date = Payslip.get_date(new_file)
                file_info = Payslip(new_file, date, pay)
                files.append(file_info)
            else:
                files.append(Payslip(old_files[i]))
        return files

    @staticmethod
    def delete_old_files(folder_files):
        new_list = []
        for payslip in folder_files:
            date_obj = datetime.strptime(payslip.date, "%d/%m/%Y").date()
            today = datetime.today().date()
            months_diff = (today.year - date_obj.year) * 12 + today.month - date_obj.month
            if months_diff >= 2 and date_obj.date >= today.day:
                os.remove(payslip.file)
                if payslip.file in folder_files:
                    folder_files.remove(payslip.file)
            else:
                new_list.append(payslip)
        return new_list

class Menu:
    menu_list = []
        
    def __init__(self, title, options):
        self.title = title
        self.options = list(options)
        self.menu_list.append(title)

    def __str__(self):
        return self.title
    
    def display(self):
        print(self.title)
        print("=========================")
        for i, option in enumerate(self.options):
            print(f"{i + 1}. {option}")
        print(f"{len(self.options) + 1}. Exit")
        print("=========================")
    
    def choice(self):
        print(f"Select a number between 1 and {len(self.options + 1)}")
        while True:
            try:
                selection = int(input("Enter your selection: "))
                return selection
            except:
                print("Invalid option, please try again")

class Report:
    budget_file_path = f'{os.getcwd()}\\budget reports.json'
    budget = {}
    report_types = ['average_budget', 'income_based_budget']

    def __init__(self, expenses, incomes, totals):
        self.expenses = expenses
        self.incomes = incomes
        self.totals = totals

class ReportTable:    #unfinished

    def __init__(self):
        pass
        
class User:    #unfinished

    def __init__(self):
        pass

class Account: #unfinished
    pass