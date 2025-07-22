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
INITIAL_SNAKE_LENGTH = 3

# Directions
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
STOPPED = "stop"

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
        for i in range(INITIAL_SNAKE_LENGTH):
            self.add_segment((-SEGMENT_SIZE * i, 0))

    def add_segment(self, position):
        segment = turtle.Turtle()
        segment.penup()
        color = RAINBOW_COLORS[len(self.segments) % len(RAINBOW_COLORS)]
        segment.color(color)
        segment.goto(position)
        segment.shape("square")
        segment.shapesize(stretch_wid=1, stretch_len=1)
        self.segments.append(segment)
        self.colors.append(color)

    def update_segment_styles(self):
        total = len(self.segments)
        for idx, segment in enumerate(self.segments):
            color = self.colors[idx]
            # Head: oval, slightly larger, oriented in direction of travel
            if idx == 0:
                segment.shape("circle")
                segment.shapesize(stretch_wid=1.1, stretch_len=1.5)
                segment.setheading(self._head_direction())
                segment.color("black", color)
                continue
            # Determine direction from previous segment
            prev = self.segments[idx - 1]
            dx = segment.xcor() - prev.xcor()
            dy = segment.ycor() - prev.ycor()
            
            # Determine if this is neck or tail
            is_neck = idx < max(2, total // 3)
            is_tail = idx > total - 4
            
            # Stretch perpendicular to this segment's direction of travel
            if abs(dx) > abs(dy):
                # Horizontal movement: thin vertically for neck/tail
                if is_neck:
                    segment.shape("square")
                    segment.shapesize(stretch_wid=0.6, stretch_len=1.0)
                    segment.setheading(0 if dx > 0 else 180)
                elif is_tail:
                    segment.shape("square")
                    taper = max(0.3, 1 - 0.2 * (idx - (total - 4)))
                    segment.shapesize(stretch_wid=taper, stretch_len=1.0)
                    segment.setheading(0 if dx > 0 else 180)
                else:
                    segment.shape("square")
                    segment.shapesize(stretch_wid=1.0, stretch_len=1.0)
                    segment.setheading(0 if dx > 0 else 180)
            elif abs(dy) > abs(dx):
                # Vertical movement: thin horizontally for neck/tail
                if is_neck:
                    segment.shape("square")
                    segment.shapesize(stretch_wid=0.6, stretch_len=1.0)
                    segment.setheading(90 if dy > 0 else 270)
                elif is_tail:
                    segment.shape("square")
                    taper = max(0.3, 1 - 0.2 * (idx - (total - 4)))
                    segment.shapesize(stretch_wid=taper, stretch_len=1.0)
                    segment.setheading(90 if dy > 0 else 270)
                else:
                    segment.shape("square")
                    segment.shapesize(stretch_wid=1.0, stretch_len=1.0)
                    segment.setheading(90 if dy > 0 else 270)
            else:
                # Diagonal or no movement: default to normal
                segment.shape("square")
                segment.shapesize(stretch_wid=1.0, stretch_len=1.0)
                segment.setheading(0)
            segment.color(color)

    def _head_direction(self):
        # Returns heading angle for head based on current direction
        if self.direction == UP:
            return 90
        elif self.direction == DOWN:
            return 270
        elif self.direction == LEFT:
            return 180
        else:
            return 0

    def move(self):
        if self.direction == STOPPED:
            return
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
        self.update_segment_styles()

    def grow(self):
        tail = self.segments[-1]
        position = tail.position()
        self.add_segment(position)
        self.update_segment_styles()

    def dodge(self, dodge_direction):
        """Instantly move the entire snake's body in a given direction."""
        dx, dy = 0, 0
        if dodge_direction == UP:
            dy = SEGMENT_SIZE
        elif dodge_direction == DOWN:
            dy = -SEGMENT_SIZE
        elif dodge_direction == LEFT:
            dx = -SEGMENT_SIZE
        elif dodge_direction == RIGHT:
            dx = SEGMENT_SIZE
        for segment in self.segments:
            segment.goto(segment.xcor() + dx, segment.ycor() + dy)
        self.update_segment_styles()

    def change_direction(self, new_direction):
        opposites = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        # If moving, and the new direction is opposite, stop.
        if self.direction != STOPPED and new_direction == opposites.get(self.direction):
            self.direction = STOPPED
        # If stopped, any direction starts it.
        elif self.direction == STOPPED:
            self.direction = new_direction
        # Otherwise, just change direction as long as it's not a 180.
        elif new_direction != opposites.get(self.direction):
            self.direction = new_direction

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
        self.update_segment_styles()
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

def draw_background_grass(num_clumps=150):
    """Draw random clumps of grass on the background."""
    grass_drawer = turtle.Turtle()
    grass_drawer.hideturtle()
    grass_drawer.penup()
    grass_drawer.speed(0)
    grass_drawer.color("mediumseagreen")

    for _ in range(num_clumps):
        # Pick a random spot for the clump
        clump_x = random.randint(-WIDTH//2, WIDTH//2)
        clump_y = random.randint(-HEIGHT//2, HEIGHT//2)
        
        # Draw a few blades in the clump
        for _ in range(random.randint(3, 6)):
            grass_drawer.goto(
                clump_x + random.randint(-10, 10),
                clump_y + random.randint(-10, 10)
            )
            grass_drawer.pendown()
            grass_drawer.setheading(random.randint(80, 100)) # Pointing mostly up
            grass_drawer.forward(random.randint(10, 15)) # Blade length
            grass_drawer.penup()

def main():
    # Score display
    score_display = turtle.Turtle()
    score_display.hideturtle()
    score_display.penup()
    score_display.goto(0, HEIGHT//2 - 40)
    score_display.color("black")

    def update_score():
        score_display.clear()
        score_display.write(f"Score: {len(snake.segments) - INITIAL_SNAKE_LENGTH}", align="center", font=("Arial", 18, "bold"))
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("Rainbow Snake Game")
    screen.bgcolor("lightgreen")
    screen.tracer(0)

    # Draw background details
    draw_background_grass()

    snake = Snake()
    food = Food()
    
    # Draw the hedge border
    draw_hedge_border()


    def go_up():
        snake.change_direction(UP)
        last_action['type'] = 'move'
    def go_down():
        snake.change_direction(DOWN)
        last_action['type'] = 'move'
    def go_left():
        snake.change_direction(LEFT)
        last_action['type'] = 'move'
    def go_right():
        snake.change_direction(RIGHT)
        last_action['type'] = 'move'

    # Track the last action: 'move' or 'dodge'
    last_action = {'type': 'move'}

    def dodge_up():
        snake.dodge(UP)
        last_action['type'] = 'dodge'
    def dodge_down():
        snake.dodge(DOWN)
        last_action['type'] = 'dodge'
    def dodge_left():
        snake.dodge(LEFT)
        last_action['type'] = 'dodge'
    def dodge_right():
        snake.dodge(RIGHT)
        last_action['type'] = 'dodge'

    screen.listen()
    screen.onkey(go_up, "Up")
    screen.onkey(go_down, "Down")
    screen.onkey(go_left, "Left")
    screen.onkey(go_right, "Right")
    screen.onkey(dodge_up, "w")
    screen.onkey(dodge_down, "s")
    screen.onkey(dodge_left, "a")
    screen.onkey(dodge_right, "d")

    update_score()
    running = True
    while running:
        # Only allow eating if last action was a normal move
        if last_action['type'] == 'move':
            head_x, head_y = snake.segments[0].position()
            food_x, food_y = food.position()
            if int(head_x) == int(food_x) and int(head_y) == int(food_y):
                food.refresh()
                snake.grow()
                update_score()

        snake.move()

        screen.update()
        time.sleep(DELAY)

        # Check for collisions
        if snake.head_collision():
            time.sleep(1)
            snake.reset()
            update_score()

    screen.mainloop()

if __name__ == "__main__":
    main()
