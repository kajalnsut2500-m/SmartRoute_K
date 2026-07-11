# 🚦 SmartRoute — Intelligent Toll & Route Planner for India
> A full-stack Flask web application that helps users plan optimized travel routes across Indian cities based on **shortest distance**, **minimum toll cost**, or **fastest travel time**.

---

## ✨ Features
- **3 Route Preferences** — Shortest Distance, Minimum Toll, Fastest Time
- **Google Maps Integration** — live traffic-aware directions with one-click navigation
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
| **External API** | Google Maps Directions API |

---

## 📂 Project Structure

```
SmartRoute_k/
├── Toll/
│   ├── run.py              # Entry point
│   ├── __init__.py         # App factory & extensions
│   ├── routes.py           # Flask routes & API endpoints
│   ├── models.py           # SQLAlchemy DB models (User, SavedRoute)
│   ├── forms.py            # WTForms definitions
│   ├── direct_routing.py   # Core routing logic (Google Maps)
│   ├── static_data.py      # Offline fallback city matrix
│   ├── floyd_warshall.py   # Graph algorithm (offline fallback)
│   ├── map_service.py      # Google Maps API integration
│   ├── templates/          # Jinja2 HTML templates
│   └── static/             # CSS, JS, images
├── instance/               # SQLite database (auto-created)
├── .env                    # Environment variables (not committed)
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/kajalnsut2500-m/SmartRoute_K.git
cd SmartRoute_K
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the `Toll/` folder:

```env
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True
```

### 5. Run the app
```bash
cd Toll
python run.py
```

Open `http://localhost:8000` in your browser.

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GOOGLE_MAPS_API_KEY` | Recommended | For live traffic & directions |
| `SECRET_KEY` | Yes | Flask session security key |
| `FLASK_DEBUG` | No | Set `True` for development |

> **Note:** Without `GOOGLE_MAPS_API_KEY`, the app automatically falls back to static offline route data.

---

## 🧠 How It Works

1. **Login / Signup** — User creates an account (password stored as bcrypt hash)
2. **Select Cities** — Type source and destination with autocomplete suggestions
3. **Choose Preference** — Pick Shortest Distance, Minimum Toll, or Fastest Time
4. **Route Computation** — Single Google Maps API call fetches up to 3 route alternatives; best route selected based on preference
5. **View Results** — App displays distance (km), travel time (hrs), toll cost (₹), and highways used
6. **Navigate** — "Start Navigation" opens Google Maps for turn-by-turn directions
7. **Save Route** — Save any result to personal route history stored in SQLite

---

## 📸 Screenshots

### 🏠 Home Page
<img width="2600" alt="Home Page" src="https://github.com/user-attachments/assets/d9c29513-b62a-47eb-8073-ddc95d2e8077" />

### 🔐 Login & Authentication
<img width="2600" alt="Login Page" src="https://github.com/user-attachments/assets/0971725c-ad18-4799-ba67-fa852a8fb467" />

### 🗺️ Plan Your Route
<img width="2600" alt="Plan Route" src="https://github.com/user-attachments/assets/954ab6fd-fc9b-4b5e-a345-d7418e9c691d" />

### ✅ Route Results
<img width="2600" alt="Route Results" src="https://github.com/user-attachments/assets/c420429f-e1d9-464a-814d-7c81e77bb073" />

### 🗺️ Google Maps Navigation
<img width="1892" alt="Google Maps Navigation" src="https://github.com/user-attachments/assets/61d39c19-3c29-4968-9091-f6553728093e" />

### 📋 Route History
<img width="2600" alt="Route History" src="https://github.com/user-attachments/assets/cb7c23b1-8d82-4940-97d3-9c4008f026ef" />

---

## 👩‍💻 Author

**Kajal Maurya** — Full-Stack Developer, NSUT Delhi

- GitHub: [@kajalnsut2500-m](https://github.com/kajalnsut2500-m)
- LinkedIn: [linkedin.com/in/kajalmaurya-603114381](https://linkedin.com/in/kajalmaurya-603114381)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
