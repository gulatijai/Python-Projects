from turtle import Turtle

class Bullet(Turtle):
    def __init__(self, x, y, direction):
        super().__init__()
        self.shape("circle")
        self.shapesize(0.3,0.3)
        self.color("white")
        self.penup()
        self.goto(x,y)
        self.speed(0)
        self.speed=20
        self.direction= direction

    def move(self):
        self.sety(self.ycor()+self.speed*self.direction)

    def is_off_screen(self):
        return self.ycor()>300 or self.ycor()<-300