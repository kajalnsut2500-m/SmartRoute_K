# 🚦 Smart Route — Intelligent Toll & Route Planner

> A full-stack web application that helps users plan optimized travel routes across Indian cities based on **shortest distance**, **minimum toll cost**, or **fastest travel time**.

---

## 📸 Screenshots

### 🏠 Home Page
<img width="1469" height="791" alt="Image" src="https://github.com/user-attachments/assets/fd8af9ae-f457-4bdd-8240-e5d6fc0f84fe" /><img width="1469" height="791" alt="Image" src="https://github.com/user-attachments/assets/c4bc59ab-4af3-4fef-9ac2-828acb301d94" />

### 🔐 Login & Authentication
<img width="1469" height="791" alt="Image" src="https://github.com/user-attachments/assets/4342a431-d057-4d81-89ef-f2fe52a69d2e" />



### 🗺️ Plan Your Route

<img width="1469" height="791" alt="Image" src="https://github.com/user-attachments/assets/4289a139-8e0d-4cd7-aaeb-80f9201d00aa" />

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

<<<<<<< Updated upstream
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
=======
## 📂 Project Structure  
SmartRoute/
├── app.py # Main Flask app
├── templates/ # Jinja2 templates (HTML pages)
├── static/ # CSS, JS, Images
├── models.py # Database models
├── routes.py # Flask routes & API endpoints
├── algorithms/ # Floyd-Warshall, graph utilities
├── users.db # SQLite database
└── requirements.txt # Project dependencies

## 🚀 How to Run
1. Clone the repo:
   ```bash
   git clone https://github.com/kajalnsut2500-m/SmartRoute_k.git
   cd SmartRoute_k
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream

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
=======
python app.py
>>>>>>> Stashed changes
