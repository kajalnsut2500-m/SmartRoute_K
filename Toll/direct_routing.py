# Direct routing using Google Directions API - bypasses Floyd-Warshall
# Single API call instead of 28+ calls

from Toll import gmaps
import logging
import re

logger = logging.getLogger(__name__)

def get_direct_route(source, destination, preference='distance'):
    """
    Get direct route using single Google Directions API call
    
    Args:
        source (str): Starting city
        destination (str): Destination city  
        preference (str): 'distance', 'time', or 'toll'
    
    Returns:
        dict: Complete route data from single API call
    """
    if not gmaps:
        logger.error("Google Maps client not initialized")
        return None
    
    try:
        # Map preferences to Google Directions API parameters
        avoid_params = []
        if preference == 'toll':
            avoid_params = ['tolls']
        
        # Single API call - gets everything we need
        directions = gmaps.directions(
            origin=f"{source}, India",
            destination=f"{destination}, India", 
            mode="driving",
            avoid=avoid_params if avoid_params else None,
            departure_time='now',
            traffic_model='best_guess',
            alternatives=True
        )
        
        if not directions:
            return None
        
        # Get the best route based on preference
        best_route = directions[0]
        if len(directions) > 1 and preference == 'time':
            # Choose fastest route if multiple available
            best_route = min(directions, key=lambda r: r['legs'][0].get('duration_in_traffic', r['legs'][0]['duration'])['value'])
        elif len(directions) > 1 and preference == 'distance':
            # Choose shortest route
            best_route = min(directions, key=lambda r: r['legs'][0]['distance']['value'])
        
        leg = best_route['legs'][0]
        
        # Extract all data from single API response
        distance_km = leg['distance']['value'] / 1000
        duration_hours = leg['duration']['value'] / 3600
        
        # Use traffic-aware time if available
        if 'duration_in_traffic' in leg:
            duration_hours = leg['duration_in_traffic']['value'] / 3600
        
        # Extract highways and calculate realistic toll
        highways = []
        for step in leg['steps']:
            highway = extract_highway_from_step(step)
            if highway and highway not in highways:
                highways.append(highway)
        
        # Calculate realistic toll based on actual route
        toll_cost = calculate_route_toll(distance_km, highways, best_route.get('summary', ''))
        
        return {
            'route': [source, destination],
            'distance_km': distance_km,
            'duration_hours': duration_hours,
            'toll_cost': toll_cost,
            'highways': highways,
            'route_summary': best_route.get('summary', ''),
            'is_direct': True,
            'api_calls_used': 1,  # vs 28+ with Floyd-Warshall
            'data_source': 'Google Directions API'
        }
        
    except Exception as e:
        logger.error(f"Direct route error: {e}")
        return None

def extract_highway_from_step(step):
    """Extract highway name from route step"""
    if 'html_instructions' not in step:
        return None
    
    instruction = step['html_instructions']
    clean_text = re.sub('<[^<]+?>', '', instruction)
    
    # Highway patterns for India
    patterns = [
        r'\b(NH\s*\d+[A-Z]?)\b',     # NH48, NH44
        r'\b(NE\s*\d+)\b',           # NE4 (National Expressway)
        r'\b(SH\s*\d+)\b',           # State highways
        r'\b([A-Za-z\s]+-[A-Za-z\s]+\s*(?:Expressway|Highway))\b'  # Named highways
    ]
    
    for pattern in patterns:
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None

def calculate_route_toll(distance_km, highways, route_summary):
    """
    Calculate realistic toll based on actual route characteristics
    
    Args:
        distance_km (float): Route distance
        highways (list): Highways used
        route_summary (str): Route summary from Google
    
    Returns:
        float: Realistic toll in INR
    """
    # Base toll rates (INR per 100km)
    rates = {
        'expressway': 200,  # Mumbai-Pune Expressway, etc.
        'nh_major': 120,    # NH48, NH44 (major national highways)
        'nh_minor': 80,     # Other national highways
        'sh': 50,           # State highways
        'default': 90       # Default rate
    }
    
    # Determine route type from highways and summary
    rate = rates['default']
    
    # Check for expressways first (highest toll)
    if any('expressway' in h.lower() for h in highways) or 'expressway' in route_summary.lower():
        rate = rates['expressway']
    # Major national highways
    elif any(h.startswith('NH 4') or h.startswith('NH 8') for h in highways):
        rate = rates['nh_major']
    # Other national highways
    elif any(h.startswith('NH') for h in highways):
        rate = rates['nh_minor']
    # State highways
    elif any(h.startswith('SH') for h in highways):
        rate = rates['sh']
    
    # Calculate base toll
    base_toll = (distance_km / 100) * rate
    
    # Add toll plaza charges (estimated 1 plaza per 60km)
    plaza_count = max(1, int(distance_km / 60))
    plaza_charges = plaza_count * 45  # Average ₹45 per plaza
    
    total_toll = base_toll + plaza_charges
    
    # Apply realistic bounds
    min_toll = distance_km * 1.2   # Minimum ₹1.2/km
    max_toll = distance_km * 5.0   # Maximum ₹5/km
    
    return max(min_toll, min(total_toll, max_toll))

def should_use_direct_routing(source, destination):
    """
    Determine if direct routing should be used instead of Floyd-Warshall
    
    For most city pairs, direct routing is better
    Floyd-Warshall only useful for complex multi-city optimization
    """
    # For now, always use direct routing for better accuracy
    # Can add logic later for multi-city routes if needed
    return True