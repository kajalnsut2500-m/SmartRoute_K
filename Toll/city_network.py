# Expanded city network for comprehensive Floyd-Warshall implementation
# Following the conceptual framework: 20-30 cities with precomputed matrices

# Step 1: Fixed City Set (20+ major Indian cities)
CITIES = [
    # Metro cities
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad",
    
    # Major tourist destinations  
    "Goa", "Jaipur", "Agra", "Varanasi", "Amritsar", "Manali", "Shimla", "Rishikesh",
    
    # Important commercial centers
    "Surat", "Kanpur", "Lucknow", "Nagpur", "Indore", "Bhopal", "Coimbatore", "Kochi"
]

# Step 2 & 3: Precomputed matrices (would be built from Google Maps data)
# These represent the Floyd-Warshall results after processing

# Distance matrix (km) - shortest distances between all city pairs
DISTANCE_MATRIX = {
    # This would be populated by running Floyd-Warshall on Google Maps distance data
    # Format: DISTANCE_MATRIX[source_city][dest_city] = shortest_distance_km
}

# Time matrix (hours) - fastest routes between all city pairs  
TIME_MATRIX = {
    # This would be populated by running Floyd-Warshall on Google Maps time data
    # Format: TIME_MATRIX[source_city][dest_city] = fastest_time_hours
}

# Toll matrix (INR) - cheapest toll routes between all city pairs
TOLL_MATRIX = {
    # This would be populated by running Floyd-Warshall on toll cost data
    # Format: TOLL_MATRIX[source_city][dest_city] = minimum_toll_inr
}

# Step 4: Route paths (which cities to pass through for optimal routes)
ROUTE_PATHS = {
    # This stores the actual path to take for each optimal route
    # Format: ROUTE_PATHS[preference][source][dest] = [city1, city2, city3, ...]
    'distance': {},
    'time': {},
    'toll': {}
}

def get_optimal_route_from_precomputed(source, destination, preference):
    """
    Step 5: Use precomputed Floyd-Warshall results for instant route lookup
    
    Args:
        source (str): Starting city
        destination (str): Destination city  
        preference (str): 'distance', 'time', or 'toll'
    
    Returns:
        dict: Precomputed optimal route data
    """
    if source not in CITIES or destination not in CITIES:
        return None
    
    # Get precomputed optimal cost
    if preference == 'distance':
        cost = DISTANCE_MATRIX.get(source, {}).get(destination)
        unit = 'km'
    elif preference == 'time':
        cost = TIME_MATRIX.get(source, {}).get(destination)  
        unit = 'hours'
    elif preference == 'toll':
        cost = TOLL_MATRIX.get(source, {}).get(destination)
        unit = 'INR'
    else:
        return None
    
    if cost is None:
        return None
    
    # Get precomputed optimal path
    route_path = ROUTE_PATHS.get(preference, {}).get(source, {}).get(destination, [source, destination])
    
    return {
        'route': route_path,
        'cost': cost,
        'unit': unit,
        'preference': preference,
        'is_precomputed': True,
        'data_source': 'Floyd-Warshall Precomputed',
        'cities_in_network': len(CITIES)
    }

def is_city_in_network(city):
    """Check if city is in our precomputed network"""
    return city in CITIES

def get_network_cities():
    """Get list of all cities in the network"""
    return CITIES.copy()

def get_network_coverage():
    """Get statistics about the precomputed network"""
    total_routes = len(CITIES) * (len(CITIES) - 1)  # All pairs except same city
    return {
        'total_cities': len(CITIES),
        'total_precomputed_routes': total_routes,
        'network_regions': ['North', 'South', 'East', 'West', 'Central'],
        'last_updated': 'Static data - needs API refresh'
    }