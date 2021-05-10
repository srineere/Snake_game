# importing required libraries
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from random import randint


class Snake(tk.Canvas):

    # Static Variables
    MOVE_INC = 20
    MOVES_PER_SECOND = 15
    GAME_SPEED = 1000 // MOVES_PER_SECOND


    def __init__(self):
        
        super().__init__(width=600,height=600,background="black")
        self.startMenu()  


    # Menu 
    def startMenu(self):

        # Helper methods
        def startclick(event):
            self.delete("all")
            self.start()
       
        def quitclick(event):
            root.destroy()
        
        def inc_speed(event):
            self.GAME_SPEED = self.GAME_SPEED +10
            self.itemconfigure(self.find_withtag("speed"), text=f"Game Speed:   {self.GAME_SPEED}", tag="speed")
        
        def dec_speed(event):
            self.GAME_SPEED = self.GAME_SPEED - 10
            self.itemconfigure(self.find_withtag("speed"), text=f"Game Speed:   {self.GAME_SPEED}", tag="speed")

        # Border
        self.create_rectangle(7,27,593,593,outline="#525d69")

        # Game Name
        self.create_text( 300,150, text=f"Snake Game", tag="start",fill="#0ff",font=('Arial',30,'bold italic'))

        # Start Button
        start = self.create_text(300,300, text="Start", tag="start",fill="#fff",font=(20))
        self.tag_bind(start, "<Button-1>", startclick)

        # Game Speed Change
        self.create_text( 300,350, text=f"Game Speed:   {self.GAME_SPEED}", tag="speed",fill="#fff",font=(20))
        
        plus = self.create_text(395,350, text="+", tag="inc",fill="#fff",font=(20))
        self.tag_bind(plus, "<Button-1>", inc_speed)
        
        minus = self.create_text(350,350, text="-", tag="dec",fill="#fff",font=(20))
        self.tag_bind(minus, "<Button-1>", dec_speed)

        # Quit Button
        quit = self.create_text(300,400, text="Quit", tag="quit",fill="#fff",font=(20))
        self.tag_bind(quit, "<Button-1>", quitclick)
   

    # start game
    def start(self):

        self.snake_position = [(100,100),(80,100),(60,100)]  # intial position of snake
        self.food_position = self.set_new_food()  # initial positio of food
        self.score = 0  # initial score
        self.direction = "Right"  # initial direction
        
        self.bind_all("<Key>", self.on_key_press) 
        self.load_assets()
        self.create_objects()
        self.after(75,self.perform_actions)
    

    # load assets required
    def load_assets(self): 
        
        try:
            self.snake_body_image = Image.open("assets/head.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)
            
            self.food_image = Image.open("assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)

        except IOError as error:
            print(error)
            root.destroy()


    # creating the objects req
    def create_objects(self): 

        # displaying score
        self.create_text( 45,12, text=f"Score: {self.score}", tag="score",fill="#fff",font=(15))
        
        # displaying snake body
        for x, y in self.snake_position:
            self.create_image(x,y,image=self.snake_body, tag="snake")
        
        # displaying food
        self.create_image(self.food_position[0],self.food_position[1],image=self.food,tag="food")
        
        #displaying the boundary wall
        self.create_rectangle(7,27,593,593,outline="#525d69")


    # used to move snake
    def perform_actions(self): 

        if(self.check_collisions()):
            self.end_game()
            return

        self.check_food_eaten()
        self.move_snake()
        self.after(self.GAME_SPEED,self.perform_actions)


    # if food is eaten by snake
    def check_food_eaten(self):

        if( self.snake_position[0] == self.food_position) :
            self.score += 1
            self.snake_position.append(self.snake_position[-1])
            self.create_image(
                *self.snake_position[-1], image=self.snake_body, tag="snake" )
            
            self.food_position = self.set_new_food()
            self.coords(self.find_withtag("food"),self.food_position)
            
            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}",tag="score")


    def set_new_food(self):
        while(True):
            x = randint(1,29)*self.MOVE_INC
            y = randint(1,29)*self.MOVE_INC
            food_pos = (x,y)

            if(food_pos not in self.snake_position):
                return food_pos


    # for the movements of snake
    def move_snake(self): 
        
        head_x , head_y = self.snake_position[0]

        if(self.direction=="Left"):
            new_head_pos = (head_x - self.MOVE_INC, head_y) 
        elif(self.direction=="Right"):
            new_head_pos = (head_x + self.MOVE_INC, head_y) 
        elif(self.direction=="Down"):
            new_head_pos = (head_x , head_y + self.MOVE_INC) 
        elif(self.direction=="Up"):
            new_head_pos = (head_x , head_y - self.MOVE_INC) 

        self.snake_position = [new_head_pos] + self.snake_position[:-1]

        for seg, pos in zip(self.find_withtag("snake"), self.snake_position):
            self.coords(seg,pos)


    # used to check for collisions 
    def check_collisions(self): 
        head_x , head_y = self.snake_position[0]

        return ( 
            head_x in (0,600) 
            or head_y in (20,600) 
            or (head_x,head_y) in self.snake_position[1:] )


    # mappin the arrow keys to snake movement
    def on_key_press(self,e):  
        new_direc = e.keysym 
        all_direction = ("Up","Down","Left","Right")
        opp_direc = ({"Up", "Down"},{"Right","Left"})

        if ( new_direc in all_direction and {new_direc,self.direction} not in opp_direc): 
            self.direction = new_direc


    # Final Card
    def end_game(self):
        window.delete("all")
        self.create_text(300,200, text=f"Game Over !!   Your Score: {self.score} ", fill="#fff", font=(20))
        def clicked(event):
            window.delete("all")
            self.start()
        buttonTXT = window.create_text(300, 300,fill="#fff", text="Retry",font=(15))
        window.tag_bind(buttonTXT, "<Button-1>", clicked) 
        self.create_text(545, 580,fill="#fff", text="By, Srineer Kaleri")



root = tk.Tk()
root.title("Snake Game");
root.resizable(False, False)

window = Snake()
window.pack()

root.mainloop()
