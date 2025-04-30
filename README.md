## DashPiX – Universal Smart Display for Raspberry Pi

**DashPiX** is a free and open-source smart dashboard designed for the Raspberry Pi. It displays real-time **time**, **weather**, and **notifications** on any HDMI screen, making it ideal for homes, schools, offices, or public spaces like villages and community halls.

---

### ✨ Features
- 🕰️ Fullscreen clock with live time updates
- 🌤️ Weather data from OpenWeatherMap with icon support
- 📅 Current date and day of the week
- 🎉 Time-based greeting (Good Morning, Good Afternoon, Good Evening)
- 💬 Custom message support (displayed from a `message.txt` file)
- 📶 Wi-Fi status and IP address display
- 🌡️ CPU temperature display (Raspberry Pi monitoring)
- 🔧 Easily configurable via `config.json`
- ⌨️ Simple exit with Escape key

---

### 📦 Requirements
- Raspberry Pi with HDMI output
- Python 3
- Pygame, Requests, Pillow

---

### 🛠️ Installation

1. **Install Dependencies**:
   ```bash
   sudo apt update && sudo apt install python3-pip
   pip3 install pygame requests pillow
   ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/ProgrammerNomad/DashPiX.git
   cd DashPiX
   ```

3. **Set Up Configuration Files**:
   - Create config file from example:
     ```bash
     cp config.json.example config.json
     ```
   - Create environment file from example:
     ```bash
     cp env.example.py env.py
     ```
   - Edit `env.py` and add your OpenWeatherMap API key and city name:
     ```python
     OPENWEATHER_API_KEY = "your_openweathermap_api_key"
     CITY_NAME = "YourCityName"
     ```

4. **Configure Display Settings**:
   Edit the `config.json` file to enable or disable features by toggling the boolean values:
   ```json
   {
     "show_time": true,
     "show_date": true,
     "show_greeting": true,
     "show_weather": true,
     "show_location": true,
     "show_news": false,
     "show_wifi_status": false,
     "show_ip_address": false,
     "show_custom_message": true,
     "show_events": false,
     "show_cpu_temp": false,
     "background_style": "light"
   }
   ```

5. **Create `message.txt`** (optional):
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

6. **Run It**:
   ```bash
   python3 display.py
   ```
   To exit the application:
   - Press `Esc` key to close the display
   - Or use `Ctrl+C` in the terminal
   
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
   git pull origin master
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
- **show_news**: Set to `true` to show news headlines (RSS feed).
- **show_wifi_status**: Set to `true` to show Wi-Fi status.
- **show_ip_address**: Set to `true` to display the IP address.
- **show_custom_message**: Set to `true` to display a message from the `message.txt` file.
- **show_events**: Set to `true` to show upcoming events (manual configuration).
- **show_cpu_temp**: Set to `true` to show the CPU temperature of the Raspberry Pi.
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

**Let the world see more, with less.** — DashPiX

---
````