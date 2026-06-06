# 🚦 Smart Route — Intelligent Toll & Route Planner

> A full-stack web application that helps users plan optimized travel routes across Indian cities based on **shortest distance**, **minimum toll cost**, or **fastest travel time**.

---

## 📸 Screenshots

### 🏠 Home Page
![Home Page](screenshots/Screenshot%202026-06-06%20at%206.43.33%20PM.png)
![Home Features](screenshots/Screenshot%202026-06-06%20at%206.43.22%20PM.png)

### 🔐 Login & Authentication
![Login Page](screenshots/Screenshot%202026-06-06%20at%206.43.44%20PM.png)

### 🗺️ Plan Your Route
![Route Planner](screenshots/Screenshot%202026-06-06%20at%206.45.08%20PM.png)
![Route Options](screenshots/Screenshot%202026-06-06%20at%206.45.43%20PM.png)

### ✅ Route Results

**Shortest Distance** — Delhi → Mumbai
![Shortest Distance Result](screenshots/Screenshot%202026-06-06%20at%206.55.02%20PM.png)

**Fastest Route** — Delhi → Mumbai
![Fastest Route Result](screenshots/Screenshot%202026-06-06%20at%206.54.28%20PM.png)

### ⏳ Loading State 🐹
![Loading](screenshots/Screenshot%202026-06-06%20at%206.51.38%20PM.png)

### ℹ️ About Page
![About Page](screenshots/Screenshot%202026-06-06%20at%206.55.11%20PM.png)

---

## ✨ Features

- **Multi-Criteria Route Optimization** — choose between shortest distance, minimum toll, or fastest time
- **Floyd-Warshall Algorithm** — all-pairs shortest path for efficient graph computation
- **Google Maps Integration** — live map view and turn-by-turn navigation
- **User Authentication** — secure login/signup with Flask-Login and WTForms
- **Responsive UI** — clean, mobile-friendly interface with smooth interactions
- **Loading Animation** — visual feedback while route is being calculated

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) |
| **Backend** | Python Flask, SQLAlchemy ORM, Flask-Login, WTForms |
| **Database** | SQLite |
| **Algorithm** | Floyd-Warshall, Graph Theory |
| **API** | Google Maps API |

---

## 📂 Project Structure

```
SmartRoute_K/
├── Toll/
│   ├── run.py              # Entry point
│   ├── __init__.py         # App factory
│   ├── routes.py           # Flask routes & API endpoints
│   ├── routes_api.py       # API logic
│   ├── models.py           # Database models
│   ├── forms.py            # WTForms definitions
│   ├── floyd_warshall.py   # Core routing algorithm
│   ├── city_network.py     # Graph/city data
│   ├── map_service.py      # Google Maps integration
│   ├── templates/          # Jinja2 HTML templates
│   └── static/             # CSS, JS, Images
├── instance/               # SQLite DB instance
├── .env                    # Environment variables
└── README.md
```

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/kajalnsut2500-m/SmartRoute_K.git
cd SmartRoute_K/SmartRoute_k

# Activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Add your Google Maps API key to .env

# Run the app
cd Toll
python run.py
```

Then open `http://localhost:8000` in your browser.

---

## 📋 Prerequisites

- Python 3.7+
- Google Maps API Key
- Modern web browser

---

## 🧠 How It Works

1. User logs in and selects source & destination city
2. The app builds a weighted graph of Indian cities and highways
3. **Floyd-Warshall algorithm** computes optimal paths for all three criteria simultaneously
4. Results display distance (km), time (hours), toll cost (₹), and highway path
5. **"Start Navigation"** opens Google Maps for turn-by-turn directions

---

## 👩‍💻 Author

**Kajal Maurya** — Full-Stack Developer, NSUT Delhi

- GitHub: [@kajalnsut2500-m](https://github.com/kajalnsut2500-m)
- LinkedIn: [linkedin.com/in/kajalmaurya-603114381](https://linkedin.com/in/kajalmaurya-603114381)

---

## 📄 License

This project is licensed under the MIT License.
