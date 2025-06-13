# Install dependencies
Write-Host "Installing Python packages..."
pip install -r requirements.txt

# Run the Python script
Write-Host "Starting Star Citizen Rich Presence..."
python .\star_citizen_presence.py

# Pause so window doesn't close immediately
Write-Host "Press any key to exit..."
$x = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
