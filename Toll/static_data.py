# Pre-computed distance, time, and toll data for major Indian cities
# This eliminates the need for Google Maps API calls during runtime

CITIES = ["Mumbai", "Delhi", "Bangalore", "Pune", "Chennai", "Kolkata", "Hyderabad", "Ahmedabad"]

# Distance matrix (in km) - based on current operational highways
DISTANCE_MATRIX = [
    [0,    1420, 981,  149,  1338, 1968, 711,  524],  # Mumbai (Delhi via Ahmedabad route)
    [1420, 0,    2194, 1569, 2180, 1472, 1566, 442], # Delhi
    [981,  2194, 0,    844,  347,  1871, 569,  1032], # Bangalore
    [149,  1569, 844,  0,    1181, 1875, 559,  665],  # Pune
    [1338, 2180, 347,  1181, 0,    1663, 629,  1371], # Chennai
    [1968, 1472, 1871, 1875, 1663, 0,    1500, 1914], # Kolkata
    [711,  1566, 569,  559,  629,  1500, 0,    977],  # Hyderabad
    [524,  442,  1032, 665,  1371, 1914, 977,  0]     # Ahmedabad
]

# Time matrix (in hours) - based on current operational highways only
TIME_MATRIX = [
    [0,    18.5, 12.8, 2.5,  17.2, 24.1, 9.2,  6.8],  # Mumbai
    [18.5, 0,    26.5, 20.2, 26.8, 18.5, 19.2, 8.5],  # Delhi (via NH48 through Ahmedabad)
    [12.8, 26.5, 0,    10.5, 4.2,  23.1, 7.1,  12.9], # Bangalore
    [2.5,  20.2, 10.5, 0,    14.8, 23.2, 7.0,  8.2],  # Pune
    [17.2, 26.8, 4.2,  14.8, 0,    20.5, 7.8,  17.1], # Chennai
    [24.1, 18.5, 23.1, 23.2, 20.5, 0,    18.5, 23.8], # Kolkata
    [9.2,  19.2, 7.1,  7.0,  7.8,  18.5, 0,    12.1], # Hyderabad
    [6.8,  8.5,  12.9, 8.2,  17.1, 23.8, 12.1, 0]     # Ahmedabad
]

# Toll matrix (in INR) - based on actual toll plaza charges
TOLL_MATRIX = [
    [0,    2400, 1800, 350,  2200, 3200, 1200, 900],  # Mumbai
    [2400, 0,    3500, 2100, 3800, 2200, 2500, 800],  # Delhi
    [1800, 3500, 0,    1400, 600,  2800, 950,  1600], # Bangalore
    [350,  2100, 1400, 0,    1800, 2900, 850,  1100], # Pune
    [2200, 3800, 600,  1800, 0,    2500, 1000, 2100], # Chennai
    [3200, 2200, 2800, 2900, 2500, 0,    2200, 3000], # Kolkata
    [1200, 2500, 950,  850,  1000, 2200, 0,    1500], # Hyderabad
    [900,  800,  1600, 1100, 2100, 3000, 1500, 0]     # Ahmedabad
]

def get_matrix(preference='distance'):
    """
    Get pre-computed matrix for the given preference
    
    Args:
        preference (str): 'distance', 'time', or 'toll'
    
    Returns:
        tuple: (matrix, cities)
    """
    if preference == 'distance':
        return [row[:] for row in DISTANCE_MATRIX], CITIES[:]
    elif preference == 'time':
        return [row[:] for row in TIME_MATRIX], CITIES[:]
    elif preference == 'toll':
        return [row[:] for row in TOLL_MATRIX], CITIES[:]
    else:
        raise ValueError(f"Invalid preference: {preference}")