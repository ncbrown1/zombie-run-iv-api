import os
from app import create_app

if __name__ == "__main__":
    app = create_app(os.getenv('APP_CONFIG', 'default'))
    app.run()