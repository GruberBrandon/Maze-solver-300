import pygame
from button import Button
from maze import Maze
import sys

# Initializes the pygame module
pygame.init()

# dictionary which stores constants for each of the colours in the rgb format
colours = {"BLACK": (0, 0, 0), "WHITE": (255, 255, 255), "RED": (255, 0, 0), "GREEN": (0, 255, 0),
           "YELLOW": (255, 215, 0), "blue": (89, 224, 214), "pastel_blue": (154, 224, 219),
           "pastel_green": (164, 249, 189), "Tardis_Blue": (0, 59, 111),
           "GREY": (220, 220, 220), "WALL_GREY": (46, 48, 48), "TRANS": (1, 1, 1), "BloodOrange": (255, 169, 104)}

# size and width of the window are stored for easy access.
screen_width = 720
screen_height = 610

# creates the window
screen = pygame.display.set_mode((screen_width, screen_height))

# Changing program title and setting program icon.
pygame.display.set_caption("Maze Solver 3000")
icon = pygame.image.load('Maze.PNG')
pygame.display.set_icon(icon)


def button_pressed():
    print("Button pressed")


# boolean variable which is used to track when a user clicks a button on the program.
click = False


# Function which acts as the entry point into the program by containing all of the main menu functionality.
# Contains functionality to access other screens in the program.
def main_menu():
    # Two buttons are created which allow the user to access the maze screen and the tutorial screen.
    to_maze_button = Button("To Maze", (310, 500), maze_menu, colours["Tardis_Blue"], colours["BLACK"],
                            (100, 50), "AgencyFB", 30)
    to_tutorial_button = Button("To Tutorials", (430, 500), tutorial_menu, colours["Tardis_Blue"], colours["BLACK"],
                                (120, 50), "AgencyFB", 30)

    main_menu_buttons = [to_maze_button, to_tutorial_button]  # Buttons are stored in an array for easy iteration later.

    # Game loop.
    while True:
        screen.fill(colours["BLACK"])  # sets background colour to black
        image = pygame.image.load('Title.PNG')  # variable which holds the image of the title.
        screen.blit(image, (35, 200))  # adds the title image to the screen.

        # Creates the buttons on the screen.
        to_maze_button.draw(screen)
        to_tutorial_button.draw(screen)
        pygame.display.flip()  # update window to show changes.

        # Program checks for events such as key presses and mouse clicks and responds with the correct function.
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for button in main_menu_buttons:
                    if button.rect.collidepoint(pos):
                        button.call_back()
            if event.type == pygame.QUIT:  # When the user clicks the red X in the top right corner the program closes.
                sys.exit()


# Function which contains the functionality of the Maze screen.
def maze_menu():
    maze = Maze(screen, 15)  # creates maze object.

    # Buttons for maze screen are declared.
    generate_button = Button("Generate", (671, 25), maze.generate, colours["pastel_blue"], colours["BLACK"], (100, 50),
                             "AgencyFB", 30)
    solve_button = Button("Solve", (671, 85), maze.route, colours["pastel_blue"], colours["BLACK"], (100, 50),
                          "AgencyFB",
                          30)
    maze_size_up_button = Button("+", (708, 145), maze.size_up, colours["pastel_blue"], colours["BLACK"], (25, 50),
                                 "AgencyFB", 30)
    maze_size_down_button = Button("-", (633, 145), maze.size_down, colours["pastel_blue"], colours["BLACK"], (25, 50),
                                   "AgencyFB", 30)
    dfs = Button("DFS", (671, 265), maze.algorithm_update_dfs, colours["BloodOrange"], colours["BLACK"],
                 (100, 50),
                 "AgencyFB", 30)
    bfs = Button("BFS", (671, 325), maze.algorithm_update_bfs, colours["BloodOrange"],
                 colours["BLACK"],
                 (100, 50), "AgencyFB", 30)

    # Maze buttons are stored in an array for when the application checks for events.
    maze_buttons = [generate_button, solve_button, maze_size_up_button, maze_size_down_button,
                    dfs, bfs]
    running = True
    screen.fill(colours["BLACK"])  # Changes background colour to remove any of the icons and buttons from the main menu
    while running:
        # All buttons are drawn on to the screen.
        for button in maze_buttons:
            button.draw(screen)

        # The text showing the current maze size is displayed on screen.
        pygame.draw.rect(screen, colours["BLACK"], ((646, 120), (50, 50)))
        string_size = str(maze.maze_size)
        font = pygame.font.SysFont('AgencyFB', 35)
        text = font.render(string_size, False, colours["WHITE"])
        screen.blit(text, [660, 135])

        pygame.display.flip()

        # Button presses are constantly checked for.
        for event in pygame.event.get():
            # Checks if the user exits the program.
            if event.type == pygame.QUIT:
                sys.exit()

            # Checks if user clicks any button.
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for button in maze_buttons:
                    if button.rect.collidepoint(pos):
                        button.call_back()

            # Checks if user presses the escape key in which case returns to the main menu screen.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


# Function which stores the functionality of the Tutorial screen.
def tutorial_menu():
    screen.fill(colours["BLACK"])
    image = pygame.image.load(
        'development_info.PNG')  # variable which holds the image informing the user that this screen is just a place holder for now.
    screen.blit(image, (65, 200))  # adds the image to the screen.

    pygame.display.flip()
    running = True
    while running:

        # Button presses are constantly checked for.
        for event in pygame.event.get():
            # Checks if the user exits the program.
            if event.type == pygame.QUIT:
                sys.exit()

            # Checks if user presses the escape key in which case returns to the main menu screen.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


main_menu()
