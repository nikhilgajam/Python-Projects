import turtle
import random
import time


class TurtleRace:
    WIDTH, HEIGHT = 700, 600
    COLORS = ['green', 'blue', 'orange', 'yellow', 'white', 'red', 'purple', 'pink', 'brown', 'cyan']

    def __init__(self):
        self.number_of_turtles = 0
        self.turtles = []

        self.get_input_number()
        self.set_turtle_screen()
        random.shuffle(self.COLORS)
        self.colors = self.COLORS[:self.number_of_turtles]
        winner = self.race(self.colors)
        print('{} turtle is the winner!'.format(winner.capitalize()))
        time.sleep(3)

    def get_input_number(self):
        while True:
            self.number_of_turtles = input("Enter No. Of Turtles to start the race (2-10): ")

            if self.number_of_turtles.isdigit():
                self.number_of_turtles = int(self.number_of_turtles)
            else:
                print("Enter a number not any character!")
                continue

            if 2 <= self.number_of_turtles <= 10:
                return self.number_of_turtles
            else:
                print("Enter a number in the range of 2 to 10\n")

    def set_turtle_screen(self):
        screen = turtle.Screen()
        screen.bgcolor('#35363a')
        screen.setup(self.WIDTH, self.HEIGHT)
        screen.title("Turtle Racing!")
        screen.getcanvas().winfo_toplevel().call('wm', 'attributes', '.', '-topmost', '1')

    def creating_turtles(self, colors):
        x_spacing = self.WIDTH // (len(colors) + 1)

        for i, color in enumerate(colors):
            turtle_participant = turtle.Turtle()
            turtle_participant.shape('turtle')
            turtle_participant.color(color)
            turtle_participant.left(90)
            turtle_participant.penup()
            turtle_participant.setpos(-self.WIDTH // 2 + (i+1) * x_spacing, -self.HEIGHT // 2 + 20)
            turtle_participant.pendown()
            self.turtles.append(turtle_participant)

        return self.turtles

    def race(self, colors):
        turtles = self.creating_turtles(colors)

        while True:
            for racer in turtles:
                distance_to_move = random.randrange(1, 20)
                racer.forward(distance_to_move)

                x, y = racer.pos()
                if y >= self.HEIGHT // 2 - 25:
                    return self.colors[turtles.index(racer)]


if __name__ == '__main__':
    TurtleRace()
