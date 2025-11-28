import random

words = ['python', 'django', 'java', 'machine', 'learning']
word = random.choice(words)
guess_word = ''
chance = 10

while chance > 0:
    c = 0
    for i in word:
        if i in guess_word:
            print(i, end=' ')
        else:
            print('_', end=' ')
        
        c += 1
    print()
    if c == 0:
        print('You Win')
        break

    guess = input('Enter your alphabet:')
    guess_word = guess_word + guess
    print(guess_word)

    if guess_word not in word:
        chance = chance - 1
        print(f'Remaning chance is {chance}')

        if chance == 0:
            print('You lost')