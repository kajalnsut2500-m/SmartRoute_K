# 🚦 SmartRoute — Intelligent Toll & Route Planner for India

> A full-stack Flask web application that helps users plan optimized travel routes across Indian cities based on **shortest distance**, **minimum toll cost**, or **fastest travel time**.

---

## ✨ Features

- **3 Route Preferences** — Shortest Distance, Minimum Toll, Fastest Time
- **Floyd-Warshall Algorithm** — computes optimal paths across all city pairs simultaneously
- **Google Maps Integration** — live map view and one-click turn-by-turn navigation
- **User Authentication** — secure signup/login with bcrypt password hashing
- **Save Route** — authenticated users can save routes to a personal history (SQLite DB)
- **City Autocomplete** — smart dropdown suggestions for source and destination
- **Offline Fallback** — static graph data kicks in when Google Maps API is unavailable
- **Responsive UI** — clean, mobile-friendly interface with loading animations

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Google Maps](https://img.shields.io/badge/Google%20Maps%20API-4285F4?style=flat&logo=google-maps&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)

| Layer | Technologies |
|---|---|
| **Backend** | Python, Flask, Flask-Login, SQLAlchemy ORM, bcrypt |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Jinja2 |
| **Database** | SQLite |
| **Algorithm** | Floyd-Warshall, Weighted Graph Theory |
| **External API** | Google Maps JavaScript API & Directions API |

---

## 📂 Project Structure

```
SmartRoute_k/
├── Toll/
│   ├── run.py              # Entry point
│   ├── __init__.py         # App factory & extensions
│   ├── routes.py           # Flask routes & API endpoints
│   ├── routes_api.py       # Route computation logic
│   ├── models.py           # SQLAlchemy DB models (User, SavedRoute)
│   ├── forms.py            # WTForms definitions
│   ├── floyd_warshall.py   # Core routing algorithm
│   ├── city_network.py     # Indian city graph data
│   ├── map_service.py      # Google Maps API integration
│   ├── templates/          # Jinja2 HTML templates
│   └── static/             # CSS, JS, images
├── instance/               # SQLite database (auto-created)
├── screenshots/            # App screenshots
├── .env                    # Environment variables (not committed)
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/kajalnsut2500-m/SmartRoute_k.git
cd SmartRoute_k
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root (see section below).

### 5. Run the app

```bash
cd Toll
python run.py
```

Open `http://localhost:8000` in your browser.

---

## 🔑 Environment Variables

Create a `.env` file in the project root with the following keys:

```env
# Google Maps API key (required for live map and directions)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# Flask secret key (any long random string)
SECRET_KEY=your_secret_key_here

# Optional: set to 'development' or 'production'
FLASK_ENV=development
```

> **Note:** Without `GOOGLE_MAPS_API_KEY`, the app falls back to static offline route data automatically.

---

## 🧠 How It Works

1. **Login / Signup** — User creates an account (password stored as bcrypt hash).
2. **Select Cities** — Type source and destination; city autocomplete narrows suggestions.
3. **Choose Preference** — Pick Shortest Distance, Minimum Toll, or Fastest Time.
4. **Graph Computation** — Floyd-Warshall runs on a weighted graph of Indian cities and highways, computing optimal paths for all three criteria at once.
5. **View Results** — App displays distance (km), travel time (hrs), toll cost (₹), and the highway path taken.
6. **Navigate** — "Start Navigation" opens Google Maps with the exact route for turn-by-turn directions.
7. **Save Route** — Logged-in users can save any result to their personal route history stored in SQLite.

---

## 📸 Screenshots

### 🏠 Home Page
<img width="1469" alt="Home Page" src="https://github.com/user-attachments/assets/fd8af9ae-f457-4bdd-8240-e5d6fc0f84fe" />

### 🔐 Login & Authentication
<img width="1469" alt="Login Page" src="https://github.com/user-attachments/assets/4342a431-d057-4d81-89ef-f2fe52a69d2e" />

### 🗺️ Plan Your Route
<img width="1469" alt="Route Planner" src="https://github.com/user-attachments/assets/4289a139-8e0d-4cd7-aaeb-80f9201d00aa" />

### ✅ Route Results
**Shortest Distance** — Delhi → Mumbai
![Shortest Distance Result](screenshots/Screenshot%202026-06-06%20at%206.55.02%20PM.png)

**Fastest Route** — Delhi → Mumbai
![Fastest Route Result](screenshots/Screenshot%202026-06-06%20at%206.54.28%20PM.png)

---

## 👩‍💻 Author

**Kajal Maurya** — Full-Stack Developer, NSUT Delhi

- GitHub: [@kajalnsut2500-m](https://github.com/kajalnsut2500-m)
- LinkedIn: [linkedin.com/in/kajalmaurya-603114381](https://linkedin.com/in/kajalmaurya-603114381)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
