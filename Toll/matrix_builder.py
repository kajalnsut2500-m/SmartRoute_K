# Matrix builder for Floyd-Warshall preprocessing
# Step 2: Build city-to-city cost matrices from Google Maps

from Toll import gmaps
from Toll.city_network import CITIES
import json
import time
import logging

logger = logging.getLogger(__name__)

def build_comprehensive_matrices():
    """
    Step 2 & 3: Build and process matrices for Floyd-Warshall
    
    This function:
    1. Calls Google Maps for all city pairs
    2. Builds distance, time, and toll matrices  
    3. Runs Floyd-Warshall algorithm
    4. Saves results for fast lookup
    
    Note: This is a one-time setup process
    """
    if not gmaps:
        logger.error("Google Maps client not initialized")
        return False
    
    n = len(CITIES)
    
    # Initialize matrices
    distance_matrix = [[float('inf')] * n for _ in range(n)]
    time_matrix = [[float('inf')] * n for _ in range(n)]
    toll_matrix = [[float('inf')] * n for _ in range(n)]
    
    # Set diagonal to 0 (same city to same city)
    for i in range(n):
        distance_matrix[i][i] = 0
        time_matrix[i][i] = 0
        toll_matrix[i][i] = 0
    
    print(f"Building matrices for {n} cities ({n*n} total combinations)...")
    
    # Step 2: Get data from Google Maps for each city pair
    for i in range(n):
        for j in range(n):
            if i != j:  # Skip same city
                source = CITIES[i]
                destination = CITIES[j]
                
                try:
                    # Get route data from Google Maps
                    directions = gmaps.directions(
                        origin=f"{source}, India",
                        destination=f"{destination}, India",
                        mode="driving",
                        departure_time='now'
                    )
                    
                    if directions:
                        leg = directions[0]['legs'][0]
                        
                        # Extract distance (km)
                        distance_km = leg['distance']['value'] / 1000
                        distance_matrix[i][j] = distance_km
                        
                        # Extract time (hours)
                        time_hours = leg['duration']['value'] / 3600
                        if 'duration_in_traffic' in leg:
                            time_hours = leg['duration_in_traffic']['value'] / 3600
                        time_matrix[i][j] = time_hours
                        
                        # Estimate toll (INR) - would be replaced with real toll API
                        toll_estimate = estimate_toll_cost(distance_km, directions[0].get('summary', ''))
                        toll_matrix[i][j] = toll_estimate
                        
                        print(f"✓ {source} → {destination}: {distance_km:.0f}km, {time_hours:.1f}h, ₹{toll_estimate:.0f}")
                    
                    # Rate limiting
                    time.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"Error getting data for {source} → {destination}: {e}")
                    continue
    
    # Step 3: Run Floyd-Warshall algorithm on each matrix
    print("Running Floyd-Warshall algorithm...")
    
    distance_result, distance_paths = floyd_warshall_with_paths(distance_matrix)
    time_result, time_paths = floyd_warshall_with_paths(time_matrix)  
    toll_result, toll_paths = floyd_warshall_with_paths(toll_matrix)
    
    # Step 4: Save results
    save_matrices_and_paths(distance_result, time_result, toll_result, 
                           distance_paths, time_paths, toll_paths)
    
    print("✅ Comprehensive matrices built and saved!")
    return True

def floyd_warshall_with_paths(matrix):
    """
    Floyd-Warshall algorithm that also tracks the optimal paths
    
    Returns:
        tuple: (optimized_matrix, path_matrix)
    """
    n = len(matrix)
    
    # Copy input matrix
    dist = [row[:] for row in matrix]
    
    # Initialize path matrix
    next_matrix = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != float('inf'):
                next_matrix[i][j] = j
    
    # Floyd-Warshall main algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_matrix[i][j] = next_matrix[i][k]
    
    return dist, next_matrix

def reconstruct_path_from_matrix(start_idx, end_idx, next_matrix):
    """Reconstruct the optimal path from Floyd-Warshall results"""
    if next_matrix[start_idx][end_idx] is None:
        return []
    
    path = [start_idx]
    current = start_idx
    
    while current != end_idx:
        current = next_matrix[current][end_idx]
        path.append(current)
    
    # Convert indices to city names
    return [CITIES[i] for i in path]

def estimate_toll_cost(distance_km, route_summary):
    """Estimate toll cost - would be replaced with real toll API data"""
    base_rate = 2.5  # ₹2.5 per km base rate
    
    # Adjust based on route type
    if 'expressway' in route_summary.lower():
        rate = 4.0  # Higher rate for expressways
    elif any(highway in route_summary.upper() for highway in ['NH 48', 'NH 44', 'NH 8']):
        rate = 3.5  # Major national highways
    else:
        rate = base_rate
    
    return distance_km * rate

def save_matrices_and_paths(dist_matrix, time_matrix, toll_matrix, 
                           dist_paths, time_paths, toll_paths):
    """Step 4: Save Floyd-Warshall results for fast lookup"""
    
    # Convert matrices to city-name indexed dictionaries
    results = {
        'distance_matrix': matrix_to_dict(dist_matrix),
        'time_matrix': matrix_to_dict(time_matrix),
        'toll_matrix': matrix_to_dict(toll_matrix),
        'distance_paths': paths_to_dict(dist_paths),
        'time_paths': paths_to_dict(time_paths),
        'toll_paths': paths_to_dict(toll_paths),
        'cities': CITIES,
        'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save to JSON file
    with open('precomputed_routes.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("💾 Results saved to precomputed_routes.json")

def matrix_to_dict(matrix):
    """Convert matrix to city-name indexed dictionary"""
    result = {}
    for i, source in enumerate(CITIES):
        result[source] = {}
        for j, destination in enumerate(CITIES):
            if matrix[i][j] != float('inf'):
                result[source][destination] = matrix[i][j]
    return result

def paths_to_dict(path_matrix):
    """Convert path matrix to city-name indexed dictionary"""
    result = {}
    for i, source in enumerate(CITIES):
        result[source] = {}
        for j, destination in enumerate(CITIES):
            if i != j:
                path = reconstruct_path_from_matrix(i, j, path_matrix)
                if path:
                    result[source][destination] = path
    return result