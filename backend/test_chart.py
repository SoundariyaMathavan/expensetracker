import requests
import json
import base64
import matplotlib.pyplot as plt
from io import BytesIO

# Make a request to the summary endpoint
response = requests.get('http://localhost:5000/api/summary')
data = response.json()

# Check if the request was successful
if data['success']:
    # Get the plot data
    plot_data = data['plot']
    
    # Decode the base64 image
    image_data = base64.b64decode(plot_data)
    
    # Save the image to a file
    with open('chart.png', 'wb') as f:
        f.write(image_data)
    
    print("Chart saved to chart.png")
    
    # Print some stats
    print(f"Total expenses: {data['stats']['total']}")
    print(f"Average daily expenses: {data['stats']['avg_daily']}")
    print(f"Selected category: {data['selected_category']}")
else:
    print(f"Error: {data.get('error', 'Unknown error')}")