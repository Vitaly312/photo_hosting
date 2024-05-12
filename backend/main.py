from app import app
from config import DevelopmentConfig, ProdConfig
from flask_apscheduler import APScheduler
import os

#print(os.environ.get("FLASK_DEBUG") )
app.config.from_object(DevelopmentConfig() if os.environ.get("FLASK_DEBUG") or 1
                       else ProdConfig())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    app.run(port=5057, debug=True)