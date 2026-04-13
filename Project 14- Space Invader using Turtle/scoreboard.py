from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score=0
        self.lives= 3
        self.level=1
        self.hideturtle()
        self.penup()
        self.color('white')
        self.goto(0,20)
        self.update_display()

    def update_display(self):
        self.clear()
        self.write(f"Score: {self.score}  Lives:{self.lives}  Level:{self.level}",
                   align='center', font=('Arial', 16, 'normal'))

    def increase_score(self):
        self.score +=10
        self.update_display()

    def lose_life(self):
        self.lives -=1
        self.update_display()

    def level_up(self):
        self.level+=1
        self.update_display()

    def game_over(self):
        self.goto(0,0)
        self.write("GAME OVER", align="center", font=("Arial", 40, "bold"))
