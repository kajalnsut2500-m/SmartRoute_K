from datetime import datetime
import logging
import re

from Toll import gmaps

logger = logging.getLogger(__name__)
def get_route_details(source, destination):
    # 1. Validate inputs
    if not source or not destination:
        logger.error(f"Missing source or destination. Got: {source}, {destination}")
        return None

    try:
        # 2. Geocode the inputs
        start_coords = gmaps.geocode(source)
        end_coords = gmaps.geocode(destination)

        if not start_coords:
            logger.error(f"Geocoding failed for source: {source}")
            return None
        if not end_coords:
            logger.error(f"Geocoding failed for destination: {destination}")
            return None

        # 3. Call Google Maps Directions API with correct syntax
        directions = gmaps.directions(
            source,  # origin
            destination,  # destination
            mode="driving",
            alternatives=True,
            departure_time="now"
        )

        if not directions:
            logger.error("No routes returned by Google Maps API.")
            return None

        # 4. Return the best route data
        if directions:
            best_route = directions[0]  # Use first (usually best) route
            leg = best_route['legs'][0]
            
            return {
                "summary": best_route.get('summary', 'Route'),
                "distance": leg['distance']['text'],
                "time": leg['duration']['text'],
                "distance_value": leg['distance']['value'],  # meters
                "duration_value": leg['duration']['value']   # seconds
            }
        
        return None

    except Exception as e:
        logger.error(f"Route fetching failed: {e}")
        return None


def extract_road_name(html_instruction):
    """Extracts road names like 'NH48' from HTML instructions"""
    # Example: "Take <b>NH48</b> toward Pune" → "NH48"
    match = re.search(r'<b>(.*?)<\/b>', html_instruction)
    return match.group(1) if match else html_instruction.split('>')[-1]