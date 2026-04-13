from tkinter import Canvas, Tk


game_running= True

class Paddle:
    def __init__(self, canvas):
        self.canvas= canvas
        self.id= self.canvas.create_rectangle(350,550,450,560, fill='blue')

    def move_left(self, event):
        self.canvas.move(self.id, -20, 0)

    def move_right(self,event):
        self.canvas.move(self.id, 20, 0)

class Ball:
    def __init__(self, canvas,paddle, bricks):
        self.canvas= canvas
        self.paddle= paddle
        self.bricks= bricks
        self.dx= 3
        self.dy= -3
        self.id= self.canvas.create_oval(390,300,402,312, fill= 'white')

    def move_ball(self):
        if not game_running:
            return
        self.canvas.move(self.id, self.dx, self.dy)
        self.check_wall_collision()
        self.check_paddle_collision()
        self.check_brick_collision()
        self.canvas.after(16, self.move_ball)

    def check_wall_collision(self):
        self.coord = self.canvas.coords(self.id)

        if self.coord[0] <= 0: #x1 left wall, x2 right wall
            self.dx=-self.dx
        if self.coord[2] >= 800:
            self.dx=-self.dx

        if self.coord[1] <= 0  : # y1 right wall
            self.dy=-self.dy
        if self.coord[3] >=600  : # y2 right wall
            global game_running
            game_running= False
            self.canvas.create_text(400,300, text="Game Over", fill='red', font=("Arial", 60))


    def check_paddle_collision(self):
        self.overlapping= self.canvas.find_overlapping(self.coord[0], self.coord[1], self.coord[2], self.coord[3])
        if self.paddle.id in self.overlapping:
            self.dy=-self.dy

    def check_brick_collision(self):
        global score
        self.overlapping= self.canvas.find_overlapping(self.coord[0], self.coord[1], self.coord[2], self.coord[3])
        for brick_id in self.bricks:
            if brick_id in self.overlapping:
                self.dy=-self.dy
                self.canvas.delete(brick_id)
                self.bricks.remove(brick_id)
                score += 1
                self.canvas.itemconfig(score_display, text=f"Score: {score}")

                if len(self.bricks)==0:
                    global game_running
                    game_running= False
                    self.canvas.create_text(400,300, text="You Win", fill='green', font=("Arial", 60))


#-----------------------------------------------------------------------
window= Tk()
window.title("Breakout game")
window.config(pady=20, padx=20)

canvas= Canvas(width=800, height=600, background='black')
canvas.pack()

paddle= Paddle(canvas)
bricks = []
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
for row in range(6):
    for col in range(9):
        x1= 35+ col*80
        y1= 50+ row*25
        x2= x1+75
        y2= y1+20
        brick= canvas.create_rectangle(x1,y1,x2,y2, fill=colors[row])
        bricks.append(brick)
ball= Ball(canvas, paddle, bricks)

score=0
score_display= canvas.create_text(650,10, text="Score: 0 ", fill='white', font=("Arial", 16))

ball.move_ball()
window.bind("<Left>", paddle.move_left)
window.bind("<Right>", paddle.move_right)


window.mainloop()