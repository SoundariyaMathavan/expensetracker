# Expense Tracker Backend

## Fixing the Seaborn Style Error

If you're encountering the error:

```
Error: 'seaborn' is not a valid package style, path of style file, URL of style file, or library style name (library styles are listed in `style.available`)
```

This is because you're trying to use seaborn's style in matplotlib incorrectly.

### Solution:

1. **DO NOT use:**
   ```python
   plt.style.use('seaborn')  # This is incorrect and causes the error
   ```

2. **Instead, use one of these approaches:**

   a. **Recommended: Use seaborn's set_style function:**
   ```python
   import seaborn as sns
   sns.set_style("darkgrid")  # Valid options: "darkgrid", "whitegrid", "dark", "white", "ticks"
   ```

   b. **Alternative: Use a valid matplotlib style name:**
   
   For newer versions of matplotlib/seaborn:
   ```python
   plt.style.use('seaborn-v0_8-darkgrid')
   ```
   
   For older versions:
   ```python
   plt.style.use('seaborn-darkgrid')
   ```

3. **To see all available styles:**
   ```python
   import matplotlib.pyplot as plt
   print(plt.style.available)
   ```

## Example Usage

See the `visualization.py` and `app.py` files for complete examples of how to properly use seaborn with matplotlib.

## Running the Backend

1. Make sure you have all dependencies installed:
   ```
   pip install -r requirements.txt
   ```

2. Run the Flask application:
   ```
   python app.py
   ```

3. The API will be available at `http://localhost:5000`