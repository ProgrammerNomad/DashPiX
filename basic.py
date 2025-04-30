import pygame
from time import time, sleep
import json
import requests
from datetime import datetime
import os

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
title_font = pygame.font.SysFont("Arial", 140, bold=True)  # Large title
main_font = pygame.font.SysFont("Arial", 180, bold=True)   # Extra large bold time
sub_font = pygame.font.SysFont("Arial", 60)     # Medium for other items

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
        # Combine location, symbol, and weather in one line
        weather_text = f"{CITY_NAME} — {temp}°C, {weather_desc.capitalize()}"
        center_text(weather_text, sub_font, WHITE, 650)  # Adjusted for new spacing
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