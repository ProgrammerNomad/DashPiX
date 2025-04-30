## DashPiX – Universal Smart Display for Raspberry Pi

**DashPiX** is a free and open-source smart dashboard designed for the Raspberry Pi. It offers both a full-featured display (`display.py`) and a simplified basic version (`basic.py`) for different use cases.

---

### ✨ Features

#### Full Version (display.py)
- 🕰️ Fullscreen clock with live time updates (12/24h format)
- 🌤️ Weather data from OpenWeatherMap
- 📅 Current date and calendar display
- 🎉 Time-based greeting
- 💬 Custom message support
- 📊 System monitoring (RAM, Storage)
- 🎨 Dark/Light mode support
- ⌨️ Simple exit with Escape key

#### Basic Version (basic.py)
- 🕰️ Large centered clock display
- 📅 Centered date display
- 👋 Centered greeting
- 🌤️ Single-line weather with location
- 🎨 Clean, minimal interface

---

### 📦 Requirements
- Raspberry Pi with HDMI output
- Python 3
- Pygame, Requests, Pillow, psutil

---

### 🛠️ Installation

1. **Install Dependencies**:
   ```bash
   sudo apt update && sudo apt install python3-pip
   pip3 install pygame requests pillow psutil
   ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/ProgrammerNomad/DashPiX.git
   cd DashPiX
   ```

3. **Set Up Configuration Files**:
   ```bash
   # Copy example files
   copy config.json.example config.json
   copy env.example.py env.py
   
   # Update configuration with new options
   python update_config.py
   ```

4. **Configure Display Settings**:
   Edit the `config.json` file:
   ```json
   {
     "show_time": true,
     "show_date": true,
     "show_greeting": true,
     "show_weather": true,
     "show_location": true,
     "show_system_info": true,
     "clock_style": "24h",
     "background_style": "dark",
     "weather_update_frequency": 600,
     "system_warnings": {
       "ram_warning": 90,
       "storage_warning": 90
     }
   }
   ```

5. **Run the Display**:
   For full version:
   ```bash
   python3 display.py
   ```
   For basic version:
   ```bash
   python3 basic.py
   ```

6. **Create `message.txt`** (optional):
   - You can create a file named `message.txt` in the same directory as `display.py`.
   - Write custom messages that you want to display. For example:
     ```txt
     📢 Community Announcement!

     🌟 Join us for the Village Festival this weekend!
     🗓 Date: May 5, 2025
     📍 Location: Village Square

     🎉 Free Entry | Food, Music & Fun!

     For more details, visit www.villagefestival.com
     ```

7. **Optional: Run on Boot**:
   To run the display on boot, add the following line to your crontab:
   ```bash
   crontab -e
   ```
   Then add this line:
   ```bash
   @reboot python3 /home/pi/DashPiX/display.py
   ```
   > Note: When running on boot, you can still exit using the `Esc` key.

> Note: 
> - The `.example` files serve as templates and should not be modified directly
> - Your personal `config.json` and `env.py` files will be ignored by git
> - Keep the example files up to date with the latest configuration options

---

### 🔄 Updating DashPiX

To update your local DashPiX installation while preserving your settings:

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git remote add origin https://github.com/ProgrammerNomad/DashPiX.git
   ```

2. **Backup your configuration files**:
   ```bash
   # On Windows
   copy env.py env.backup.py
   copy config.json config.backup.json
   
   # On Raspberry Pi
   cp env.py env.backup.py
   cp config.json config.backup.json
   ```

3. **Pull the latest changes**:
   ```bash
   git pull origin main
   ```

4. **Restore your configuration**:
   ```bash
   # On Windows
   copy env.backup.py env.py
   copy config.backup.json config.json
   
   # On Raspberry Pi
   cp env.backup.py env.py
   cp config.backup.json config.json
   ```

5. **Check for new configuration options**:
   ```bash
   # On Windows
   fc env.example.py env.py
   fc config.json.example config.json
   
   # On Raspberry Pi
   diff env.example.py env.py
   diff config.json.example config.json
   ```
   If there are new options, manually add them to your configuration files.

> Note: 
> - Always backup your configuration files before updating
> - Check the changelog before updating
> - Never commit your personal `env.py` and `config.json` files

---

### 📱 Customization
You can toggle or change the display settings at any time by editing the `config.json` file. Here's a breakdown of the settings:

- **show_time**: Set to `true` to display the time.
- **show_date**: Set to `true` to display the current date.
- **show_greeting**: Set to `true` to display a greeting based on the time of day.
- **show_weather**: Set to `true` to display weather information.
- **show_location**: Set to `true` to display the current city and weather description.
- **show_system_info**: Set to `true` to display system monitoring information (RAM, Storage).
- **clock_style**: Choose between "12h" or "24h" format.
- **weather_update_frequency**: Set weather update interval in seconds (default: 600).
- **system_warnings**: Configure warning thresholds for RAM and storage.
- **background_style**: Set to `light` or `dark` to choose the background style.

> Note: OpenWeatherMap API key and city name are now configured in `env.py` for better security.

---

### 🚀 Coming Soon
- RSS Feed-based news
- Local sensor integration (temperature, humidity)
- Calendar or prayer times
- Enhanced theming support

---

### 🧑‍💻 Contributors
Made with ❤️ by [@ProgrammerNomad](https://github.com/ProgrammerNomad)

---

### 📜 License
This project is licensed under the **MIT License**. You can use, modify, and distribute it freely.

---

### 🔗 Related Projects & Inspiration
- OpenWeatherMap API
- Raspberry Pi digital signage projects

> Feel free to fork, contribute, or share your custom DashPiX setups!

---

### 📦 Dependencies Explanation

#### psutil
- System monitoring and resource management
- RAM usage tracking
- Storage usage monitoring
- CPU temperature reading
- Process and system utilities

#### Pillow (PIL)
- Image processing and manipulation
- Format conversion for weather icons
- Image resizing and optimization
- Support for various image formats

To install these dependencies:
```bash
pip install psutil pillow
```

**Let the world see more, with less.** — DashPiX

---
