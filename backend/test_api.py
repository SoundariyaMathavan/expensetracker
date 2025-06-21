import requests
import json

def test_summary_endpoint():
    # Test with no category filter
    print("Testing /api/summary with no category filter...")
    response = requests.get('http://localhost:5000/api/summary')
    if response.status_code == 200:
        data = response.json()
        print("Success! Response:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    
    print("\n" + "-"*50 + "\n")
    
    # Test with category filter
    print("Testing /api/summary with category='Food'...")
    response = requests.get('http://localhost:5000/api/summary?category=Food')
    if response.status_code == 200:
        data = response.json()
        print("Success! Response:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def test_expenses_endpoint():
    # Test with no category filter
    print("Testing /api/expenses with no category filter...")
    response = requests.get('http://localhost:5000/api/expenses?period=monthly')
    if response.status_code == 200:
        data = response.json()
        print("Success! Response:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    
    print("\n" + "-"*50 + "\n")
    
    # Test with category filter
    print("Testing /api/expenses with category='Food'...")
    response = requests.get('http://localhost:5000/api/expenses?period=monthly&category=Food')
    if response.status_code == 200:
        data = response.json()
        print("Success! Response:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print("Testing API endpoints...")
    print("="*50)
    test_summary_endpoint()
    print("="*50)
    test_expenses_endpoint()
    print("="*50)
    print("Tests completed.")