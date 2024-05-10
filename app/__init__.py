from flask import Flask
from flask_apscheduler import APScheduler


app = Flask(__name__)
app.config['JOBS'] = [
        {
            'id': 'job1',
            'func': 'app.utils:delete_deprecated_photos',
            'args': (),
            'trigger': 'interval',
            'seconds': 60 * 60 * 24
        }
    ]

app.config['SCHEDULER_API_ENABLED'] = True
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

from . import routers