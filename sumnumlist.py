#Input as string of numbers whose digits of each numbers are added up 
# to make it a single digit number list

num = input('Enter the numbers: ').split()
numbers_list = [ ]

for i in num:
    numbers_list.append(int(i))

while any(j >= 10 for j in numbers_list):
    new_list = []
    for j in numbers_list:
        sum = 0
        while j > 0:
            sum += j % 10
            j //= 10
        new_list.append(sum)
    numbers_list = new_list

print('Final list of numbers:', numbers_list)