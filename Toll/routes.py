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
from flask import jsonify

logger = logging.getLogger(__name__)




@app.route('/')
@app.route('/home')
@login_required
def home_page():
    return render_template('home.html')
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
        logger.debug(f"Source: {source}")
        preference = form.preference.data
        logger.debug(f"Preference: {preference}")

        matrix_data, cities = build_matrix(preference)
        logger.debug(f"Matrix data sample: {matrix_data[0][:3] if len(matrix_data) > 0 else 'Empty'}")
        logger.debug(f"Cities from matrix: {cities}")
        
        destination = form.destination.data.strip().title()

        if source not in cities or destination not in cities:
            flash("Invalid Source or Destination", "danger")
            return redirect(url_for('SmartRoute'))
        fw = floyd_warshall(matrix_data)

        src_idx = cities.index(source)
        dest_idx = cities.index(destination)
        
        # Get shortest path using Floyd-Warshall result
        dist_matrix, next_matrix = fw
        cost = dist_matrix[src_idx][dest_idx]
        
        if cost >= float('inf'):
            flash("No path found between the selected cities.", "danger")
            return redirect(url_for('SmartRoute'))
            
        route = reconstruct_path(src_idx, dest_idx, next_matrix, cities)
        
        # Get detailed route steps from Google Maps
        detailed_steps = []
        if len(route) >= 2:
            directions = get_route_steps(route[0], route[-1])
            if directions and 'legs' in directions:
                for leg in directions['legs']:
                    if 'steps' in leg:
                        for step in leg['steps']:
                            if 'html_instructions' in step:
                                road_info = extract_road_name(step['html_instructions'])
                                detailed_steps.append(road_info)
        
        # Calculate toll based on distance if not toll preference
        total_toll = 0
        if preference == 'toll':
            total_toll = cost  # Already calculated toll cost
        else:
            # Estimate toll based on distance (avoid extra API calls)
            for i in range(len(route) - 1):
                from_idx = cities.index(route[i])
                to_idx = cities.index(route[i + 1])
                # Use distance from existing matrix to estimate toll
                if not np.isinf(matrix_data[from_idx][to_idx]):
                    total_toll += matrix_data[from_idx][to_idx] * 2.5  # ₹2.5 per km estimate
            
        show_result = True

    return render_template(
        'input.html',
        show_result=show_result,
        form=form,
        route=route,
        detailed_steps=detailed_steps if 'detailed_steps' in locals() else [],
        cost=cost,
        source=source,
        destination=destination,
        total_toll=total_toll,
        preference=form.preference.data if form.preference.data else ''
    )




@app.route('/show_all_details')
@login_required
def Show_all_results():
    return render_template('show_all_results.html')


def extract_road_name(html_instruction):
    """Extract road names from Google's HTML instructions"""
    clean_text = re.sub('<[^<]+?>', '', html_instruction)  # Remove HTML tags
    road_match = re.search(r'(?:Take|Continue on|Merge onto)\s+(.*?)\s+(?:toward|to|via)', clean_text)
    return road_match.group(1).strip() if road_match else clean_text

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
