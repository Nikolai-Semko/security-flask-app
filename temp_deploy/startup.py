# startup.py for Azure App Service
import os
from app import app

if __name__ == '__main__':
    # Azure App Service sets the PORT environment variable
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)