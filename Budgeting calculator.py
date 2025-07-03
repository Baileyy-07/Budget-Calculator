'''Budgeting Calculator'''

__Author__ = ' Bailey Iles '
__Version__ = ' 0.0.0 '
__Date__ = ' 8/4/25 '

#use textual for a TUI interface

import BudCalMod
import MainBudCalMod

main = BudCalMod.Menu("main", ["Expenses", "Incomes", "Balance", "Report"])

while True:
    BudCalMod.Menu.display(main)
    choice = MainBudCalMod.CEDN(5, zoom = True)
    if choice == "exit":
        break
    elif choice == 1:
        pass
    elif choice == 2:
        MainBudCalMod.incomes_display()
    elif choice == 3:
        pass
    elif choice == 4:
        pass
    else:
        print("Invalid input, try again.")