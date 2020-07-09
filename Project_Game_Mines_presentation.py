#!/usr/bin/env python
# coding: utf-8

# # Python project

# # Game Mines

# # Instructions of game

# In[ ]:


def instructions():
    print('''Mines: Rules of the game,

The minefield in this game is represented by an 8x8 array with alphanumeric \
labels from A1 to H8.
Each of the 8*8=64 alphanumerics represents an imaginary square plot of land \
on the minefield.

Being a minefield, some of the alphanumerics have a mine underneath them.
You need to select mine-free squares by giving the corresponding alphanumeric \
as the input. 

The first input is guaranteed to be a vacant (mine-free) square. 
On selecting a vacant square, it reveals a number, which would inform 
the number of adjacent squares that have mines underneath.

If the number is zero, it means that none of the adjacent squares 
have a hidden mine and so on.
Additionaly if the number revealed by a square given as input is zero, 
then all the adjacent squares would reveal their numbers as well, recursively.

A square can have 3(if in corner) or 5(if on the edge) or 8(anywhere else) \
neighboring squares.
By making use of the clue given by the revealed numbers, 
you have to traverse the whole minefield without stepping on a mine.

On finishig the game successfully or on stepping on a mine, 
all the mine containing squares would be revealed with a ## on them.

Play on.\n''')

    # input prompt seems erratic without next line
    clear_output(wait=True)
    input("Press Enter to continue")
    # to clear the output on next input
    clear_output(wait=True)
    print('''Below is the array representing the mine field.

Each square plot is given an alphanumeric label based on the row and column names. 
Enter the label(case insensitive) to select a square. 

The squares, from now on will be 
represented by [_] until they reveal a number or a mine.''')


# # Data() class 

# In[ ]:


class Data():
    def __init__(self):
        # generating lst_for_array = [[A1,A2,..A8],[..B8],[..H8]]
        self.lst_for_array=[]
        for j in range(65,73):
            self.lst_for_array.append([chr(j)+str(i) for i in range(1,9)])

        # generating array from the list, lst_for_array above for display
        self.field=np.array(self.lst_for_array)
        self.field2=self.field.copy()

        # to make the vacant array for display
        # how to make directly from list of 64 [_]?
        self.fld=[]
        for j in range(8):
            self.fld.append(["[_]" for i in range(8)])
        self.field3=np.array(self.fld)

        # generating the field dataframe ##################################
        # [A,B,C....,H] and [1,2,3...,8]for dataframe index and column name
        self.lsrt=[chr(i) for i in range(65,73)]
        self.quas=[str(i) for i in range(1,9)]
        self.fdf = pd.DataFrame(self.field,index=self.lsrt,columns=self.quas)

        # generating a dictionary of field labels and indices #############
        # generating label_lst=['A1', 'A2', 'A3', 'A4'..., 'H8'] a list of labels
        self.label_lst=[]
        for i in self.lst_for_array:
            self.label_lst.extend([i[t] for t in range(8)])

        # generating index_lst = [[0,0],[0,1],...[7,7]]
        self.index_lst=[]
        for i in range(8):
            self.index_lst.extend([i,j] for j in range(8))

        # generating label_index_dictn={A1:[0,0],A2:[0,1]..., 64:[7,7]}
        self.label_index_dictn=dict([self.label_lst[k],self.index_lst[k]] for k in range(64))

        # for label dictionary of neighbors
        self.label_index_dictn2=self.label_index_dictn.copy()
        self.neigh_lst2_label=[]
        self.neigh_lst1=[]
        for i in range(8):
            for j in range(8):
                self.neigh_lst1+=[[i-1,j-1],[i-1,j],[i-1,j+1],[i,j-1],[i,j+1],                                     [i+1,j-1],[i+1,j],[i+1,j+1]]
                for tse in self.neigh_lst1:
                    if tse in self.index_lst:
                        self.neigh_lst2_label+=[self.label_lst[self.index_lst.index(tse)]]
                # gets null lists below without using list() why?
                self.label_index_dictn2[self.label_lst[self.index_lst.index([i,j])]] =                list(self.neigh_lst2_label)
                del self.neigh_lst2_label[:]
                del self.neigh_lst1[:]
        self.neighbor_dictn = self.label_index_dictn2

        
        ##initializing some more variables ################################
        self.mine_count=0
        self.mine_count2=0
        self.edit_count=0
        self.edited_squares=set()   # a set to contain the value of the edited squares
 

       
    #######################################################################
    # 1st method in Data() to take first input as argument and create mine_list etc.
    def first_inp(self,x0):
        global input_n
        global no_of_mines_str
        self.x0=x0
        self.no_of_mines=0
        while(self.x0 not in self.label_lst and self.x0 != '0'):
            print("\nYou did not enter a matching alphanumeric label\n")
            self.x0 = (input("Enter square's alphanumeric label or enter 0 to stop game: ")).upper()
            if self.x0 in self.label_lst or self.x0 =='0':
                input_n=self.x0
                break
        while(self.no_of_mines == 0 and self.x0 != '0'):
            try:
                while(9 > int(no_of_mines_str) or 31 < int(no_of_mines_str)):
                    print("\nYou did not enter a number from 10 to 30\n")
                    no_of_mines_str=input("\nEnter the no of mines you want to play with (from 10 to 30): ")
                    self.no_of_mines=int(no_of_mines_str)
            except:
                print("Something is not right")
                print("Enter a number from 10 to 30")
                no_of_mines_str=input("\nEnter the no of mines you want to play with (from 10 to 30): ")
            else:
                self.no_of_mines=int(no_of_mines_str)
                break
        # making label list for mines with input removed
        self.label_lst_for_mines=self.label_lst.copy()
        for tt in self.label_lst:
            if tt == self.x0:
                self.label_lst_for_mines.remove(tt)        
        # making list of mine labels
        self.label_lst_of_mines=[]
        while len(self.label_lst_of_mines)<self.no_of_mines:
            rr=np.random.choice(self.label_lst_for_mines)
            if rr not in self.label_lst_of_mines and rr in self.label_lst_for_mines:
                self.label_lst_of_mines.append(rr)
        # zeroes list of labels
        cnt=0
        self.zeroes_label=[]
        for lfg in self.neighbor_dictn:
            for kds in self.neighbor_dictn[lfg]:
                if lfg in self.label_lst_of_mines or kds in self.label_lst_of_mines:
                    cnt+=1
            if cnt==0:
                self.zeroes_label.append(lfg)
            cnt=0


# # Editor() class

# In[ ]:



##########################################################################
# child class of Data to make edits to the field variable
class Editor(Data):
    def __init__(self):
        super().__init__()
        super().first_inp(input_n)

    
    ######################################################################
    # 1st method in Editor(), to recursively reveal adjacent zero numbered squares
    def zero_revealer(self,labelz):
        self.labelz=labelz
        
        self.field3[np.where(self.field2 == self.labelz)] = '00'
        self.field2[np.where(self.field2 == self.labelz)] = '00'

        # to avoid duplicates in edit_count
        if self.labelz not in self.edited_squares:
self.edit_count+=1
        self.edited_squares.add(self.labelz)

        # recursive calling of the function
        for q in self.neighbor_dictn[self.labelz]:
if q not in self.edited_squares:
    self.mine_count2=0
    for l in self.neighbor_dictn[q]:
        if l not in self.edited_squares:
            if l in self.label_lst_of_mines:
                self.mine_count2+=1
    if self.mine_count2 == 0:
        self.zero_revealer(q)
        
    self.field3[np.where(self.field2 == q)] = '0'+str(self.mine_count2)
    self.field2[np.where(self.field2 == q)] = '0'+str(self.mine_count2)

    # to avoid duplicates in edit_count
    if q not in self.edited_squares: 
        self.edit_count+=1
    self.edited_squares.add(q)

        return(self.field3)

    ######################################################################    
    # 2nd method in Editor(), to edit the squares in the array
    def array_edit(self,x01):
        self.x2=x01
        for label in self.label_lst:
if self.x2 == label:
    self.mine_count=0
    for j in self.neighbor_dictn[label]:
        if j in self.label_lst_of_mines:
            self.mine_count+=1
    if self.mine_count == 0:
        self.zero_revealer(label)
        
        self.field3[np.where(self.field2 == self.x2)] = '0'+str(self.mine_count)
        self.field2[np.where(self.field2 == self.x2)] = '0'+str(self.mine_count)
        if self.x2 not in self.edited_squares:
self.edit_count+=1
        self.edited_squares.add(self.x2)

        # revealing additional squares at the beginning 
        if self.edit_count==1:
self.p=np.random.choice(self.zeroes_label)
self.field3[np.where(self.field2 == self.p)] = '00'
self.field2[np.where(self.field2 == self.p)] = '00'
self.edit_count+=1
self.edited_squares.add(self.p)
self.first_square_zero=False #to print the clue based on this
        if self.edit_count>2:
self.first_square_zero=True #to print the clue only once

        return(self.field3)


# # Main loop

# In[ ]:


# main loop of code #######################################################
# imports
from IPython.display import display, clear_output
import numpy as np
import pandas as pd

instructions()

# creating objects of Data() and Editor()
obj1=Data()
display(obj1.fdf)
no_of_mines_str=input("\nEnter the no of mines you want to play with (from 10 to 30), 10 would be good to start with: ")
input_n=input("\nEnter square's alphanumeric label or enter 0 to stop game: ").upper()
obj2=Editor()

# exception handling loop 
while True:
    try:
        while True:
            if obj2.edit_count>=64-len(obj2.label_lst_of_mines):
                print("\nCONGRATS you have traversed the minefield unhurt")
                for v in obj2.label_lst_of_mines:
                    obj2.field3[np.where(obj2.field2 == v)] = '##'
                df3=pd.DataFrame(obj2.field3,index=obj2.lsrt,columns=obj2.quas)
                display(df3)
                break
            elif input_n == '0':
                print("\nGame has been stopped")
                break
            else:
                if obj2.edit_count == 0:
                    firstout=obj2.array_edit(input_n) 
                    df1=pd.DataFrame(firstout,index=obj2.lsrt,columns=obj2.quas)
                    # to clear the output on next input
                    clear_output(wait=True)
                    print("\nTotal no.of. mines in the field is: ",len(obj2.label_lst_of_mines))
                    print("")
                    display(df1)
                elif obj2.edit_count != 0:
                    if obj2.edit_count<20:
                        print('''\nThe numbers indicate the count of the mines in squares 
adjacent to that particular square,
based on which you should be able to deduce an non-mine square''')
                    if obj2.first_square_zero==False:
                        print('\nClue: you can now select any square around {} '.format(obj2.p))
                    input_n = (input("Enter square's alphanumeric label or enter 0 to stop game: ")).upper()
                    if input_n !='0':
                        if input_n in obj2.label_lst_of_mines:
                            print("\nYou stepped on a mine, BOOM!!!")
                            for v in obj2.label_lst_of_mines:
                                obj2.field3[np.where(obj2.field2 == v)] = '##'
                            df4=pd.DataFrame(obj2.field3,index=obj2.lsrt,columns=obj2.quas)
                            display(df4)
                            break
                        if input_n in obj2.edited_squares:
                            print("That square is already revealed, enter another square name")
                            continue
                        else:
                            secondout=obj2.array_edit(input_n)
                            df2=pd.DataFrame(secondout,index=obj2.lsrt,columns=obj2.quas)
                            clear_output(wait=True)
                            print("\nTotal no.of. mines in the field is: ",len(obj2.label_lst_of_mines))
                            print("")
                            display(df2) 
                    else:
                        print("\nGame has been stopped")
                        break
    except:
        print("Something is not right")
        print("Enter an alphanumeric combo as seen in the array or enter 0 to exit")
    else:
        break
print("\nRerun code to play again")

