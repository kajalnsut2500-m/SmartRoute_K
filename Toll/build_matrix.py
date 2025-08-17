import numpy as np
from Toll.map_service import get_route_details


def build_matrix(preference='distance', cities=None):
    """
    Builds a N x N cost matrix from Google Maps API data.
    
    Args:
        preference (str): "distance" (km), "time" (hrs), or "toll" (₹/$)
        cities (list): Optional list of city names. If None, uses default cities.
    
    Returns:
        tuple: (np.ndarray: Cost matrix, list: cities used)
    """
    # Validate preference parameter to prevent injection
    valid_preferences = ['distance', 'time', 'toll']
    if preference not in valid_preferences:
        raise ValueError(f"Invalid preference. Must be one of: {valid_preferences}")
    
    if cities is None:
        cities = ["Mumbai", "Delhi", "Bangalore", "Pune", "Chennai", "Kolkata", "Hyderabad", "Ahmedabad"]
    
    # Add caching to avoid repeated API calls
    cache = {}
    n = len(cities)
    matrix = np.full((n, n), np.inf)  # Initialize with infinity
    
    # Set diagonal to 0 (same city)
    np.fill_diagonal(matrix, 0)
    
    # Only process upper triangle to avoid duplicate API calls
    for i in range(n):
        for j in range(i + 1, n):
                
            # Check cache first
            cache_key = f"{cities[i]}-{cities[j]}"
            if cache_key in cache:
                data = cache[cache_key]
            else:
                # Get API data for city pair with error handling
                try:
                    data = get_route_details(cities[i], cities[j])
                    if data:
                        cache[cache_key] = data
                except Exception as e:
                    print(f"API call failed for {cities[i]} to {cities[j]}: {e}")
                    data = None
                    
            if not data:
                print(f"No data for {cities[i]} to {cities[j]}")
                continue  # Keep as infinity if no route
            
            print(f"API data for {cities[i]} to {cities[j]}: {data}")
            
            try:
                # Set cost based on user preference
                if preference == 'distance' and 'distance' in data:
                    cost = float(data['distance'].split()[0].replace(',', ''))
                    matrix[i][j] = matrix[j][i] = cost  # Symmetric matrix
                elif preference == 'time' and 'time' in data:
                    # Use duration_value (seconds) from API for accurate time
                    if 'duration_value' in data:
                        cost = data['duration_value'] / 3600  # Convert seconds to hours
                        matrix[i][j] = matrix[j][i] = cost
                    else:
                        # Fallback: Parse time text like "15 hours 30 mins"
                        import re
                        time_text = data['time'].lower()
                        hours = 0
                        minutes = 0
                        
                        # Extract hours using regex
                        hour_match = re.search(r'(\d+)\s*hour', time_text)
                        if hour_match:
                            hours = float(hour_match.group(1))
                        
                        # Extract minutes using regex
                        min_match = re.search(r'(\d+)\s*min', time_text)
                        if min_match:
                            minutes = float(min_match.group(1))
                        
                        cost = hours + (minutes / 60)  # Convert to decimal hours
                        matrix[i][j] = matrix[j][i] = cost
                elif preference == 'toll':
                    # For toll, use estimated value based on distance
                    if 'distance_value' in data:
                        distance_km = data['distance_value'] / 1000  # Convert meters to km
                        cost = distance_km * 2.5  # ₹2.5 per km estimate
                        matrix[i][j] = matrix[j][i] = cost
                    elif 'distance' in data:
                        distance = float(data['distance'].split()[0].replace(',', ''))
                        cost = distance * 2.5  # ₹2.5 per km estimate
                        matrix[i][j] = matrix[j][i] = cost
            except (ValueError, IndexError, KeyError):
                continue  # Skip invalid data
        
    
    return matrix, cities



'''import sqlite3
from Toll.floyd_warshall import floyd_warshall
import os





def build_matrix_from_db(preference):
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path =os.path.join(basedir,"toll.db")
    print('USing database at : ',db_path)
    conn=sqlite3.connect(db_path)
    cursor=conn.cursor()
    cursor.execute('SELECT id,source,destination,time,distance,toll FROM route_data')
    data=cursor.fetchall()
    print("data : ",data)
    print("DB exists: ",os.path.exists(db_path))
    
    cities=set()
    for row in data:
        try:
            id,src,dst,time,dist,toll=row
            src=str(src).strip().title()
            dst=str(dst).strip().title()
            if not src or not dst or src=='source' or dst=='destination':
               continue
            cities.add(src)
            cities.add(dst)
        except Exception as e:
            print("Skipping error due to error:", row,e)
            continue
        
        
    
    cities=sorted(list(cities))
    city_index={city:i for i ,city in enumerate(cities)}

    n=len(cities)
    INF=10**9
    matrix=[[INF]*n for i in range(n)]
    
    
    for j in range(n):
        matrix[j][j]=0
    for row in data:
        try:
            id,src,dst,time, dist,toll=row
            src=str(src).strip().title()
            dst=str(dst).strip().title()
            if src not in city_index or dst not in city_index:
               continue
            i=city_index[str(src)]
            k=city_index[str(dst)]
            if preference=='time':
                matrix[i][k]=time
            elif preference=='distance':
                matrix[i][k]=dist
            elif preference=='toll':
                matrix[i][k]=toll
        except Exception as e:
            print("Error while building matrix from row:", row,e)
            continue
    conn.close()
    return matrix,cities'''

