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
        # Use the next color in the sequence based on the new length
        color = RAINBOW_COLORS[len(self.segments) % len(RAINBOW_COLORS)]
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


# Custom food as a cartoon mouse
class Food(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.refresh()

    def draw_mouse(self, x, y):
        self.clear()
        # Draw head
        self.penup()
        self.goto(x, y - SEGMENT_SIZE//2)
        self.pendown()
        self.fillcolor("gray")
        self.begin_fill()
        self.circle(SEGMENT_SIZE//2)
        self.end_fill()
        # Draw left ear
        self.penup()
        self.goto(x - SEGMENT_SIZE//2, y + SEGMENT_SIZE//4)
        self.pendown()
        self.fillcolor("gray")
        self.begin_fill()
        self.circle(SEGMENT_SIZE//4)
        self.end_fill()
        # Draw right ear
        self.penup()
        self.goto(x + SEGMENT_SIZE//2, y + SEGMENT_SIZE//4)
        self.pendown()
        self.fillcolor("gray")
        self.begin_fill()
        self.circle(SEGMENT_SIZE//4)
        self.end_fill()
        # Draw nose
        self.penup()
        self.goto(x, y - SEGMENT_SIZE//2 + 2)
        self.pendown()
        self.fillcolor("pink")
        self.begin_fill()
        self.circle(SEGMENT_SIZE//10)
        self.end_fill()
        # Draw eyes
        self.penup()
        # Move eyes higher: adjust y by +SEGMENT_SIZE//8
        eye_y = y - SEGMENT_SIZE//8
        self.goto(x - SEGMENT_SIZE//6, eye_y)
        self.pendown()
        self.fillcolor("black")
        self.begin_fill()
        self.circle(SEGMENT_SIZE//20)
        self.end_fill()
        self.penup()
        self.goto(x + SEGMENT_SIZE//6, eye_y)
        self.pendown()
        self.begin_fill()
        self.circle(SEGMENT_SIZE//20)
        self.end_fill()
        self.penup()
        self.goto(x, y)
        self.penup()
        # self.showturtle()  # Keep the turtle hidden so only the drawing appears

    def refresh(self):
        x, y = random_food_position()
        self.goto(x, y)
        self.draw_mouse(x, y)

def draw_hedge_border():
    """Draw a hedge border around the play area"""
    border_drawer = turtle.Turtle()
    border_drawer.hideturtle()
    border_drawer.penup()
    border_drawer.speed(0)
    
    hedge_clump_size = SEGMENT_SIZE
    
    # Draw a dense hedge by stepping by a fraction of the clump size
    step = hedge_clump_size // 2
    
    # Top border
    for x in range(-WIDTH//2, WIDTH//2 + step, step):
        y = HEIGHT//2 - hedge_clump_size//2
        draw_bush_clump(border_drawer, x, y, hedge_clump_size)
    
    # Bottom border
    for x in range(-WIDTH//2, WIDTH//2 + step, step):
        y = -HEIGHT//2 + hedge_clump_size//2
        draw_bush_clump(border_drawer, x, y, hedge_clump_size)
    
    # Left border
    for y in range(-HEIGHT//2, HEIGHT//2 + step, step):
        x = -WIDTH//2 + hedge_clump_size//2
        draw_bush_clump(border_drawer, x, y, hedge_clump_size)
    
    # Right border
    for y in range(-HEIGHT//2, HEIGHT//2 + step, step):
        x = WIDTH//2 - hedge_clump_size//2
        draw_bush_clump(border_drawer, x, y, hedge_clump_size)

def draw_bush_clump(turtle_obj, x, y, size):
    """Draw a clump of bushes at the specified position"""
    turtle_obj.penup()
    
    # Define shades of green for a more natural look
    bush_colors = ["#228B22", "#006400", "#556B2F"] # ForestGreen, DarkGreen, DarkOliveGreen
    
    # Draw a few overlapping circles to represent a bush
    for _ in range(3):
        turtle_obj.goto(
            x + random.randint(-size//4, size//4), 
            y + random.randint(-size//4, size//4)
        )
        turtle_obj.pendown()
        # Use dot for a simple, filled circle
        turtle_obj.dot(random.randint(size//2, size), random.choice(bush_colors))
        turtle_obj.penup()

def main():
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("Rainbow Snake Game")
    screen.bgcolor("white")
    screen.tracer(0)

    snake = Snake()
    food = Food()
    
    # Draw the hedge border
    draw_hedge_border()


    def go_up():
        snake.set_direction(UP)
        snake.move()
    def go_down():
        snake.set_direction(DOWN)
        snake.move()
    def go_left():
        snake.set_direction(LEFT)
        snake.move()
    def go_right():
        snake.set_direction(RIGHT)
        snake.move()

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
