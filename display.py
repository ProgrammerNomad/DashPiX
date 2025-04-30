import pygame
from time import time, sleep  # Import specific functions from time
import json
import requests
import socket
from datetime import datetime
import psutil  # Add to imports
import os
from PIL import Image
import calendar

try:
    from env import OPENWEATHER_API_KEY, CITY_NAME
    from update_config import update_config, validate_config  # Add validate_config import
except ImportError as e:
    print(f"Import error: {str(e)}")
    print("Please create env.py file from env.example.py template")
    exit(1)

# Update config with any new options
update_config()

# Load the configuration
with open("config.json") as config_file:
    config = json.load(config_file)
    # Override API key and city from env.py
    config["api_key"] = OPENWEATHER_API_KEY
    config["city"] = CITY_NAME

# After loading config
if not validate_config(config):
    print("Error: Invalid configuration")
    exit(1)

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
DARK_GREY = (25, 25, 25)  # Very dark grey for dark mode
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Add after other global variables
last_weather_update = 0
weather_data = None
calendar.setfirstweekday(calendar.MONDAY)  # Start week from Monday

# Function to display text
def display_text(text, font, color, position):
    # Filter out characters above \uFFFF
    filtered_text = ''.join(char for char in text if ord(char) <= 0xFFFF)
    surface = font.render(filtered_text, True, color)
    screen.blit(surface, position)

# Add clock style support
def show_time_and_date():
    now = datetime.now()
    clock_style = config.get("clock_style", "24h")
    clock_format = config.get("clock_format", "HH:MM:SS")
    
    if clock_style == "12h":
        time_text = now.strftime("%I:%M:%S %p")
    else:
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

# Update the show_weather function
def show_weather():
    global last_weather_update, weather_data
    if config["show_weather"]:
        current_time = time()
        update_frequency = config.get("weather_update_frequency", 600)  # Default 10 minutes
        
        # Update weather data if enough time has passed
        if current_time - last_weather_update >= update_frequency:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={config['city']}&appid={config['api_key']}&units=metric"
                response = requests.get(url)
                weather_data = response.json()
                last_weather_update = current_time
            except Exception as e:
                weather_data = None
        
        # Display weather data if available
        if weather_data:
            temp = weather_data["main"]["temp"]
            weather_desc = weather_data["weather"][0]["description"]
            weather_code = weather_data["weather"][0]["icon"]
            
            # Show weather info
            weather_text = f"{temp}°C, {weather_desc.capitalize()}"
            display_text(weather_text, small_font, WHITE, (50, 250))
            
            # Show weather icon
            show_weather_icon(weather_code, (300, 250))
            
            # Show location if enabled
            if config.get("show_location", False):
                location_text = f"Location: {config['city']}"
                display_text(location_text, small_font, WHITE, (50, 280))
        else:
            display_text("Weather Info Unavailable", small_font, RED, (50, 250))
            if config.get("show_location", False):
                display_text(f"Location: {config['city']}", small_font, WHITE, (50, 280))

# Function to show weather icon
def show_weather_icon(weather_code, position):
    try:
        # OpenWeatherMap icon URL
        icon_url = f"http://openweathermap.org/img/wn/{weather_code}@2x.png"
        response = requests.get(icon_url, timeout=5)  # Add timeout
        if response.status_code == 200:
            # Save temporarily and load with pygame
            with open("temp_icon.png", "wb") as f:
                f.write(response.content)
            
            icon = pygame.image.load("temp_icon.png")
            icon = pygame.transform.scale(icon, (50, 50))
            screen.blit(icon, position)
            
            # Clean up temporary file
            os.remove("temp_icon.png")
    except requests.RequestException as e:
        print(f"Weather icon download error: {str(e)}")
    except Exception as e:
        print(f"Error loading weather icon: {str(e)}")

# Add better network error handling
def show_network_info():
    if config["show_wifi_status"]:
        try:
            ip = requests.get("https://api.ipify.org", timeout=5).text
            display_text(f"IP: {ip}", small_font, WHITE, (50, 300))
        except requests.RequestException as e:
            print(f"Network error: {str(e)}")
            display_text("Network Error", small_font, RED, (50, 300))
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            display_text("Error", small_font, RED, (50, 300))

# Function to show custom message from a file
def show_custom_message():
    if config["show_custom_message"]:
        try:
            with open("message.txt", "r", encoding='utf-8') as msg_file:
                message_lines = msg_file.read().splitlines()
            
            y_position = 350
            for line in message_lines:
                # Skip empty lines
                if line.strip():
                    display_text(line, small_font, WHITE, (50, y_position))
                    y_position += 30  # Increment position for next line
        except FileNotFoundError:
            display_text("No Message Found", small_font, RED, (50, 350))
        except Exception as e:
            display_text(f"Error: {str(e)}", small_font, RED, (50, 350))

# Function to show system info like CPU temperature, RAM, and storage usage
def show_system_info():
    if config["show_system_info"]:
        try:
            # RAM Usage with warning threshold
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            ram_warning = config.get("system_warnings", {}).get("ram_warning", 90)
            ram_color = RED if ram_percent > ram_warning else WHITE
            
            # Storage with warning threshold
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            storage_warning = config.get("system_warnings", {}).get("storage_warning", 90)
            storage_color = RED if disk_percent > storage_warning else WHITE
            
            # Display with warning colors
            display_text(f"RAM: {ram_percent}%", small_font, ram_color, (50, 430))
            display_text(f"Storage: {disk_percent}%", small_font, storage_color, (50, 460))
        except Exception as e:
            print(f"Error showing system info: {str(e)}")
            display_text("Error Reading System Info", small_font, RED, (50, 400))

# Function to scroll text if it exceeds a certain width
def scroll_text(text, font, color, position, max_width=300):
    if not hasattr(scroll_text, "offset"):
        scroll_text.offset = 0
        
    if config.get("text_effects", {}).get("scroll_long_text", False):
        surface = font.render(text, True, color)
        if surface.get_width() > max_width:
            scroll_text.offset = (scroll_text.offset + 1) % surface.get_width()
            screen.blit(surface, (position[0] - scroll_text.offset, position[1]))
        else:
            screen.blit(surface, position)
    else:
        display_text(text, font, color, position)

# Add new function for calendar display
def show_calendar():
    now = datetime.now()
    cal = calendar.monthcalendar(now.year, now.month)
    month_name = now.strftime("%B %Y")
    
    # Get screen dimensions
    screen_width = screen.get_width()
    
    # Calendar position (right side)
    cal_x = screen_width - 400  # 400 pixels from right edge
    cal_y = 50  # Same top alignment as time
    
    # Display month name
    display_text(month_name, font, WHITE, (cal_x, cal_y))
    
    # Display weekday headers
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(weekdays):
        display_text(day, small_font, GREY, (cal_x + i*50, cal_y + 60))
    
    # Display calendar days
    for week_num, week in enumerate(cal):
        for day_num, day in enumerate(week):
            if day != 0:
                # Highlight current day
                color = RED if day == now.day else WHITE
                display_text(str(day), small_font, color, 
                           (cal_x + day_num*50, cal_y + 90 + week_num*30))

# Function to update the display
def update_display():
    # Set background color based on config
    if config.get("background_style", "dark") == "dark":
        screen.fill(DARK_GREY)
    else:
        screen.fill(BLACK)
    
    # Left side content (existing features)
    if config["show_greeting"]:
        show_greeting()
    if config["show_time"]:
        show_time_and_date()
    if config["show_weather"]:
        show_weather()
        
    # Right side content (calendar)
    show_calendar()
    
    # Bottom half content (hardware info)
    if config["show_network_info"]:
        show_network_info()
    if config["show_custom_message"]:
        show_custom_message()
    if config["show_cpu_temp"] or config["show_system_info"]:
        show_system_info()

    pygame.display.update()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Exit on pressing Esc key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    update_display()
    sleep(1)  # Use sleep() directly

pygame.quit()