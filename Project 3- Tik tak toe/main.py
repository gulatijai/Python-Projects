list_of_numbers= [1,2,3,4,5,6,7,8,9]

def board():
    print(f"{list_of_numbers[0]} | {list_of_numbers[1]} | {list_of_numbers[2]}" )
    print("------------------")
    print(f"{list_of_numbers[3]} | {list_of_numbers[4]} | {list_of_numbers[5]}")
    print("------------------")
    print(f"{list_of_numbers[6]} | {list_of_numbers[7]} | {list_of_numbers[8]}")

winning_list=[[0,1,2], [3,4,5], [6,7,8],
 [0,3,6], [1,4,7], [2,5,8],
 [0,4,8], [2,4,6]]

def check_winner(player):
    for comb in winning_list:
        if list_of_numbers[comb[0]]==list_of_numbers[comb[1]]==list_of_numbers[comb[2]]:
            print(f"Player {player} wins")
            return True
    return False

def check_draw():
    for num in list_of_numbers:
        if isinstance(num, int):
            return False
    print ('Its draw')
    return True

game= True
current_player= 'X'
while game:
    board()

    try:
        move_position= int(input("Enter your number between 1-9: "))
    except ValueError:
        print("Invalid input. Enter a number between 1-9")
        continue

    if move_position<1 or move_position>9:
        print("invalid number")
        continue
    if not isinstance(list_of_numbers[move_position-1], int):
        print("Number already taken,enter new number")
        continue

    list_of_numbers[move_position-1]= current_player

    if check_winner(current_player):
        board()
        game= False
    elif check_draw():
        board()
        game=False

    if current_player=='X':
        current_player='O'
    else:
        current_player='X'




