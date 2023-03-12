# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:08:23 2020

@author: admin
"""
import time

num_of_calls = 0
print(time.time())

def take_input(): #take input from input.txt
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

def take_output(grid): #put output
    with open('solution.txt', 'w') as f:
        for item in grid:
            f.write("%s\n" % item)
        f.write("Backtrack\n")


#checks if number does not occur in row
def num_in_row(grid, row, num):
    for iter1 in range(9):
        if(grid[row][iter1]==num):
            return True #if number does not occur in row
    return False #if number occurs in row

#checks if number does not occur in column
def num_in_col(grid, col, num):
    for iter1 in range(9):
        if(grid[iter1][col]==num):
            return True #if number does not occur in column
    return False #if number occurs in column

#check if number does not occur in 3*3 square
def num_in_square(grid, row, col, num):
    for iter1 in range(3):
        for iter2 in range(3):
            if(grid[iter1+row][iter2+col]==num):
                return True #if number does not occur in square
    return False  #if number occurs in column      

#find the next blank space in the grid
def next_blank(grid): 
	for it1 in range(9): 
		for it2 in range(9): 
			if(grid[it1][it2]==0): #return co ordinates of next blank 
				return (it1, it2)
	return False

def backtracker(grid, num_of_calls):
    
    c = [0,0] #iterator stores memory of next blank across grid
    
    if(not next_blank(grid)):
        return True #no blank exists
    else:
        c = next_blank(grid)   
    
    row = c[0]
    col = c[1]
    
    for num in range(1,10): #check numbers one after another 
        if(not num_in_row(grid, row, num) and not num_in_col(grid, col, num) and not num_in_square(grid, row-row%3, col-col%3, num)): #check if number can be filled in the position
            grid[row][col]= num
            num_of_calls.append("0") #append to mark a step
            if(backtracker(grid, num_of_calls)):#check iteratively over next blank
                return True
            grid[row][col]=0 #incase of improper assignment, return to 0
        
    return False #traverse back in loop

if __name__=="__main__": 
    
    grid = take_input()       
    num_of_calls= []
    if(backtracker(grid, num_of_calls)): 
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in grid]))
        print(len(num_of_calls))
    else: 
        print ("No solution exists")
    
    take_output(grid)
    print(time.time())
   
        