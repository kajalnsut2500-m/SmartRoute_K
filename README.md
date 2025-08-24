# 🚦 Smart Route – Intelligent Toll and Route Planner  

A **Full-Stack Web Application** built with **Python Flask** that helps users plan intelligent travel routes across Indian cities.  
Users can optimize routes based on **shortest distance**, **minimum toll cost**, or **fastest travel time**.  

---

## ✨ Features  
- **Multi-Criteria Route Optimization**  
  - Shortest distance  
  - Minimum toll cost  
  - Fastest travel time  
- **Floyd-Warshall Algorithm** for all-pairs shortest path  
- **Google Maps API Integration** for live traffic & directions  
- **Secure User Authentication** with Flask-Login and WTForms  
- **Modern UI/UX** with animations, responsive layouts, and smooth interactions  
- **Performance Optimized** (200ms API response, 60% fewer API calls)  

---

## 🛠 Tech Stack  
**Frontend:** HTML5, CSS3, JavaScript (ES6+)  
**Backend:** Python Flask, SQLAlchemy ORM, Flask-Login, WTForms  
**Database:** SQLite  
**APIs:** Google Maps API  
**Algorithms:** Floyd-Warshall, Graph Theory, Caching mechanisms  

---

## 📂 Project Structure  
```
SmartRoute_k/
├── app.py              # Main Flask app
├── templates/          # Jinja2 templates (HTML pages)
├── static/            # CSS, JS, Images
├── models.py          # Database models
├── routes.py          # Flask routes & API endpoints
├── algorithms/        # Floyd-Warshall, graph utilities
├── users.db          # SQLite database
└── requirements.txt  # Project dependencies
```

## 🚀 Quick Start
```bash
git clone https://github.com/kajalnsut2500-m/SmartRoute_k.git
cd SmartRoute_k
pip install -r requirements.txt
python app.py
```
Then visit `http://localhost:5000`

## 📋 Prerequisites
- Python 3.7+
- Modern web browser

## 👨💻 Author
**Kajal Maurya**
- GitHub: [@kajalnsut2500-m](https://github.com/kajalnsut2500-m)

## 📄 License
This project is licensed under the MIT License.