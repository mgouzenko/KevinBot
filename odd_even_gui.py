'''
***************************************************************************
Mitchell Gouzenko
Mag2272
Description: A gui version of odds and evens.
***************************************************************************
''' 
import tkMessageBox as tkm
import Tkinter as tk
import random

class odd_even_game():
    def __init__(self):
        self.main = tk.Tk()
        self.main.title('Mitchell Gouzenko - Mag2272')
        
        #Initialize the computer's winning mod - that is, the remainder
        #that the computer needs to achieve after dividing the round total
        #by two, so that the computer wins. Basically, a 0 corresponds to
        #the computer being even and a 1 corresponds to it being odd.
        self.comwin = tk.IntVar(value=0)
        
        #Initialize scores & rounds played to 0.
        self.comscore=0
        self.humscore=0
        self.rounds_played=0
        
        #Initialize a variable to keep track of the prior round's result.
        self.winner= tk.StringVar(value='Welcome to Odds & Evens.\n Click '
            'a button below: ')
        
        #Initialize variables to keep track of scores.
        self.scorevar = tk.StringVar(value = 'Your Score: $0')
        self.comscorevar = tk.StringVar(value = 'Computer Score: $0')

        # Create three vertical levels of frames.
        self.top_frame = tk.Frame()
        self.mid_frame = tk.Frame()
        self.bottom_frame = tk.Frame()
        
        #Create three levels of bottom frame and turn of their propagation.
        self.bottom_left=tk.Frame(self.bottom_frame,width=200,height=25)
        self.bottom_left.pack_propagate(0)
        self.bottom_mid=tk.Frame(self.bottom_frame)
        self.bottom_right=tk.Frame(self.bottom_frame,width=200,height=25)
        self.bottom_right.pack_propagate(0)
        
        #Create a separate frame in which to pack the radio buttons.
        self.radio_frame=tk.Frame(self.mid_frame)
        
        #Create a similar frame to report scores
        self.score_frame=tk.Frame(self.mid_frame)
        
        #Initiate labels that will ouput the title, score, and winner of 
        #each round.
        self.title_label = tk.Label(self.top_frame, text='Odds and Evens',\
            font=("Helvetica", 20),bg='black',fg='white', width = 53)           
        
        #This label will let the user know who won the round.    
        self.winner_label=tk.Label(self.mid_frame,\
            textvariable=self.winner,height=2,width=30)
        
        #These label will print the score.
        self.score_label = tk.Label(self.score_frame,\
            textvariable=self.scorevar,width=20)
        self.com_score_label = tk.Label(self.score_frame,\
            textvariable = self.comscorevar,width=20)
        
        #Initiate buttons to throw odds or evens using the play function.
        #The lambda operator is used to create just one instance of the
        #function in order to pass in a value.
        self.odd_button=tk.Button(self.bottom_mid,text='Throw a 1',\
            command=lambda:self.play(1))
        self.even_button = tk.Button(self.bottom_mid,text='Throw a 2',\
            command=lambda: self.play(2))
        
        #Initiate radio buttons for the user to pick if he/she is playing 
        #as odd or even.
        self.odd_rb=tk.Radiobutton(self.radio_frame,text='Play as Odd Player', \
            variable=self.comwin,value=0,width=20)          
        self.even_rb=tk.Radiobutton(self.radio_frame,text='Play as Even Player',\
            variable = self.comwin,value=1,width=20)
        
        #Initiate a quit button that relys on the quit function.
        self.quit_button = tk.Button(self.bottom_right,text='End Game',\
            command=self.quit,width=16)
              
        #Pack the title.
        self.title_label.pack()
        
        #Pack the score labels into the score frame and pack the score 
        #frame into the mid frame.
        self.score_label.pack(side='top')
        self.com_score_label.pack(side = 'bottom')
        self.score_frame.pack(side='left')
        
        #Pack the odd and even radio buttons into their own separate frame.
        self.odd_rb.pack()
        self.even_rb.pack()
        #Pack the radio button frame into the right of the mid frame.
        self.radio_frame.pack(side='right')
        
        #Pack the winner label into the middle of the mid frame.
        self.winner_label.pack()
        
        #Pack the even/odd buttons into the middle of the bottom frame.
        self.even_button.pack(side='left')
        self.odd_button.pack(side='left')
        
        #Pack the quit button into the right of the bottom frame.
        self.quit_button.pack(side='right')

        #Pack top and mid frames.
        self.top_frame.pack()
        self.mid_frame.pack()
        
        #Pack all three segments of bottom frame.
        self.bottom_left.pack(side='left')
        self.bottom_mid.pack(side='left')
        self.bottom_right.pack(side='left')

        #Finally, pack the bottom frame.
        self.bottom_frame.pack()
        
        #Loop over the class.
        tk.mainloop()

          
    #Allows the computer to determine a move based on a probability 
    #threshold.
    def computer_move(self,threshold):
        '''Generates computer move based on threshold between 0 & 100. The
        threshold represents percentage of time computer picks 1.'''
        #Generate a random number from 0 to 100.
        x = random.random()*100
        if threshold>x:
            return 1
        else:
            return 2
    
                   
    def play(self,hmove):
        '''Plays a game of odd/even between the human and the computer,
        with a computer threshold of 50'''
        #Computer makes a move:
        com = self.computer_move(50)
        
        #Determine if computer wins
        if (com+hmove)%2 == self.comwin.get():
            #If computer wins: Set the value of the results that the 
            #computer reports after the round.
            result = 'The computer picked ' + str(com) + '.\nYou lose $' \
                +str(com+hmove) + '.'          
            self.winner.set(result)
            
            #Increment scores accordingly.
            self.comscore += (com+hmove)
            self.humscore -=(com+hmove)
            
            #If the computer hasn't won, then it has to have lost the 
            #round. Increase/decrease scores accordingly.
        else:
            result = 'The computer picked ' + str(com) + '.\nYou win $' \
                +str(com+hmove) + '.'
            self.winner.set(result)
            self.humscore += (com+hmove)
            self.comscore -= (com+hmove)
            
        #Set the value of the stringvar that reports the total scores.
        if self.humscore>=0:
            self.scorevar.set(value='Your Score: $'+str(self.humscore))
            self.comscorevar.set(value='Computer Score: -$'\
                +str(self.humscore))
        else:
            self.scorevar.set(value='Your Score: -$'+str(self.comscore))
            self.comscorevar.set(value='Computer Score: $'\
                +str(self.comscore))
        
        #Increment the number of rounds played.
        self.rounds_played+=1
    
    #Provide a function that quits the game and shows the user the results.
    def quit(self): 
        info = self.scorevar.get() 
        tkm.showinfo('Results',info+'\n\nRounds Played:\n'+\
            str(self.rounds_played))
        self.main.destroy()
                             
                                    
game = odd_even_game()