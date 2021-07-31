import asyncio
from random import randrange
from databases import Database

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import threading
from tkinter import *

global x
global sof
global level
global a

def callback(event):
    global l
    global a
    global x0
    global y0
    global x1
    global y1
    event.x, event.y
    if event.x >= x0 and event.x<= x1 and event.y >= y0 and event.y <= y1 :
        #print("great!")
        l.destroy()
        score_label()
        l.pack()
    #print(event.x, event.y , x1)

def create_circle(x, y, r, canvasName): #center coordinates, radius
    global x0
    global y0
    global x1
    global y1
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    print( "x0= " +  str(x0) + " x1= " + str(x1) + " y0= " +  str(y0)  + " y1= " + str(y1) )
    return canvasName.create_oval(x0, y0, x1, y1 , outline="#000000", fill="#f50")

def score_label():
    global a
    global l
    global x
    global sof
    a=a+1
    l = Label(root, text=str(a))
    l.config(font=("Courier", 14))


def game_over():
    global l
    global a
    a="Game over you have gained "+ str(a) + " points"
    l = Label(root, text=str(a))
    l.config(font=("Courier", 14))

score_limit= 15
score_limits =[score_limit]
print(score_limits[0])
y=0.5
for x in range(1,5):
    score_limit=int(score_limit*(1.15+y))
    y=y+0.1
    score_limits.append(score_limit)
    print(score_limits[x])
    #score_limits = [15, 35 ]


width=500
height=200
root = Tk()
myCanvas = Canvas(root, width=width, height=height)
a=-1
x=2
sof =6
level=0
myCanvas.pack()


#queue = asyncio.Queue()
#loop = asyncio.get_event_loop()

async def before_game():
    global continue_game
    global l
    global b
    global score_limits
    continue_game=0
    message = "you need to get minimum " + str(score_limits[level] ) + " points"
    l = Label(root, text=str(message))
    l.config(font=("Courier", 14))
    l.pack()
    root.update_idletasks()
    root.update()
    await asyncio.sleep(2)
    l.destroy()
    b = 3
    while b>0:
        message= "level "+ str(level+1) +" will start in "+ str(b)
        l = Label(root, text=str(message))
        l.config(font=("Courier", 14))
        l.pack()
        b=b-1
        root.update_idletasks()
        root.update()
        await asyncio.sleep(1)
        l.destroy()
    continue_game=1




async def game():
    global sof
    global x
    global l
    global continue_game
    global a
    global  level
    global  score_limit
    continue_game=0
    l.destroy()
    score_label()
    l.pack()
    x = 2
    sof = 6
    myCanvas.bind("<Button-1>", callback)
    while x<sof:
        #points_to_get=myCanvas.create_text((60, 10), text="minimum " + str(score_limits[level]) + " points")
        points_to_get=myCanvas.create_text(( 10, 10), fill="darkblue", font="Times 14 italic ",
                                           text="minimum " + str(score_limits[level]) + " points")
        myCanvas.move(points_to_get, myCanvas.bbox(points_to_get)[3] - myCanvas.bbox(points_to_get)[0] ,10)
        print(myCanvas.bbox(points_to_get))
        #print(points_to_get.winfo_width())
        #print(str(points_to_get.winfo_height()))
        x_circle= randrange(20 ,width-20,20)
        y_circle= randrange(20,height-20,20)
        while myCanvas.bbox(points_to_get)[2] >=  x_circle-20 or myCanvas.bbox(points_to_get)[3] >= y_circle-20 :
            x_circle = randrange(20, width - 20, 20)
            y_circle = randrange(20, height - 20, 20)
        #myCanvas.create_text((x_circle, y_circle),text="str(sof-x)" )
        circle2 = create_circle( x_circle, y_circle , 20, myCanvas)
        myCanvas.create_text((x_circle, y_circle),text=str(sof-x) )
        root.update_idletasks()
        root.update()
        await asyncio.sleep(1.5)
        # print('... World!')
        myCanvas.delete("all")
        #await asyncio.sleep(1)
        x=x+1

'''
@asyncio.coroutine
def consume():
    while True:
        value = yield from queue.get()
        print("Consumed", value)
'''
def start_async_stuff():
    global a
    global level
    global score_limits
    global l
    print('lets async!')
    run_game=1
    not_first_time=0
    while run_game:
        if not_first_time==1:
            l.destroy()
        not_first_time=1
        asyncio.run(before_game())
        asyncio.run(game())
        # myCanvas.unbind("<Button-1>", callback)
        myCanvas.unbind("<Button 1>")
        if a < score_limits[level]:
            l.destroy()
            game_over()
            l.pack()
            run_game=0
        level = level + 1
    #loop.run_forever()
   # asyncio.run(game())

threading.Thread(target=start_async_stuff).start()
root.mainloop()
