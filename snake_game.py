import turtle
import time
import random

# Rainbow colors
RAINBOW_COLORS = [
    "green", "blue", "indigo", "violet", "red", "orange", "yellow"
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
        self.pending_direction = None  # Store the last direction input this frame

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
            # Head: oval, size varies based on snake length
            if idx == 0:
                segment.shape("circle")
                # Scale head size based on total segments
                if total <= 3:
                    # Very small head for short snake
                    segment.shapesize(stretch_wid=0.6, stretch_len=0.9)
                elif total == 4:
                    # Slightly larger head for 4 segments
                    segment.shapesize(stretch_wid=0.75, stretch_len=1.05)
                elif total == 5:
                    # Medium head for 5 segments
                    segment.shapesize(stretch_wid=0.9, stretch_len=1.2)
                else:
                    # Normal/large head for long snake
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
        # Process the last direction input from this frame
        if self.pending_direction is not None:
            opposites = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
            new_direction = self.pending_direction
            self.pending_direction = None  # Clear the pending direction
            
            # If moving, and the new direction is opposite, stop.
            if self.direction != STOPPED and new_direction == opposites.get(self.direction):
                self.direction = STOPPED
            # If stopped, any direction starts it.
            elif self.direction == STOPPED:
                self.direction = new_direction
            # Otherwise, just change direction as long as it's not a 180.
            elif new_direction != opposites.get(self.direction):
                self.direction = new_direction
        
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
        
        # Check if any segment would go out of bounds
        for segment in self.segments:
            new_x = segment.xcor() + dx
            new_y = segment.ycor() + dy
            # Check if the new position would be outside the playing area
            if not (-WIDTH//2 < new_x < WIDTH//2 and -HEIGHT//2 < new_y < HEIGHT//2):
                # Block the dodge if any segment would go out of bounds
                return
        
        # If all segments would stay in bounds, execute the dodge
        for segment in self.segments:
            segment.goto(segment.xcor() + dx, segment.ycor() + dy)
        self.update_segment_styles()

    def change_direction(self, new_direction):
        # Store the most recent direction input for processing in the next frame
        self.pending_direction = new_direction

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
        self.pending_direction = None


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


class Predator(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.spawn()

    def draw_cat(self, x, y):
        self.clear()
        # Draw body
        self.penup()
        self.goto(x, y - SEGMENT_SIZE//2)
        self.pendown()
        self.fillcolor("orange")
        self.begin_fill()
        self.circle(SEGMENT_SIZE//2)
        self.end_fill()
        # Draw left ear (pointed)
        self.penup()
        self.goto(x - SEGMENT_SIZE//3, y + SEGMENT_SIZE//3)
        self.pendown()
        self.fillcolor("orange")
        self.begin_fill()
        for _ in range(3):
            self.forward(SEGMENT_SIZE//3)
            self.left(120)
        self.end_fill()
        # Draw right ear (pointed)
        self.penup()
        self.goto(x + SEGMENT_SIZE//3, y + SEGMENT_SIZE//3)
        self.pendown()
        self.fillcolor("orange")
        self.begin_fill()
        for _ in range(3):
            self.forward(SEGMENT_SIZE//3)
            self.left(120)
        self.end_fill()
        # Draw eyes (angry looking)
        self.penup()
        eye_y = y - SEGMENT_SIZE//8
        self.goto(x - SEGMENT_SIZE//6, eye_y)
        self.pendown()
        self.fillcolor("red")
        self.begin_fill()
        self.circle(SEGMENT_SIZE//15)
        self.end_fill()
        self.penup()
        self.goto(x + SEGMENT_SIZE//6, eye_y)
        self.pendown()
        self.begin_fill()
        self.circle(SEGMENT_SIZE//15)
        self.end_fill()
        # Draw nose
        self.penup()
        self.goto(x, y - SEGMENT_SIZE//3)
        self.pendown()
        self.fillcolor("black")
        self.begin_fill()
        self.circle(SEGMENT_SIZE//12)
        self.end_fill()
        self.penup()

    def spawn(self):
        # Spawn predator at a random position away from center
        x = random.randint(-WIDTH//2 + SEGMENT_SIZE*2, WIDTH//2 - SEGMENT_SIZE*2)
        y = random.randint(-HEIGHT//2 + SEGMENT_SIZE*2, HEIGHT//2 - SEGMENT_SIZE*2)
        # Snap to grid
        x -= x % SEGMENT_SIZE
        y -= y % SEGMENT_SIZE
        self.goto(x, y)
        self.draw_cat(x, y)

    def move_towards_snake(self, snake_head_pos):
        # Simple AI: move towards snake head
        current_x, current_y = self.position()
        snake_x, snake_y = snake_head_pos
        
        # Calculate direction
        dx = snake_x - current_x
        dy = snake_y - current_y
        
        # If already at snake position, don't move
        if dx == 0 and dy == 0:
            return
        
        # Move one step at a time on the grid
        move_x, move_y = 0, 0
        if abs(dx) > abs(dy):
            # Move horizontally
            if dx > 0:
                move_x = SEGMENT_SIZE
            elif dx < 0:
                move_x = -SEGMENT_SIZE
        else:
            # Move vertically
            if dy > 0:
                move_y = SEGMENT_SIZE
            elif dy < 0:
                move_y = -SEGMENT_SIZE
        
        new_x = current_x + move_x
        new_y = current_y + move_y
        
        # Check bounds (consistent with snake collision detection)
        if -WIDTH//2 < new_x < WIDTH//2 and -HEIGHT//2 < new_y < HEIGHT//2:
            self.goto(new_x, new_y)
            self.draw_cat(new_x, new_y)

    def collides_with_snake(self, snake):
        # Check if predator caught the snake head
        predator_pos = self.position()
        snake_head_pos = snake.segments[0].position()
        distance = ((predator_pos[0] - snake_head_pos[0])**2 + 
                   (predator_pos[1] - snake_head_pos[1])**2)**0.5
        return distance < SEGMENT_SIZE

    def reset(self):
        self.spawn()

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
    predator = Predator()
    
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
    frame_count = 0  # Track frames for predator movement
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
        
        # Move predator every 2 frames (slower than snake)
        frame_count += 1
        if frame_count % 2 == 0:
            predator.move_towards_snake(snake.segments[0].position())
        
        # Check if predator caught the snake
        if predator.collides_with_snake(snake):
            time.sleep(1)
            snake.reset()
            predator.reset()
            update_score()

        screen.update()
        time.sleep(DELAY)

        # Check for collisions
        if snake.head_collision():
            time.sleep(1)
            snake.reset()
            predator.reset()
            update_score()

    screen.mainloop()

if __name__ == "__main__":
    main()
