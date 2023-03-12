# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:54:15 2020

@author: admin
"""
import sys
import time
import random

print(time.time())
no_of_calls = []

def take_input(): #take inputs from input.txt
    x = open('input.txt',"r")
    array = x.readlines()
    array = list(map(lambda s: s.strip(), array))
    arr2=[]
    for i in array:
        i = i.split(" ")
        arr2.append(i)
    arr3 = []
    for i in range(9):    
        arr3.append(list(map(int, arr2[i])))
 
    return arr3

class Sudoku():
    def __init__(self, state:[], size:int, column_size:int, row_size:int):
        
        # Set values for the variable
        self.state = state
        self.size = size
        self.column_size = column_size
        self.row_size = row_size
        self.states = {}

        # Create states for numbers
        self.update_states()
        
    # Update states for cells
    def update_states(self):

        # Reset states
        self.states = {}
        
        numbers = []

        # Loop the state
        for y in range(self.size):
            for x in range(self.size):
                
                # Check if a cell is blank
                if (self.state[y][x] == 0):

                    # check all possible numbers
                    numbers = []
                    for number in range(1, self.size + 1):

                        # Check if the number is allowed
                        if(self.is_allowed(number, y, x) == True):
                            numbers.append(number)

                    # Add numbers to a state
                    if(len(numbers) > 0):
                        self.states[(y, x)] = numbers
                            
    # Check if a number is permissible
    def is_allowed(self, number:int, row:int, column:int) -> bool:

        # Check a row
        for iter1 in range(self.size):

            # Return false if the number exists in the row
            if (iter1 != column and self.state[row][iter1] == number):
                return False

        # Check a column
        for iter2 in range(self.size):
            
            # Return false if the number exists in the column
            if (iter2 != row and self.state[iter2][column] == number):
                return False

        row_start = (row//self.row_size)*self.row_size
        col_start = (column//self.column_size)*self.column_size;

        # Check 3*3 space
        for iter1 in range(row_start, row_start+self.row_size):
            for iter2 in range(col_start, col_start+self.column_size):
                
                # Return false if the number exists in the 3*3 space
                if (iter1 != row and iter2 != column and self.state[iter1][iter2]== number):
                    return False

        # Return true if no conflicts
        return True

    # Calculate number of conflicts
    def no_of_conflicts(self, number:int, row:int, column:int) -> int:

        no_of_conflicts = 0

        # Check a row
        for iter1 in range(self.size):

            # Check if a conflict is found in a row
            if (iter1 != column and self.state[row][iter1] == number):
                no_of_conflicts += 1

        # Check a column
        for iter2 in range(self.size):
            
            # Check if a conflict is found in a column
            if (iter2 != row and self.state[iter2][column] == number):
                no_of_conflicts += 1

        row_start = (row//self.row_size)*self.row_size
        col_start = (column//self.column_size)*self.column_size;

        # Check 3*3 space
        for iter1 in range(row_start, row_start+self.row_size):
            for iter2 in range(col_start, col_start+self.column_size):
                
                # Check 3*3 space
                if (iter1 != row and iter2 != column and self.state[iter1][iter2]== number):
                    no_of_conflicts += 1

        return no_of_conflicts

    # Create an initial solution
    def initial_solution(self):
        
        # Generate an initial solution
        for (y,x), numbers in self.states.items():

            # A dictionary to store numbers and the number of conflicts for each number
            scores = {}

            # check all numbers
            for number in numbers:

                # Add to conflicts dictionary
                scores[number] = self.no_of_conflicts(number, y, x)

            # Sort scores on number of conflicts to get best value
            scores = {key: value for key, value in sorted(scores.items(), key=lambda item: item[1])}

            # Get best numbers
            best_numbers = []
            min = sys.maxsize
            for key, value in scores.items():

                # Add a number if it is less or equal to current minimum
                if(value <= min):
                    best_numbers.append(key)
                    min = value

            # Assign a number at random (one of the best numbers)
            self.state[y][x] = random.choice(best_numbers)

        # Print initial solution
        print('\nInitial solution:')
        self.print_state()
        print()

    # Min-conflicts algorithm
    def min_conflicts(self, var_rate:float=0.04, val_rate:float=0.02, max_steps:int=100000) -> bool:

        # Generate an initial solution
        self.initial_solution()

        # repeatedly choose a random variable in conflict and change it
        for i in range(max_steps):

            if((i + 1)%10000 == 0):
                print(max_steps - i - 1)

            conflicts = []
            conflict_count = 0

            # Get all variables that are in conflict
            for (y,x), numbers in self.states.items():

                # Check if the number is allowed
                if(self.is_allowed(self.state[y][x], y, x) == False):
                    
                    # Add the cell
                    conflicts.append((y,x))

                    # Add to the conflict count
                    conflict_count += 1

                # random to jump out from a local minimum
                elif (random.random() < var_rate):

                    # Add the cell
                    conflicts.append((y,x))

            # Check if we have a valid solution
            if(conflict_count <= 0):
                return True

            # Select a cell in conflict at random
            y, x = random.choice(conflicts)

            # Get numbers to chose from
            numbers = self.states.get((y, x))

            # Loop numbers
            scores = {}
            for number in numbers:

                # Add the number of conflicts as a score
                scores[number] = self.no_of_conflicts(number, y, x)

            # Sort scores on value
            scores = {key: value for key, value in sorted(scores.items(), key=lambda item: item[1])}
            
            # Get best numbers
            best_numbers = []
            min = sys.maxsize
            for key, value in scores.items():

                # Add a number if it is less or equal to current minimum
                if (value <= min):
                    best_numbers.append(key)
                    min = value

                # random to jump out from local minimum
                elif (random.random() < val_rate):
                    best_numbers.append(key)

            # Assign a number
            self.state[y][x] = random.choice(best_numbers)
            no_of_calls.append("0")

        # No solution was found, return false
        return False
        
    def print_state(self):
        for y in range(self.size):
            print(' ', end='')
            for x in range(self.size):
                if x != 0 and x % self.column_size == 0:
                    print(' ', end='')
                digit = str(self.state[y][x]) if len(str(self.state[y][x])) > 1 else ' ' + str(self.state[y][x])
                print('{0} '.format(digit), end='')
            print(' ')
    
    def take_output(self): #put output
        with open('solution.txt', 'w') as f:
            for item in self.state:
                f.write("%s\n" % item)
            f.write("Min conflict solution\n")
    

if __name__=="__main__": 
    
    grid = take_input()   
    var_rate = 0.02
    val_rate = 0.03
    max_steps = 200000
    
    sudoku = Sudoku(grid, 9, 3, 3)
    
    success = sudoku.min_conflicts(var_rate, val_rate, max_steps)
    
    print('\nPuzzle solution:') if success == True else print('\nNo solution was found!!!\nEnd state:')
    sudoku.print_state()
    print(len(no_of_calls))
    sudoku.take_output()
     
    print(time.time())