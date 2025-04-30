import pygame
import time
import json
import requests
import socket
from datetime import datetime

# Load the configuration
with open("config.json") as config_file:
    config = json.load(config_file)

# Initialize Pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("DashPiX")

# Set font
font = pygame.font.SysFont("Arial", 50)
small_font = pygame.font.SysFont("Arial", 30)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Function to display text
def display_text(text, font, color, position):
    surface = font.render(text, True, color)
    screen.blit(surface, position)

# Function to show current time and date
def show_time_and_date():
    now = datetime.now()
    time_text = now.strftime("%H:%M:%S")
    date_text = now.strftime("%A, %B %d, %Y")
    display_text(time_text, font, WHITE, (50, 50))
    if config["show_date"]:
        display_text(date_text, small_font, WHITE, (50, 120))

# Function to show greeting based on time of day
def show_greeting():
    now = datetime.now()
    hour = now.hour
    if hour < 12:
        greeting = "Good Morning!"
    elif hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    display_text(greeting, small_font, WHITE, (50, 180))

# Function to fetch and show weather
def show_weather():
    if config["show_weather"]:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={config['city']}&appid={config['api_key']}&units=metric"
            response = requests.get(url)
            data = response.json()
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"]
            weather_text = f"{temp}°C, {weather_desc.capitalize()}"
            display_text(weather_text, small_font, WHITE, (50, 250))
        except Exception as e:
            display_text("Weather Info Unavailable", small_font, RED, (50, 250))

# Function to show Wi-Fi status and IP address
def show_network_info():
    if config["show_wifi_status"]:
        try:
            ssid = "N/A"
            ip = requests.get("https://api.ipify.org").text
            display_text(f"IP: {ip}", small_font, WHITE, (50, 300))
        except:
            display_text("Network Error", small_font, RED, (50, 300))

# Function to show custom message from a file
def show_custom_message():
    if config["show_custom_message"]:
        try:
            with open("message.txt", "r") as msg_file:
                message = msg_file.read()
            display_text(message, small_font, WHITE, (50, 350))
        except FileNotFoundError:
            display_text("No Message Found", small_font, RED, (50, 350))

# Function to show system info like CPU temperature
def show_system_info():
    if config["show_cpu_temp"]:
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as temp_file:
                cpu_temp = float(temp_file.read()) / 1000
            display_text(f"CPU Temp: {cpu_temp:.1f}°C", small_font, WHITE, (50, 400))
        except:
            display_text("Error Reading CPU Temp", small_font, RED, (50, 400))

# Function to update the display
def update_display():
    screen.fill(BLACK)
    
    # Show features based on config
    if config["show_greeting"]:
        show_greeting()
    if config["show_time"]:
        show_time_and_date()
    if config["show_weather"]:
        show_weather()
    if config["show_network_info"]:
        show_network_info()
    if config["show_custom_message"]:
        show_custom_message()
    if config["show_cpu_temp"]:
        show_system_info()

    pygame.display.update()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_display()
    time.sleep(1)

pygame.quit()