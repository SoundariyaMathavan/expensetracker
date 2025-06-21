import requests
import sys

def check_server():
    try:
        response = requests.get('http://localhost:5000/api/test')
        if response.status_code == 200:
            print("✅ Backend server is running correctly!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend server returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the backend server at http://localhost:5000")
        print("The server might not be running or might be running on a different port.")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {str(e)}")
        return False

if __name__ == "__main__":
    print("Checking if the backend server is running...")
    if check_server():
        sys.exit(0)
    else:
        sys.exit(1)import requests
import sys

def check_server():
    try:
        response = requests.get('http://localhost:5000/api/test')
        if response.status_code == 200:
            print("✅ Backend server is running correctly!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend server returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the backend server at http://localhost:5000")
        print("The server might not be running or might be running on a different port.")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {str(e)}")
        return False

if __name__ == "__main__":
    print("Checking if the backend server is running...")
    if check_server():
        sys.exit(0)
    else:
        sys.exit(1)