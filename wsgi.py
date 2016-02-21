import os
from app import create_app

if __name__ == "__main__":
    app = create_app(os.getenv('APP_CONFIG', 'default'))
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)