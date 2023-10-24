

import pygame
import time

# Class for a text input box
class TextInputBox:
    def __init__(self, rect, font, placeholder):
        # Initialize the text input box
        self.rect = rect  # The rectangular area for the input box
        self.font = font  # The font used for text rendering
        self.placeholder = placeholder  # Placeholder text displayed when the input box is empty
        self.text = ''  # The current text entered by the user
        self.show_placeholder = True  # Controls the visibility of the placeholder text
        self.cursor_visible = True  # Controls the visibility of the text cursor
        self.cursor_flash_time = 0.5  # Time interval for cursor blinking
        self.last_cursor_toggle = time.time()  # Keeps track of time for cursor blinking
        self.input_active = False  # Indicates if the input box is currently active for text entry

    def handle_event(self, event):
        # Handle user input events for the text input box
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Clicking inside the box activates it
                self.input_active = True
                self.show_placeholder = False
            else:
                # Clicking outside the box deactivates it
                self.input_active = False
                self.show_placeholder = bool(not self.text)

        if self.input_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Handle Enter key (e.g., process input, clear text)
                    print(self.text)  # Replace with your processing logic
                    self.text = ''  # Clear the input
                elif event.key == pygame.K_BACKSPACE:
                    # Handle Backspace key (delete a character)
                    self.text = self.text[:-1]
                else:
                    if self.font.size(self.text + event.unicode)[0] <= self.rect.width - 10:
                        # Prevent text from overflowing the box
                        self.text += event.unicode

    def update(self):
        # Update the input box, e.g., cursor blinking
        if self.input_active:
            if time.time() - self.last_cursor_toggle > self.cursor_flash_time:
                self.cursor_visible = not self.cursor_visible
                self.last_cursor_toggle = time.time()

    def draw(self, screen):
        # Draw the input box and its contents
        pygame.draw.rect(screen, (255, 255, 255), self.rect)  # Draw the input box background
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Draw a border around the input box

        if self.input_active:
            if self.cursor_visible:
                # Draw the text cursor
                cursor_x = self.rect.x + 5 + self.font.size(self.text)[0]
                cursor_y = self.rect.y + 5
                pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + self.rect.height - 10), 2)

        if not self.text:
            # Draw the placeholder text when no text is entered
            placeholder_surface = self.font.render(self.placeholder, True, (128, 128, 128))
            placeholder_x = self.rect.x + 5
            placeholder_y = self.rect.y + (self.rect.height - placeholder_surface.get_height()) // 2
            screen.blit(placeholder_surface, (placeholder_x, placeholder_y))
        else:
            # Draw the entered text
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            text_x = self.rect.x + 5
            text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
            screen.blit(text_surface, (text_x, text_y))

# Class for creating a button
class Button:
    def __init__(self, rect, font, text, background_color, text_color):
        self.rect = rect  # Rectangular area for the button
        self.font = font  # Font for the button text
        self.text = text  # Button text
        self.background_color = background_color  # Button background color
        self.text_color = text_color  # Text color

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Draw a border around the button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_x = self.rect.x + (self.rect.width - text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

# Initialize Pygame
pygame.init()

# Define screen dimensions
screen_width = 1920
screen_height = 1020

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the window title
pygame.display.set_caption("Eagle Defender")

# Define the light blue color (in RGB format)
light_blue = (135, 206, 235)

# Define the font
font = pygame.font.Font(None, 32)

# Create the text input boxes with increased vertical separation and rightward displacement
username_input = TextInputBox(pygame.Rect(screen_width // 2 + 250, screen_height // 2 - 80, 400, 40), font, "Nombre de Usuario")
password_input = TextInputBox(pygame.Rect(screen_width // 2 + 250, screen_height // 2 + 20, 400, 40), font, "Contraseña")

# Adjust the x-coordinates to shift the text input boxes to the right
username_input.rect.x += 50
password_input.rect.x += 50

# Create the "Ingresar" button right below the text input boxes and of the same size
button_font = pygame.font.Font(None, 36)
button_width, button_height = 400, 40  # Same size as the text input boxes
ingresar_button = Button(pygame.Rect(screen_width // 2 + 300, screen_height // 2 + 120, button_width, button_height), button_font, "Ingresar", (192, 192, 192), (0, 0, 0))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        username_input.handle_event(event)
        password_input.handle_event(event)

    screen.fill(light_blue)

    # Update and draw the input boxes
    username_input.update()
    username_input.draw(screen)

    password_input.update()
    password_input.draw(screen)

    # Draw the "Ingresar" button
    ingresar_button.draw(screen)

    pygame.display.flip()

# Quit Pygame
pygame.quit()