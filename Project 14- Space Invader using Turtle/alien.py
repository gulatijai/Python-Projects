from turtle import Turtle

class Alien(Turtle):
    def __init__(self, x,y):
        super().__init__()
        self.shape("square")
        self.color('red')
        self.penup()
        self.goto(x,y)
        self.speed(0)
        self.move_speed=5
        self.direction=1 # 1 = right, -1 = left

    def move(self):
        self.setx(self.xcor()+self.move_speed*self.direction)

    def move_down(self):
        self.sety(self.ycor()-20)
        self.direction *=-1

    def is_at_boundary(self):
        return self.xcor()>380 or self.xcor()<-380