

def lemonadechange(bills):
    five = 0
    ten = 0

    for i in bills:
        if i == 5:
            five += 1
            print('No change needed')
        elif i == 10:
            if five > 0:
                five -= 1
                ten += 1
                print('Gave $5 as change')
            else:
                print('Not enough $5 to give change')
                return False
        else:
            if ten > 0 and five > 0:
                ten -= 1
                five -= 1
                print('Gave one $10 and one $5 for $15 change')
            elif five >= 3:
                five -= 3
                print('Gave three $5 for the $15 change')
            else:
                print('Not enough money to give change')
                return False
            
    return True
#print(lemonadechange([5,5,5,10,20]))
print(lemonadechange([5,5,10,10,20]))
