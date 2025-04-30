# DashPiX – Universal Smart Display for Raspberry Pi

**DashPiX** is a free and open-source smart dashboard designed for the Raspberry Pi. It displays real-time **time**, **weather**, and **notifications** on any HDMI screen, making it ideal for homes, schools, offices, or public spaces like villages and community halls.

---

## ✨ Features
- 🕒 Fullscreen clock with live time updates
- ☀️ Weather data from OpenWeatherMap with icon support
- 🔔 Modular notifications (upcoming)
- 🌐 Lightweight, runs on any Raspberry Pi model with HDMI
- 🌟 Minimal setup and fully customizable

---

## 📚 How It Works
DashPiX runs a Python script using `pygame` to draw fullscreen widgets on your display. The data (time, weather) is fetched live from the internet. Icons and fonts are rendered cleanly for easy reading from a distance.

---

## 📂 Installation

### 1. Install Dependencies
```bash
sudo apt update && sudo apt install python3-pip
pip3 install pygame requests pillow
```

### 2. Clone the Repository
```bash
git clone https://github.com/ProgrammerNomad/DashPiX.git
cd DashPiX
```

### 3. Set Your API Key and City
Edit `display.py`:
```python
API_KEY = 'your_openweathermap_api_key'
CITY = 'YourCityName'
```

### 4. Run It
```bash
python3 display.py
```

### 5. Optional: Run on Boot
```bash
crontab -e
```
Add this line:
```
@reboot python3 /home/pi/DashPiX/display.py
```

---

## 🚀 Coming Soon
- Notification system (email, local files, MQTT)
- Local sensor integration (temperature, humidity)
- Calendar or prayer times
- Theming support

---

## 📍 Use Cases
- Smart home clock and weather panel
- Village/community information screen
- Office entrance display
- School or temple digital notice board

---

## 👤 Contributors
Made with ❤️ by [@ProgrammerNomad](https://github.com/ProgrammerNomad)

---

## 📄 License
This project is licensed under the **MIT License**. You can use, modify, and distribute it freely.

---

## 🔗 Related Projects & Inspiration
- OpenWeatherMap API
- Raspberry Pi digital signage projects

> Feel free to fork, contribute, or share your custom DashPiX setups!

---

**Let the world see more, with less.** — DashPiX
