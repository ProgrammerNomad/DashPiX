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

# Initialize Pygame
pygame.init()

# Screen settings - Fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("DashPiX Basic")

# Set larger fonts for full width display
main_font = pygame.font.SysFont("Arial", 120)  # Bigger main font
sub_font = pygame.font.SysFont("Arial", 60)   # Bigger sub font

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

def show_time_and_date():
    now = datetime.now()
    time_text = now.strftime("%H:%M:%S")
    date_text = now.strftime("%A, %B %d, %Y")
    
    # Center time horizontally
    width = screen.get_width()
    time_surface = main_font.render(time_text, True, WHITE)
    time_x = (width - time_surface.get_width()) // 2
    
    display_text(time_text, main_font, WHITE, (time_x, 50))
    display_text(date_text, sub_font, WHITE, (50, 180))

def show_greeting():
    now = datetime.now()
    hour = now.hour
    if hour < 12:
        greeting = "Good Morning!"
    elif hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    display_text(greeting, sub_font, WHITE, (50, 280))

def show_weather():
    global last_weather_update, weather_data
    current_time = time()
    
    if current_time - last_weather_update >= 600:  # Update every 10 minutes
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
        weather_text = f"{temp}°C, {weather_desc.capitalize()}"
        location_text = f"Location: {CITY_NAME}"
        
        display_text(weather_text, sub_font, WHITE, (50, 380))
        display_text(location_text, sub_font, WHITE, (50, 460))
    else:
        display_text("Weather Info Unavailable", sub_font, RED, (50, 380))

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