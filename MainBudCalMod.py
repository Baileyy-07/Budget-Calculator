import BudCalMod

"""this module outlines the user functionality of the program"""

all_commands = {"income":{"create":BudCalMod.Income.add_income, "edit":BudCalMod.Income.edit_income, "delete":BudCalMod.Income.delete_income},
                "expense":{"category":{"create":[], "edit":[], "delete":[]},
                    "create":[], "edit":[], "delete":[]},
                "balance":{"create":[], "edit":[], "delete":[]},
                "report":{"create":[], "edit":[], "delete":[]}}

def CEDN(number = None, C = None, E = None, D = None, zoom = None):
    """used to initiate the create, edit or delete object options when menu is displayed"""
    options = [number if number else None, "C" if C else None, "E" if E else None, "D" if D else None, "zoom" if zoom else None]
    while True:
        displays = ["Number = '#'.","Create = 'C'", "Edit = 'E'", "Delete = 'D'"]
        commands = {"C" : "create", "E" : "edit", "D" : "delete"}
        chosen_displays = " | "

        for i, option in enumerate(options):
            if option:
                try:
                    chosen_displays += displays[i]
                    chosen_displays += " | "
                except IndexError:
                    continue

        print(chosen_displays, sep= " | ")
        choice = input("Enter option: ")
        try:
            choice = choice.capitalize()
        except:
            continue
        if choice == str(number):
            return "exit"
        elif choice == "C":
            if options[1] == "C":
                return commands[choice]
            else:
                print("Invalid input, try again.")
                continue
        elif choice == "E":
            if options[2] == "E":
                return commands[choice]
            else:
                print("Invalid input, try again.")
                continue
        elif choice == "D":
            if options[3] == "D":
                return commands[choice]
            else:
                print("Invalid input, try again.")
                continue

        else:
            if options[4] != None:
                try:
                    choice = int(choice)
                    if choice in range(number):
                        return choice
                    else:
                        print("Invalid input, try again. not indexed")
                except:
                    print("Invalid input, try again. not integer")
            else:
                print("Invalid input, try again. no zoom")

def incomes_display():
    """the whole code for using the income code from BudCalMod"""
    BudCalMod.Income.get_incomes()
    income_list = BudCalMod.Income.income_list     
    while True:
        print("\nIncomes")
        if not income_list:
            print("\nNo Incomes Detected.")
            print("1. Exit")
            choice1 = CEDN(number=0, C=True)
            if choice1 in all_commands["income"]:
                make_new = all_commands["income"][choice1]
                make_new()
            elif choice1 == 1:
                break

        else:
            num = len(income_list)
            for i, inc in enumerate(income_list, 1):
                print(f"{i}. {inc}")
            print(f"{len(income_list) + 1}. Exit")
            choice2 = CEDN(number = num + 1, C = True)
            if choice2 in num:
                income = income_list[choice2 - 1]
                print("\nSelected Income Details:")
                print(f"Name = {income.name}")
                print(f"Average Earnings (per pay period): ${income.average_pay}")
                print(f"Pay Period: {income.pay_period[0]}")
                print(f"Payslips On File:")
                for payslip in income.payslips:
                    print(f"{payslip.date} - {payslip.pay}")
                print("1. Back")
                choice3 = CEDN(number = 1, E = True, D = True)
                if choice3 == 1:
                    continue
                else:
                    command = all_commands["income"][choice3]
                    command(choice2 - 1)
            elif choice2 == num + 1:
                break
            else:
                create = all_commands["income"][choice2]
                create()