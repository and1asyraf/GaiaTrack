# How to Launch GaiaTrack

## Quick Start

1. **Open Terminal/Command Prompt**
   - Navigate to the project folder: `cd "C:\Users\User\OneDrive\Documents\Projects Git Hub\GaiaTrack"`

2. **Activate Virtual Environment**
   ```
   venv\Scripts\activate
   ```

3. **Run the Django Server**
   ```
   python manage.py runserver
   ```

4. **Open Your Browser**
   - Go to: `http://127.0.0.1:8000/`

## That's it! 🚀

The app should now be running locally on your computer.

## Troubleshooting

- **If you get import errors**: Make sure the virtual environment is activated (you should see `(venv)` in your terminal)
- **If port 8000 is busy**: Django will automatically try port 8001, 8002, etc.
- **If you need to stop the server**: Press `Ctrl+C` in the terminal
