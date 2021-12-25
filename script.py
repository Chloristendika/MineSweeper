'''MineSweeperDemo'''
'''Author: Chloris'''
'''LastData: 12-25'''

'''
Goal:
1. Test For All 
3. pygamelize
'''
import random


FirstClick = True

class Mine: # The unit

    def __init__(self, x_, y_, val = 0):
        self.x = x_
        self.y = y_
        self.value = val
        self.status = 'Unknown' # Status: Unknown (Not inited) / Mine / Num
        self.revealed = False   # Revealed: If the unit will be displayed on the scream by its true value
        self.marked = False     # Marked: (the Flag Mark)


    def around_count_mine(self):     # Around_count_mine: calculate the amount of the mines around the certain Mine
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                x_ = self.x + i; y_ = self.y + j
                if x_ <= 8 and x_ >= 0 and y_ <= 8 and y_ >= 0 and MineMap[x_][y_].status == 'Mine':
                    count += 1

        return count

    def arount_count_flag(self):
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                x_ = self.x + i; y_ = self.y + j
                if x_ <= 8 and x_ >= 0 and y_ <= 8 and y_ >= 0 and MineMap[x_][y_].marked == True:
                    count += 1
        return count

    def __repr__(self):
        return "ClassMine: ({}, {}, val = {})".format(self.x, self.y, self.value)

MineMap = [[Mine(i, j) for j in range(9)] for i in range(9)] # Initialize the MineMap
IsWalked = []

Remain_Mine_Num = 10


def Update():
    for i in range(9):
        for j in range(9):
            # print('*' if MineMap[i][j].revealed == False else MineMap[i][j].value, end = ' ')
            if MineMap[i][j].revealed == False:
                print('*', end = ' ')
            elif MineMap[i][j].marked == True:
                print('?', end = ' ')
            else:
                print(MineMap[i][j].value, end = ' ')
        print('\n')
    print("Remain: " + str(Remain_Mine_Num))

def Init(x, y): # The First click is (x, y) and generate the Mine randomly
    cnt = 0
    while cnt < 10: # Generate Ten Mines
        while True:  
            rand_x = random.randint(0, 8)
            rand_y = random.randint(0, 8)
            Unit = MineMap[rand_x][rand_y]
            if Unit.status == 'Unknown' and (rand_x, rand_y) != (x, y): # To ensure player's first click is not a Mine
                Unit.status = 'Mine'
                Unit.value = -1
                #print("The {} mine is on ({}, {})".format(cnt + 1, rand_x, rand_y))
                break
        cnt += 1


    # Calculating the Other Units:
    for row in range(9):
        for col in range(9):
            U = MineMap[row][col]
            if U.status == 'Mine':
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]: # The Eight Directions
                        if i == 0 and j == 0:
                            continue
                        x = row + i
                        y = col + j
                        if x <= 8 and x >= 0 and y <= 8 and y >= 0 and MineMap[x][y].status != 'Mine':
                            MineMap[x][y].status = 'Num'
                            MineMap[x][y].value += 1
            else:
                U.status = 'Num'
    for i in range(10):
        IsWalked.append([False] * 10)


    # Print to debug:
    '''
    for i in range(9):
        for j in range(9):
            print(MineMap[i][j].value if MineMap[i][j].status == 'Num' else '*', end = ' ')
        print('\n')
    '''
def Clear():
    for i in range(10):
        for j in range(10):
            IsWalked[i][j] = False


def Dfs(x, y):
    IsWalked[x][y] = True
    MineMap[x][y].revealed = True
    if MineMap[x][y].value > 0:
        return
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            x_ = x + i
            y_ = y + j
            if x_ == x and y_ == y:
                continue
            if IsWalked[x_][y_] == True:
                continue
            if x_ <= 8 and x_ >= 0 and y_ <= 8 and y_ >= 0 and MineMap[x_][y_].status != 'Mine':
                Dfs(x_, y_)
    return

def OutPutOrigion():
    for i in range(9):
        for j in range(9):
            print('$' if MineMap[i][j].status == 'Mine' else MineMap[i][j].value, end = ' ')
        print('\n')

def CheckForWin():  # Check every mine unit to see if every unit has been marked successfully
    IsWin = True
    for i in range(9):
        if IsWin == False:
            break
        for j in range(9):
            if MineMap[i][j].status == 'Mine':
                if MineMap[i][j].marked == False:
                    IsWin = False
                    break
    return IsWin
                

def click(x, y):  # Player
    if MineMap[x][y].status == 'Mine':
        return False
    if MineMap[x][y].value > 0:
        MineMap[x][y].revealed = True
    if MineMap[x][y].value == 0:
        Clear()
        Dfs(x, y)
    # Update()
    return True

def double_click(x, y):
    # print("DEBUG-Enter in The Func")
    if MineMap[x][y].status != 'Num': # Only Num unit has this func
        # print("A1")
        return
    if MineMap[x][y].arount_count_flag() != MineMap[x][y].value: # Filter the not satisfied unit
        # print("A2")
        return
    # print("DEBUG1")
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            x_ = x + i; y_ = y + j
            if x_ <= 8 and x_ >= 0 and y_ <= 8 and y_ >= 0:
                if MineMap[x_][y_].revealed == True or MineMap[x_][y_].marked == True:
                    continue
                if MineMap[x_][y_].value > 0:
                    MineMap[x_][y_].revealed = True
                else:
                    Clear()
                    Dfs(x_, y_)
                    # print("DEBUG3")



if __name__ == '__main__':
    # Update()
    while True:
        # D = input("INPUT:").split()
        x = int(D[0]); y = int(D[1]); command = D[2] # Command includes: 'Click' 'Mark' 'Unmark' 'Double' 'Info'
        if x < 1 or x > 9 or y < 1 or y > 9:
            print("Format Error!")
            continue
        if FirstClick:
            Init(x - 1, y - 1)
            FirstClick = False
            # Debug
            # OutPutOrigion()   

        if command == 'Click':
            click(x - 1, y - 1)
        if command == 'Mark':
            if MineMap[x - 1][y - 1].revealed == True:
                continue
            if MineMap[x - 1][y - 1].marked == True:
                continue
            MineMap[x - 1][y - 1].marked = True
            MineMap[x - 1][y - 1].revealed = True
            Remain_Mine_Num -= 1
            Update()
        if command == 'Double':
            double_click(x - 1, y - 1)
            Update()

        if command == 'Unmark':
            if MineMap[x - 1][y - 1].status == 'Num':
                continue
            MineMap[x - 1][y - 1].marked = False
            MineMap[x - 1][y - 1].revealed = False
            Remain_Mine_Num += 1
            Update()
        # Just for Debug
        if command == 'Info':
            print("Status: {}".format(MineMap[x - 1][y - 1].status))
            print("Revealed: {}".format(MineMap[x - 1][y - 1].revealed))
            print("Marked: {}".format(MineMap[x - 1][y - 1].marked))
            print("Value: {}".format(MineMap[x - 1][y - 1].value))
            print("Around_Flag: {}".format(MineMap[x - 1][y - 1].arount_count_flag()))

        if CheckForWin():
            print("Succeed!")
            break
