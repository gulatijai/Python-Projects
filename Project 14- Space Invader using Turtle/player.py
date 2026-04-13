from turtle import Turtle

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('triangle')
        self.color('green')
        self.penup()
        self.goto(0,-280)
        self.setheading(90)
        self.speed(0)
        self.move_speed=20

    def move_left(self):
        if self.xcor()>-380:
            self.setx(self.xcor()-self.move_speed)

    def move_right(self):
        if self.xcor()<380:
            self.setx(self.xcor()+self.move_speed)
