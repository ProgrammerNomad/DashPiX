import pygame
from time import time, sleep
import json
import requests
from datetime import datetime
import os
from PIL import Image
from io import BytesIO

try:
    from env import OPENWEATHER_API_KEY, CITY_NAME
except ImportError as e:
    print("Please create env.py file from env.example.py template")
    exit(1)

from update_config import update_config

# Update config with any new options
update_config()

# Load the configuration
with open("config.json") as config_file:
    config = json.load(config_file)

# Initialize Pygame
pygame.init()

# Screen settings - Fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("DashPiX Basic")

# Update fonts for better hierarchy
title_font = pygame.font.SysFont("Arial", 80, bold=True)   # Smaller title size
main_font = pygame.font.SysFont("Arial", 180, bold=True)   # Keep time size the same
sub_font = pygame.font.SysFont("Arial", 60)     # Keep other text size the same

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (25, 25, 25)
RED = (255, 0, 0)

# Global variables
last_weather_update = 0
weather_data = None

def display_text(text, font, color, position):
    filtered_text = ''.join(char for char in text if ord(char) <= 0xFFFF)
    surface = font.render(filtered_text, True, color)
    screen.blit(surface, position)

def center_text(text, font, color, y_position):
    surface = font.render(text, True, color)
    width = screen.get_width()
    x = (width - surface.get_width()) // 2
    display_text(text, font, color, (x, y_position))

def show_time_and_date():
    now = datetime.now()
    
    # Title with spacing
    center_text("DashPiX", title_font, WHITE, 50)
    
    # Time based on config with increased spacing
    if config.get("clock_style", "24h") == "12h":
        time_text = now.strftime("%I:%M:%S %p")
    else:
        time_text = now.strftime("%H:%M:%S")
    center_text(time_text, main_font, WHITE, 250)  # Increased Y position for more space
    
    # Date with consistent spacing
    date_text = now.strftime("%A, %B %d, %Y")
    center_text(date_text, sub_font, WHITE, 450)  # Increased spacing after time

def show_greeting():
    now = datetime.now()
    hour = now.hour
    if hour < 12:
        greeting = "Good Morning!"
    elif hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    center_text(greeting, sub_font, WHITE, 550)  # Adjusted for new spacing

def get_weather_icon(icon_code, size=(50, 50)):
    try:
        url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        response = requests.get(url)
        if response.status_code == 200:
            # Convert bytes to pygame image
            image_data = BytesIO(response.content)
            pil_image = Image.open(image_data)
            pil_image = pil_image.resize(size)
            mode = pil_image.mode
            size = pil_image.size
            data = pil_image.tobytes()
            
            py_image = pygame.image.fromstring(data, size, mode)
            return py_image
    except Exception as e:
        print(f"Error loading weather icon: {e}")
    return None

def show_weather():
    global last_weather_update, weather_data
    current_time = time()
    
    if current_time - last_weather_update >= config.get("weather_update_frequency", 600):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(url)
            weather_data = response.json()
            last_weather_update = current_time
        except Exception:
            weather_data = None
    
    if weather_data:
        temp = weather_data["main"]["temp"]
        weather_desc = weather_data["weather"][0]["description"]
        icon_code = weather_data["weather"][0]["icon"]
        
        # Get screen width for centering
        width = screen.get_width()
        
        # Create temperature text
        temp_text = f"{CITY_NAME} - {temp}°C"
        temp_surface = sub_font.render(temp_text, True, WHITE)
        
        # Create description text
        desc_text = f", {weather_desc.capitalize()}"
        desc_surface = sub_font.render(desc_text, True, WHITE)
        
        # Get weather icon
        icon = get_weather_icon(icon_code)
        
        # Calculate total width for centering
        total_width = temp_surface.get_width()
        if icon:
            total_width += icon.get_width() + 10  # 10px spacing
        total_width += desc_surface.get_width()
        
        # Calculate starting x position for center alignment
        x = (width - total_width) // 2
        y = 650  # Keep existing y position
        
        # Draw temperature
        screen.blit(temp_surface, (x, y))
        x += temp_surface.get_width() + 5  # 5px spacing
        
        # Draw icon
        if icon:
            screen.blit(icon, (x, y))
            x += icon.get_width() + 5  # 5px spacing
        
        # Draw description
        screen.blit(desc_surface, (x, y))
    else:
        center_text(f"{CITY_NAME} — Weather Info Unavailable", sub_font, RED, 650)

def update_display():
    screen.fill(DARK_GREY)
    show_time_and_date()
    show_greeting()
    show_weather()
    pygame.display.update()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    update_display()
    sleep(1)

pygame.quit()