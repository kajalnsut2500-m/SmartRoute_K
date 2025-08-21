import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class RoutesAPI:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.base_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    
    def get_route_with_tolls(self, origin, destination, preference='TRAFFIC_AWARE'):
        """
        Get route with real toll information from Google Routes API
        
        Args:
            origin (str): Starting city
            destination (str): Destination city  
            preference (str): 'TRAFFIC_AWARE', 'TRAFFIC_AWARE_OPTIMAL', 'FUEL_EFFICIENT'
        
        Returns:
            dict: Route data with real toll costs
        """
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters,routes.travelAdvisory.tollInfo'
        }
        
        # Map preferences to Routes API routing preferences
        routing_preference_map = {
            'distance': 'FUEL_EFFICIENT',
            'time': 'TRAFFIC_AWARE_OPTIMAL', 
            'toll': 'FUEL_EFFICIENT'
        }
        
        routing_preference = routing_preference_map.get(preference, 'TRAFFIC_AWARE')
        
        payload = {
            "origin": {
                "address": f"{origin}, India"
            },
            "destination": {
                "address": f"{destination}, India"
            },
            "travelMode": "DRIVE",
            "routingPreference": routing_preference,
            "computeAlternativeRoutes": False,
            "languageCode": "en-US",
            "units": "METRIC"
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            
            if response.status_code != 200:
                logger.error(f"Routes API error {response.status_code}: {response.text}")
                # Fallback to simple estimation
                return self._fallback_estimation(origin, destination)
            
            data = response.json()
            
            if 'routes' not in data or not data['routes']:
                logger.warning(f"No routes found from {origin} to {destination}")
                return self._fallback_estimation(origin, destination)
            
            # Get the best route (first one is usually optimal)
            route = data['routes'][0]
            
            # Extract route information
            distance_km = route.get('distanceMeters', 0) / 1000
            duration_str = route.get('duration', '0s')
            duration_seconds = int(duration_str.replace('s', '')) if duration_str.endswith('s') else 0
            duration_hours = duration_seconds / 3600
            
            # Extract toll information
            toll_info = route.get('travelAdvisory', {}).get('tollInfo', {})
            estimated_price = toll_info.get('estimatedPrice', [])
            
            # Convert toll price to INR
            toll_cost_inr = 0
            if estimated_price:
                for price in estimated_price:
                    if price.get('currencyCode') == 'INR':
                        toll_cost_inr = float(price.get('units', 0))
                        break
                    elif price.get('currencyCode') == 'USD':
                        # Convert USD to INR (approximate rate: 1 USD = 83 INR)
                        toll_cost_inr = float(price.get('units', 0)) * 83
                        break
            
            return {
                'distance_km': distance_km,
                'duration_hours': duration_hours,
                'toll_cost_inr': toll_cost_inr,
                'has_tolls': len(estimated_price) > 0,
                'route_found': True
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Routes API error for {origin} to {destination}: {e}")
            return self._fallback_estimation(origin, destination)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return self._fallback_estimation(origin, destination)
    
    def _fallback_estimation(self, origin, destination):
        """Fallback to static data when Routes API fails"""
        # Use static data as fallback
        from Toll.static_data import get_matrix, CITIES
        
        if origin in CITIES and destination in CITIES:
            distance_matrix, _ = get_matrix('distance')
            time_matrix, _ = get_matrix('time')
            toll_matrix, _ = get_matrix('toll')
            
            origin_idx = CITIES.index(origin)
            dest_idx = CITIES.index(destination)
            
            return {
                'distance_km': distance_matrix[origin_idx][dest_idx],
                'duration_hours': time_matrix[origin_idx][dest_idx],
                'toll_cost_inr': toll_matrix[origin_idx][dest_idx],
                'has_tolls': True,
                'route_found': True
            }
        
        return None

def build_matrix_with_routes_api(preference='distance', cities=None):
    """
    Build matrix using Routes API for real toll data
    
    Args:
        preference (str): 'distance', 'time', or 'toll'
        cities (list): List of cities
    
    Returns:
        tuple: (matrix, cities)
    """
    if cities is None:
        cities = ["Mumbai", "Delhi", "Bangalore", "Pune", "Chennai", "Kolkata", "Hyderabad", "Ahmedabad"]
    
    routes_api = RoutesAPI()
    n = len(cities)
    matrix = [[float('inf')] * n for _ in range(n)]
    
    # Set diagonal to 0 (same city)
    for i in range(n):
        matrix[i][i] = 0
    
    # Get route data for each city pair
    for i in range(n):
        for j in range(n):
            if i != j:
                route_data = routes_api.get_route_with_tolls(cities[i], cities[j], preference)
                
                if route_data and route_data['route_found']:
                    if preference == 'distance':
                        matrix[i][j] = route_data['distance_km']
                    elif preference == 'time':
                        matrix[i][j] = route_data['duration_hours']
                    elif preference == 'toll':
                        # Use actual toll cost, fallback to distance-based if no toll data
                        if route_data['toll_cost_inr'] > 0:
                            matrix[i][j] = route_data['toll_cost_inr']
                        else:
                            # Fallback: estimate based on distance
                            matrix[i][j] = route_data['distance_km'] * 2.5
                
                # Add small delay to avoid rate limiting
                import time
                time.sleep(0.1)
    
    return matrix, cities