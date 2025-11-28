#Expense Tracker Program

class Expense:
    def __init__(self,name,amount):
        self.name = name
        self.amount = amount
        
class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self,name,amount):
        exp = Expense(name,amount)
        self.expenses.append(exp)
        
    def view_expenses(self):
        if not self.expenses:
            print('No expenses found')
            return
        else:
            start = 1
            for i in self.expenses:
                print(f'Expense- {i.name},Amount- {i.amount} - {start}')
                start += 1
    
    def total_expenses(self):
        total = 0
        for i in self.expenses:
            total += i.amount
        print('Total Expense:', total)
        return total

def main():
    tracker = ExpenseTracker()

    while True:
        print(('Expense Tracker Menu:'))
        print('1.Add Expense')
        print('2.View Expense')
        print('3.Total Expense')
        print('4.Exit')

        choice = input("Enter your choice(1-5):")

        if choice == '1':
            name = input('Enter your expense:- ')
            amount = float(input('Enter the expense amount:- '))
            exp = Expense(name,amount)
            tracker.add_expense(name,amount)
            print('Expense added.')
        elif choice == '2':
            tracker.view_expenses()
        elif choice == '3':
            tracker.total_expenses()
        elif choice == '4':
            print('Exit')
            break
        else:
            print('Invalid choice!Try Again')
main()

    

