
class Config:
    JOBS = [
        {
            'id': 'job1',
            'func': 'app.utils:delete_deprecated_photos',
            'args': (),
            'trigger': 'interval',
            'seconds': 10#60 * 60 * 24
        }
    ]
    SCHEDULER_API_ENABLED = True

class DevelopmentConfig(Config):
    API_ACCESS_TOKEN = '123456abcdef'
    SECRET_KEY = '1mht0m5830yKry2Y3w14kL8w05YF7T9C2Kb5O778Z0poWm3xkh7pb91JxO949Ks42n7LrE'

class ProdConfig(Config):
    API_ACCESS_TOKEN = ...
    SECRET_KEY = ...
