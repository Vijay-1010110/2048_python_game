import os
import sys
import keyboard
import random
import copy
import pickle


#clear_console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

cols = 4
rows = 4
grid = [[0 for _ in range(cols)] for _ in range(rows)]
row_len = len(grid)
col_len = len(grid)
score = 0
high_score = 0
prev_state = []
prev_score = 0


grid_overFlow = False

def find_random_empty_place():
    global grid_overFlow
    #find the places where value == 0
    empty_places = [(i,j) for i in range(rows) for j in range(cols) if grid[i][j] == 0]
    #get the one random occurance of zero(empty place)
    if empty_places:
        grid_overFlow = False
        #returns a random  empty place
        return random.choice(empty_places)
    else :
        grid_overFlow = True
        return None

#generate value 2 or 4 ratio 9:1
def set_value():
    # Define the choices and their probabilities
    choices = [2, 4]
    probabilities = [0.9, 0.1]
    # Generate a random number with the specified probabilities
    value =  random.choices(choices, probabilities)[0]
    empty_place = find_random_empty_place()
    if empty_place is not None:
        i, j = empty_place
        value = random.choices(choices, probabilities)[0]
        grid[i][j] = value




#display grid 
def display_grid():
    for i,row in enumerate(grid):

        for k in enumerate(grid):
            print('+---------',end='')
        print('+')

        for k in enumerate(grid):
            print('*         ',end='')
        print('*')

        #dispay value
        

        for j,value in enumerate(row):
            print('*',str(value).center(8) if value != 0 else ''.center(8),end='')
        print('*')

        for k in enumerate(grid):
            print('*         ',end='')
        print('*')

    for k in enumerate(grid):
        print('+---------',end='')
    print('+')



#shift funtions
#left shift
def left_shift():
    global score,grid,prev_state,prev_score
    prev_state = copy.deepcopy(grid)
    prev_score = score
    for i in range(row_len):
        k = 0
        for j in range(1,col_len):
            if grid[i][j] != 0:
                if grid[i][k] != 0:
                    if grid[i][k] == grid[i][j]:
                        grid[i][k] = grid[i][k] * 2
                        score += grid[i][j]
                        grid[i][j] = 0
                    k += 1
                grid[i][k] = grid[i][j]
                if k != j:
                    grid[i][j] = 0
            

#right shift
def right_shift():
    global score,grid,prev_state,prev_score
    prev_state = copy.deepcopy(grid)
    prev_score = score
    for i in range(row_len):
        k = row_len - 1
        for j in range(col_len - 2,-1,-1):
            if grid[i][j] != 0:
                if grid[i][k] != 0:
                    if grid[i][k] == grid[i][j]:
                        grid[i][k] = grid[i][k] * 2
                        score += grid[i][k]
                        grid[i][j] = 0
                    k -= 1
                grid[i][k] = grid[i][j]
                if k != j:
                    grid[i][j] = 0       

#up shift
def up_shift():
    global score,grid,prev_state,prev_score
    prev_state = copy.deepcopy(grid)
    prev_score = score
    for i in range(row_len):
        k = 0
        for j in range(1,col_len):
            if grid[j][i] != 0:
                if grid[k][i] != 0:
                    if grid[k][i] == grid[j][i]:
                        grid[k][i] = grid[k][i] * 2
                        score +=  grid[k][i]
                        grid[j][i] = 0
                    k += 1
                grid[k][i] = grid[j][i]
                if k != j:
                    grid[j][i] = 0


#down shift
def down_shift():
    global score,grid,prev_state,prev_score
    prev_state = copy.deepcopy(grid)
    prev_score = score
    for i in range(row_len):
        k = col_len - 1
        for j in range(col_len - 2,-1,-1):
            if grid[j][i] != 0:
                if grid[k][i] != 0:
                    if grid[k][i] == grid[j][i]:
                        grid[k][i] = grid[k][i] * 2
                        score +=  grid[k][i] 
                        grid[j][i] = 0
                    k -= 1
                grid[k][i] = grid[j][i]
                if k != j:
                    grid[j][i] = 0



def get_high_score():
    # You can implement your logic to retrieve the high score (from a file or elsewhere)
    # For simplicity, let's assume the high score is stored in another file
    try:
        with open('2048_game_high_score.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return 0

def save_high_score(high_score):
    # Save the high score to a file
    with open('2048_game_high_score.pkl', 'wb') as file:
        pickle.dump(high_score, file)


def save_game_state():
    # Save current state to a file
    with open('2048_game_state.pkl', 'wb') as file:
        game_state = {
            'grid': grid,
            'score': score,
            'high_score': get_high_score()  # You need to implement get_high_score()
        }
        pickle.dump(game_state, file)

def load_game_state():
    # Load saved state from a file
    try:
        with open('2048_game_state.pkl', 'rb') as file:
            game_state = pickle.load(file)
            return game_state['grid'], game_state['score']
    except FileNotFoundError:
        # Handle the case where the file is not found (first run or no saved state)
        return [[0 for _ in range(cols)] for _ in range(rows)], 0
    finally:
        if game_over:
            return [[0 for _ in range(cols)] for _ in range(rows)], 0
    


def wait_for_key():
    valid_keys = {'a', 's', 'w', 'd', 'q' , 'backspace','r'}

    # Clear the keyboard buffer
    keyboard.read_event(suppress=True)


    while True:
        key = keyboard.read_event(suppress=True).name
        if key in valid_keys:
            return key

# Example usage
wait_for_key()

def game_over():
    game_over = False
    h1,h2,v1,v2 = 0,0,0,0
    hc,vc = 0,0
    if grid_overFlow :
        for i in range(row_len):
            for j in range(col_len):
                h1 = grid[i][j]
                if h1 == h2:
                    return False
                h2 = h1

                v1 = grid[j][i]
                if v1 == v2:
                    return False
                v2 = v1
        else:
            return True
            


def game_run():
    global grid,score,high_score
    high_score = get_high_score()
    grid,score = load_game_state()
    set_value()
    set_value()
    clear_console()
    key_pressed = False
    while True:   
            
            display_grid()
            if score >= high_score:
                high_score = score #update high score
            print('score : ',str(score).ljust(7),end=' | ')
            print('High Score : ',str(high_score).ljust(7))

            
                
            #save prev state

            key = wait_for_key()
            
            if key == 'a':
                left_shift()
            elif key == 's':
                down_shift()
            elif key == 'w':
                up_shift()
            elif key == 'd':
                right_shift()
            elif key == 'backspace':
                grid = copy.deepcopy(prev_state)
                clear_console()
                score = prev_score
                continue
            elif key == 'r':
                grid = [[0 for _ in range(cols)] for _ in range(rows)]
                score = 0
                clear_console()
                set_value()
                set_value()
                continue
            save_game_state()
            save_high_score(high_score)
            if key == 'q':
                sys.exit()

            set_value()
            if game_over():
                print('*****************| Game Over |********************')
                exit()
            key_pressed = True  
            clear_console()
      
        


game_run()
