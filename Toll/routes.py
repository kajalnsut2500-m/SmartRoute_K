from Toll import app,render_template,db
from Toll.forms import Inputform,RegisterForm,LoginForm
from Toll.models import UserInput
from flask import flash,request,redirect,url_for
from Toll.floyd_warshall import floyd_warshall,reconstruct_path
import numpy as np
from flask_login import login_user, logout_user, login_required,current_user
from Toll import bcrypt
from sqlalchemy.exc import IntegrityError,OperationalError
from sqlalchemy import func 
import re 
import logging
from Toll import gmaps
from .map_service import get_route_details
from Toll.build_matrix import build_matrix
from Toll.direct_routing import get_direct_route, should_use_direct_routing
from flask import jsonify

logger = logging.getLogger(__name__)




@app.route('/')
@app.route('/home')
def home_page():
    return render_template('route_options.html')

@app.route('/options')
def route_options():
    return render_template('route_options.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/technology')
def technology_page():
    return render_template('technology.html')
@app.route('/get_the_route', methods=['GET', 'POST'])
@login_required
def SmartRoute():
    form = Inputform()
    show_result = False
    route = []
    cost = None
    source = destination = None
    total_toll = 0
    preference = ''

    if form.validate_on_submit():
        source = form.source.data.strip().title()
        destination = form.destination.data.strip().title()
        preference = form.preference.data
        
        # Use direct routing (1 API call vs 28+ with Floyd-Warshall)
        if should_use_direct_routing(source, destination):
            direct_route_data = get_direct_route(source, destination, preference)
            
            if direct_route_data:
                route = direct_route_data['route']
                cost = direct_route_data.get('distance_km', 0) if preference == 'distance' else direct_route_data.get('duration_hours', 0) if preference == 'time' else direct_route_data.get('toll_cost', 0)
                total_toll = direct_route_data.get('toll_cost', 0)
                highway_path = direct_route_data.get('highways', [])
                flash(f"✅ Direct route via {direct_route_data.get('route_summary', 'optimal path')}", "success")
            else:
                flash("⚠️ Using offline estimates", "warning")
                from Toll.static_data import get_matrix
                matrix_data, cities = get_matrix(preference)
                if source in cities and destination in cities:
                    src_idx = cities.index(source)
                    dest_idx = cities.index(destination)
                    cost = matrix_data[src_idx][dest_idx]
                    route = [source, destination]
                    total_toll = get_matrix('toll')[0][src_idx][dest_idx] if preference != 'toll' else cost
                    highway_path = ["NH48"]
                else:
                    flash("Route not found", "danger")
                    return redirect(url_for('SmartRoute'))
        else:
            # Fallback to Floyd-Warshall
            flash("⚠️ Using offline estimates", "warning")
            matrix_data, cities = build_matrix(preference)
            
            if source not in cities or destination not in cities:
                flash("Invalid Source or Destination", "danger")
                return redirect(url_for('SmartRoute'))
                
            fw = floyd_warshall(matrix_data)
            src_idx = cities.index(source)
            dest_idx = cities.index(destination)
            
            dist_matrix, next_matrix = fw
            cost = dist_matrix[src_idx][dest_idx]
            
            if cost >= float('inf'):
                flash("No path found between the selected cities.", "danger")
                return redirect(url_for('SmartRoute'))
                
            route = reconstruct_path(src_idx, dest_idx, next_matrix, cities)
        
            # Handle toll calculation for Floyd-Warshall fallback
            total_toll = 0
            highway_path = []
            if preference == 'toll':
                total_toll = cost
            else:
                toll_matrix, _ = build_matrix('toll')
                for i in range(len(route) - 1):
                    from_idx = cities.index(route[i])
                    to_idx = cities.index(route[i + 1])
                    if from_idx < len(toll_matrix) and to_idx < len(toll_matrix[from_idx]):
                        segment_toll = toll_matrix[from_idx][to_idx]
                        if segment_toll != float('inf'):
                            total_toll += segment_toll
            
            # Get highway names for Floyd-Warshall route
            if len(route) >= 2:
                directions = get_route_steps(route[0], route[-1])
                if directions and 'legs' in directions:
                    for leg in directions['legs']:
                        if 'steps' in leg:
                            for step in leg['steps']:
                                if 'html_instructions' in step:
                                    highway = extract_highway_name(step['html_instructions'])
                                    if highway and highway not in highway_path:
                                        highway_path.append(highway)
            
        # Redirect to results page
        return render_template(
            'results.html',
            route=route,
            highway_path=highway_path if 'highway_path' in locals() else [],
            cost=cost,
            source=source,
            destination=destination,
            total_toll=total_toll,
            preference=preference
        )

    return render_template('input.html', form=form)







def extract_road_name(html_instruction):
    """Extract road names from Google's HTML instructions"""
    clean_text = re.sub('<[^<]+?>', '', html_instruction)  # Remove HTML tags
    road_match = re.search(r'(?:Take|Continue on|Merge onto)\s+(.*?)\s+(?:toward|to|via)', clean_text)
    return road_match.group(1).strip() if road_match else clean_text

def extract_highway_name(html_instruction):
    """Extract highway names like NH48, NH44, etc. from Google Maps instructions"""
    # Remove HTML tags
    clean_text = re.sub('<[^<]+?>', '', html_instruction)
    
    # Look for highway patterns: NH, SH, AH followed by numbers
    highway_patterns = [
        r'\b(NH\s*\d+[A-Z]?)\b',  # National Highway: NH48, NH44
        r'\b(SH\s*\d+[A-Z]?)\b',  # State Highway: SH1, SH2
        r'\b(AH\s*\d+[A-Z]?)\b',  # Asian Highway: AH1, AH2
        r'\b(Mumbai[- ]Pune\s*Expressway)\b',  # Named expressways
        r'\b(Delhi[- ]Mumbai\s*Expressway)\b',
        r'\b(Yamuna\s*Expressway)\b',
        r'\b(Agra[- ]Lucknow\s*Expressway)\b'
    ]
    
    for pattern in highway_patterns:
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None

@login_required
def get_route_steps(origin, destination):
    try:
        if not gmaps:
            logger.error("Google Maps client not initialized")
            return None
            
        directions = gmaps.directions(
            origin=origin,
            destination=destination,
            mode="driving",
            alternatives=True,
            departure_time="now"
        )
        
        if not directions:
            logger.warning("No directions found")
            return None
        
        return directions[0] if directions else None
    
    except Exception as e:
        logger.error(f"Google Maps API Error: {e}")
        return None





@app.route('/Register',methods=['GET','POST'])
def Register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # Create and add new user (rely on database constraints)
            hashed_pw = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
            new_user = UserInput(
                username=form.username.data, 
                email_address=form.email_address.data,
                password_hash=hashed_pw
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login_page'))
            
        except IntegrityError as e:
            db.session.rollback()
            if "username" in str(e):
                flash('Username already taken', 'danger')
            elif "email_address" in str(e):
                flash('Email already registered', 'danger')
            else:
                flash('Registration error occurred', 'danger')
            return redirect(url_for('Register_page'))
            
    return render_template('register.html', form=form)





@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            attempted_user = UserInput.query.filter_by(username=form.username.data).first()
            if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
                login_user(attempted_user)
                flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
                return redirect(url_for('SmartRoute'))
            else:
                flash('Username and password are not matched!!', category='danger')
        except Exception as e:
            logger.error(f"Login error: {e}")
            flash('Login error occurred', 'danger')
    return render_template('login.html', form=form)
        
@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('login_page'))

@app.teardown_appcontext
def shutdown_session(exception=None):
    if exception:
        logger.error(f"Database error: {exception}")
    db.session.remove()

@app.route('/api/city-search')
@login_required
def city_search():
    q = request.args.get('q', '').strip().title()
    # Use hardcoded city list to avoid API calls
    cities = ["Mumbai", "Delhi", "Bangalore", "Pune", "Chennai", "Kolkata", "Hyderabad", "Ahmedabad"]
    matches = [c for c in cities if q.lower() in c.lower()]
    return jsonify(matches)
