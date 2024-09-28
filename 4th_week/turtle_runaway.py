# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random
import time

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        self.start_time = None
        self.score = None

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # TODO) You can do something here and follows.
        self.show_you()
        
        self.start_time = time.time()
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.remove_you, 3000)
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def show_you(self):
        # runner 위에 'YOU'를 표시
        self.drawer.penup()
        self.drawer.setpos(self.runner.pos())
        self.drawer.write("YOU", align="center", font=("Arial", 20, "bold"))

    def remove_you(self):
        # 'YOU' 지우기
        self.drawer.undo()

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # TODO) You can do something here and follows.
        is_catched = self.is_catched()
        elapsed_time = int(time.time() - self.start_time)

        if is_catched:
            self.drawer.undo()
            self.drawer.penup()
            self.drawer.setpos(-300, 300)
            self.score = elapsed_time
            self.drawer.write(f'Game Over! Score: {self.score}')
        else:
            self.drawer.undo()
            self.drawer.penup()
            self.drawer.setpos(-300, 300)
            self.drawer.write(f'Hurry Up!! | Time: {elapsed_time} sec')

            # Note) The following line should be the last of this function to keep the game playing
            self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        x, y = self.pos()
        target_x, target_y = opp_pos
        angle_to_target = self.towards(target_x, target_y)
        self.setheading(angle_to_target)
        self.forward(self.step_move)
        
        # mode = random.randint(0, 5)
        # if mode >= 0 and mode <= 2:
        #     self.forward(self.step_move)
        # elif mode == 3:
        #     self.left(self.step_turn)
        # elif mode == 4:
        #     self.right(self.step_turn)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    chaser = RandomMover(screen)
    runner = ManualMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
