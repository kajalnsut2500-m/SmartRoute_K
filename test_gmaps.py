from Toll import gmaps

# Test Directions API
try:
    result = gmaps.directions(
        origin="Delhi",
        destination="Mumbai",
        mode="driving",
        departure_time="now"
    )
    
    if result:
        print("✅ API is working! Got routes:")
        for route in result:
            print("Summary:", route['summary'])
            print("Distance:", route['legs'][0]['distance']['text'])
            print("Duration:", route['legs'][0]['duration']['text'])
            print()
    else:
        print(" No data returned. Check API key and enabled APIs.")

except Exception as e:
    print(" Error:", e)
