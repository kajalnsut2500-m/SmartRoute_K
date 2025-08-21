# Smart routing system that combines Floyd-Warshall precomputed data with live Google Maps
# Implements the complete conceptual framework

import json
import os
from Toll.city_network import CITIES, is_city_in_network
from Toll.direct_routing import get_direct_route
import logging

logger = logging.getLogger(__name__)

class SmartRouter:
    def __init__(self):
        self.precomputed_data = self.load_precomputed_data()
    
    def load_precomputed_data(self):
        """Step 4: Load saved Floyd-Warshall results"""
        try:
            with open('precomputed_routes.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Precomputed routes not found. Run matrix_builder.py first.")
            return None
    
    def get_optimal_route(self, source, destination, preference):
        """
        Smart routing decision engine:
        1. Check if both cities are in precomputed network
        2. Use Floyd-Warshall results if available
        3. Fall back to direct Google Maps routing
        4. Use Google Maps for final highway details (Step 6)
        """
        
        # Step 5: Use precomputed data if both cities are in network
        if (self.precomputed_data and 
            is_city_in_network(source) and 
            is_city_in_network(destination)):
            
            precomputed_route = self.get_precomputed_route(source, destination, preference)
            if precomputed_route:
                # Step 6: Enhance with live Google Maps data for highway details
                enhanced_route = self.enhance_with_live_data(precomputed_route)
                return enhanced_route
        
        # Fallback: Direct Google Maps routing for cities not in network
        logger.info(f"Using direct routing for {source} → {destination} (not in precomputed network)")
        return get_direct_route(source, destination, preference)
    
    def get_precomputed_route(self, source, destination, preference):
        """Step 5: Look up optimal route from Floyd-Warshall results"""
        try:
            # Get optimal cost from precomputed matrices
            if preference == 'distance':
                cost = self.precomputed_data['distance_matrix'][source][destination]
                paths = self.precomputed_data['distance_paths']
                unit = 'km'
            elif preference == 'time':
                cost = self.precomputed_data['time_matrix'][source][destination]
                paths = self.precomputed_data['time_paths']
                unit = 'hours'
            elif preference == 'toll':
                cost = self.precomputed_data['toll_matrix'][source][destination]
                paths = self.precomputed_data['toll_paths']
                unit = 'INR'
            else:
                return None
            
            # Get optimal path (list of cities to pass through)
            route_path = paths.get(source, {}).get(destination, [source, destination])
            
            return {
                'route': route_path,
                'cost': cost,
                'unit': unit,
                'preference': preference,
                'is_precomputed': True,
                'data_source': 'Floyd-Warshall Precomputed',
                'last_updated': self.precomputed_data.get('last_updated', 'Unknown')
            }
            
        except (KeyError, TypeError) as e:
            logger.error(f"Error accessing precomputed data: {e}")
            return None
    
    def enhance_with_live_data(self, precomputed_route):
        """
        Step 6: Use Google Maps only for final route details
        - Highway names
        - Current traffic conditions  
        - Updated toll booth locations
        """
        route_path = precomputed_route['route']
        
        if len(route_path) < 2:
            return precomputed_route
        
        # Get live highway and traffic data for the precomputed optimal route
        live_data = get_direct_route(route_path[0], route_path[-1], precomputed_route['preference'])
        
        if live_data:
            # Combine precomputed optimal path with live highway details
            enhanced = precomputed_route.copy()
            enhanced.update({
                'highways': live_data.get('highways', []),
                'route_summary': live_data.get('route_summary', ''),
                'live_traffic_time': live_data.get('duration_hours'),
                'enhanced_with_live_data': True
            })
            return enhanced
        
        return precomputed_route
    
    def get_routing_strategy(self, source, destination):
        """Determine which routing strategy to use"""
        both_in_network = (is_city_in_network(source) and is_city_in_network(destination))
        has_precomputed = self.precomputed_data is not None
        
        if both_in_network and has_precomputed:
            return "floyd_warshall_enhanced"
        else:
            return "direct_google_maps"
    
    def get_network_info(self):
        """Get information about the routing network"""
        if self.precomputed_data:
            return {
                'total_cities': len(self.precomputed_data.get('cities', [])),
                'last_updated': self.precomputed_data.get('last_updated'),
                'has_precomputed_data': True,
                'routing_strategy': 'Hybrid (Floyd-Warshall + Google Maps)'
            }
        else:
            return {
                'total_cities': len(CITIES),
                'has_precomputed_data': False,
                'routing_strategy': 'Direct Google Maps only'
            }

# Global router instance
smart_router = SmartRouter()

def get_smart_route(source, destination, preference):
    """
    Main function to get optimal route using smart routing strategy
    
    This implements the complete conceptual framework:
    - Uses Floyd-Warshall for cities in precomputed network
    - Falls back to direct Google Maps for other cities
    - Enhances results with live traffic and highway data
    """
    return smart_router.get_optimal_route(source, destination, preference)