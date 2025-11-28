#Program for a simple to-do app

class Task:

    def __init__(self,name):
        self.name = name
        self.status = False #Status set to False initially as no task completed

    def completed(self): #-->to check if the task is completed as status becomes true after completion
        self.status = True

    def __str__(self): #to display the task name
        self.name

class Todo:

    def __init__(self):
        self.tasks = []
    def add_task(self,name):
        t1 = Task(name)
        self.tasks.append(t1)
        print(f'Task added {name}')

    def showtasks(self):
        if not self.tasks:
            print('No tasks')
            return
        t = 1
        for i in self.tasks:
            print(f'Task -{i.name}- {t}')
            t += 1
    
    def change_status(self,n):
        if n > 0 or n >= len(self.tasks):
            print('Invalid')
            return
        self.tasks[n].completed()
        print(f'{self.task[n].name} with status {self.task[n].status}')

def main():
    todo1 = Todo()
    while True:
        print('1.Add Task\n2.View Task\n3.Update Task\n4.Exit')
        ch = int(input('Enter your choice:'))
        if ch == 1:
            name = input('Enter your task name:')
            todo1.add_task(name)
        elif ch == 2:
            todo1.showtasks()
        elif ch == 3:
            todo1.showtasks()
            num = int(input('Enter your task number')) - 1
            todo1.change_status(num)
        elif ch == 4:
            break
        else:
            print('Invalid choice')

main()