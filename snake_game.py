import turtle
import time
import random

# Rainbow colors
RAINBOW_COLORS = [
    "red", "orange", "yellow", "green", "blue", "indigo", "violet"
]

# Game settings
WIDTH, HEIGHT = 600, 600
SEGMENT_SIZE = 20
DELAY = 0.1

# Directions
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

def random_food_position():
    x = random.randint(-WIDTH//2 + SEGMENT_SIZE, WIDTH//2 - SEGMENT_SIZE)
    y = random.randint(-HEIGHT//2 + SEGMENT_SIZE, HEIGHT//2 - SEGMENT_SIZE)
    # Snap to grid
    x -= x % SEGMENT_SIZE
    y -= y % SEGMENT_SIZE
    return x, y

class Snake:
    def __init__(self):
        self.segments = []
        self.directions = []
        self.colors = []
        self.create_snake()
        self.direction = RIGHT
        self.color_index = 0

    def create_snake(self):
        for i in range(3):
            self.add_segment((-SEGMENT_SIZE * i, 0))

    def add_segment(self, position):
        segment = turtle.Turtle()
        segment.shape("square")
        segment.penup()
        color = RAINBOW_COLORS[len(self.segments) % len(RAINBOW_COLORS)]
        segment.color(color)
        segment.goto(position)
        self.segments.append(segment)
        self.colors.append(color)

    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            x = self.segments[i - 1].xcor()
            y = self.segments[i - 1].ycor()
            self.segments[i].goto(x, y)
        if self.direction == UP:
            self.segments[0].sety(self.segments[0].ycor() + SEGMENT_SIZE)
        elif self.direction == DOWN:
            self.segments[0].sety(self.segments[0].ycor() - SEGMENT_SIZE)
        elif self.direction == LEFT:
            self.segments[0].setx(self.segments[0].xcor() - SEGMENT_SIZE)
        elif self.direction == RIGHT:
            self.segments[0].setx(self.segments[0].xcor() + SEGMENT_SIZE)

    def grow(self):
        tail = self.segments[-1]
        position = tail.position()
        self.color_index = (self.color_index + 1) % len(RAINBOW_COLORS)
        color = RAINBOW_COLORS[self.color_index]
        segment = turtle.Turtle()
        segment.shape("square")
        segment.penup()
        segment.color(color)
        segment.goto(position)
        self.segments.append(segment)
        self.colors.append(color)

    def set_direction(self, direction):
        # Prevent the snake from reversing
        opposites = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        if direction != opposites.get(self.direction):
            self.direction = direction

    def head_collision(self):
        x, y = self.segments[0].position()
        # Wall collision
        if not (-WIDTH//2 < x < WIDTH//2 and -HEIGHT//2 < y < HEIGHT//2):
            return True
        # Self collision
        for segment in self.segments[1:]:
            if self.segments[0].distance(segment) < SEGMENT_SIZE / 2:
                return True
        return False

    def reset(self):
        for segment in self.segments:
            segment.goto(1000, 1000)
        self.segments.clear()
        self.colors.clear()
        self.create_snake()
        self.direction = RIGHT
        self.color_index = 0

class Food(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.color("black")
        self.speed(0)
        self.refresh()

    def refresh(self):
        self.goto(random_food_position())

def main():
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("Rainbow Snake Game")
    screen.bgcolor("white")
    screen.tracer(0)

    snake = Snake()
    food = Food()

    def go_up():
        snake.set_direction(UP)
    def go_down():
        snake.set_direction(DOWN)
    def go_left():
        snake.set_direction(LEFT)
    def go_right():
        snake.set_direction(RIGHT)

    screen.listen()
    screen.onkey(go_up, "Up")
    screen.onkey(go_down, "Down")
    screen.onkey(go_left, "Left")
    screen.onkey(go_right, "Right")

    score = 0
    running = True
    while running:
        screen.update()
        time.sleep(DELAY)
        snake.move()

        # Check for food collision
        if snake.segments[0].distance(food) < SEGMENT_SIZE:
            food.refresh()
            snake.grow()
            score += 1

        # Check for collisions
        if snake.head_collision():
            time.sleep(1)
            snake.reset()
            score = 0

    screen.mainloop()

if __name__ == "__main__":
    main()
