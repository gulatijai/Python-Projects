import time
from turtle import Turtle, Screen
from player import Player
from alien import Alien
from bullet import Bullet
from scoreboard import Scoreboard
import random

screen= Screen()
screen.setup(width=800, height=600)
screen.bgcolor('black')
screen.title("Space Invaders")
screen.tracer(0)# turns off auto animation

player= Player()
scoreboard= Scoreboard()
alien_shoot_timer=0

aliens=[]
for row in range(3):
    for column in range(8):
        x= -280 + column*80
        y= 200- row*60
        alien= Alien(x,y)
        aliens.append(alien)

player_bullets=[]
alien_bullets=[]

def shoot():
    bullet= Bullet(player.xcor(), player.ycor()+20, 1)
    player_bullets.append(bullet)

screen.listen()  # keyboard binding
screen.onkey(player.move_left, "Left")
screen.onkey(player.move_right, "Right")
screen.onkey(shoot, "space")

game_running = True
while game_running:
    screen.update()
    time.sleep(0.02)


    for bullet in player_bullets[:]:
        bullet.move()
        if bullet.is_off_screen():
            bullet.hideturtle()
            player_bullets.remove(bullet)

    for alien in aliens:
        alien.move()
        if alien.is_at_boundary():
            for a in aliens:
                a.move_down()
            break
    alien_shoot_timer += 1
    if alien_shoot_timer >= 50:
        if aliens:
            shooting_alien= random.choice(aliens)
            bullet= Bullet(shooting_alien.xcor(), shooting_alien.ycor()-20,-1)
            alien_bullets.append(bullet)
        alien_shoot_timer=0

    for bullet in alien_bullets[:]:
        bullet.move()
        if bullet.is_off_screen():
            bullet.hideturtle()
            alien_bullets.remove(bullet)

    for bullet in alien_bullets[:]:
        if abs(bullet.xcor()-player.xcor())<20 and abs(bullet.ycor()-player.ycor())<20:
            bullet.hideturtle()
            alien_bullets.remove(bullet)
            scoreboard.lose_life()
            if scoreboard.lives==0:
                game_running= False
                scoreboard.game_over()
                screen.update()
                time.sleep(2)

    for bullet in player_bullets[:]:
        for alien in aliens[:]:
            if abs(bullet.xcor()- alien.xcor())<20 and abs(bullet.ycor()- alien.ycor())<20:
                bullet.hideturtle()
                player_bullets.remove(bullet)
                alien.hideturtle()
                aliens.remove(alien)
                scoreboard.increase_score()
                break

    for alien in aliens:
        if alien.ycor()<-250:
            scoreboard.lose_life()
            if scoreboard.lives==0:
                game_running= False
                scoreboard.game_over()
                screen.update()
                time.sleep(2)

    if len(aliens)==0:
        scoreboard.level_up()
        for alien in aliens:
            alien.move_speed+=1

        for row in range(3):
            for column in range(8):
                x = -280 + column * 80
                y = 200 - row * 60
                alien = Alien(x, y)
                aliens.append(alien)



screen.mainloop()