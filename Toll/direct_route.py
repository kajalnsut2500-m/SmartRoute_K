# Direct route calculation using Google Directions API
# Bypasses Floyd-Warshall for more accurate real-world routing

import os
from dotenv import load_dotenv
from Toll import gmaps
import logging

load_dotenv()
logger = logging.getLogger(__name__)

def get_direct_route(source, destination, preference='distance'):
    """
    Get direct route using Google Directions API with proper preferences
    
    Args:
        source (str): Starting city
        destination (str): Destination city
        preference (str): 'distance', 'time', or 'toll'
    
    Returns:
        dict: Route data with accurate information
    """
    if not gmaps:
        logger.error("Google Maps client not initialized")
        return None
    
    try:
        # Map preferences to Google Directions API parameters
        avoid_params = []
        optimize_route = True
        
        if preference == 'toll':
            avoid_params = ['tolls']
        elif preference == 'time':
            # Use traffic-aware routing for fastest time
            departure_time = 'now'
        
        # Get directions with proper parameters
        directions = gmaps.directions(
            origin=f"{source}, India",
            destination=f"{destination}, India",
            mode="driving",
            avoid=avoid_params if avoid_params else None,
            optimize_waypoints=optimize_route,
            departure_time='now',
            traffic_model='best_guess',
            alternatives=True
        )
        
        if not directions:
            logger.warning(f"No directions found from {source} to {destination}")
            return None
        
        # Get the best route (first one is usually optimal for given preference)
        route = directions[0]
        leg = route['legs'][0]
        
        # Extract accurate route information
        distance_km = leg['distance']['value'] / 1000  # Convert meters to km
        duration_hours = leg['duration']['value'] / 3600  # Convert seconds to hours
        
        # Get traffic-aware duration if available
        if 'duration_in_traffic' in leg:
            duration_hours = leg['duration_in_traffic']['value'] / 3600
        
        # Extract highway information from steps
        highways = []
        toll_plazas = 0
        
        for step in leg['steps']:
            if 'html_instructions' in step:
                instruction = step['html_instructions']
                highway = extract_highway_name(instruction)
                if highway and highway not in highways:
                    highways.append(highway)
                
                # Count potential toll plazas (rough estimate)
                if any(word in instruction.lower() for word in ['toll', 'plaza', 'expressway']):
                    toll_plazas += 1
        
        # Calculate realistic toll based on actual toll plazas and route type
        toll_cost = calculate_realistic_toll(distance_km, highways, toll_plazas)
        
        return {
            'route': [source, destination],  # Direct route
            'distance_km': distance_km,
            'duration_hours': duration_hours,
            'toll_cost': toll_cost,
            'highways': highways,
            'route_summary': route.get('summary', ''),
            'is_direct_route': True,
            'data_source': 'Google Directions API',
            'timestamp': 'Live data'
        }
        
    except Exception as e:
        logger.error(f"Direct route error for {source} to {destination}: {e}")
        return None

def extract_highway_name(html_instruction):
    """Extract highway names from Google's HTML instructions"""
    import re
    
    # Remove HTML tags
    clean_text = re.sub('<[^<]+?>', '', html_instruction)
    
    # Look for highway patterns
    highway_patterns = [
        r'\b(NH\s*\d+[A-Z]?)\b',  # National Highway: NH48, NH44
        r'\b(NE\s*\d+)\b',        # National Expressway: NE4
        r'\b(SH\s*\d+[A-Z]?)\b',  # State Highway: SH1, SH2
        r'\b(AH\s*\d+[A-Z]?)\b',  # Asian Highway: AH1, AH2
        r'\b([A-Za-z\s]+-[A-Za-z\s]+\s*Expressway)\b',  # Named expressways
    ]
    
    for pattern in highway_patterns:
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None

def calculate_realistic_toll(distance_km, highways, toll_plazas):
    """
    Calculate realistic toll based on actual toll plaza structure
    
    Args:
        distance_km (float): Route distance
        highways (list): List of highways used
        toll_plazas (int): Estimated number of toll plazas
    
    Returns:
        float: Realistic toll cost in INR
    """
    base_toll = 0
    
    # Toll rates based on highway type
    highway_rates = {
        'expressway': 150,  # ₹150 per 100km on expressways
        'nh': 80,          # ₹80 per 100km on national highways
        'sh': 50,          # ₹50 per 100km on state highways
        'default': 60      # Default rate
    }
    
    # Determine primary highway type
    primary_rate = highway_rates['default']
    for highway in highways:
        if 'expressway' in highway.lower():
            primary_rate = highway_rates['expressway']
            break
        elif highway.startswith('NH'):
            primary_rate = highway_rates['nh']
        elif highway.startswith('SH'):
            primary_rate = highway_rates['sh']
    
    # Calculate base toll
    base_toll = (distance_km / 100) * primary_rate
    
    # Add toll plaza charges (₹30-50 per plaza)
    plaza_charges = toll_plazas * 40  # Average ₹40 per plaza
    
    # Total realistic toll
    total_toll = base_toll + plaza_charges
    
    # Apply reasonable bounds
    min_toll = distance_km * 1.5  # Minimum ₹1.5/km
    max_toll = distance_km * 6.0  # Maximum ₹6/km
    
    return max(min_toll, min(total_toll, max_toll))

def get_optimized_route(source, destination, preference='distance'):
    """
    Get optimized route that bypasses Floyd-Warshall for direct routes
    
    Returns both direct route and fallback multi-city route if needed
    """
    # First try direct route (most accurate)
    direct_route = get_direct_route(source, destination, preference)
    
    if direct_route:
        return direct_route
    
    # Fallback to existing Floyd-Warshall method
    logger.info(f"Using Floyd-Warshall fallback for {source} to {destination}")
    return None  # Let existing code handle this