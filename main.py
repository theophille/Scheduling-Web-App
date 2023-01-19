from our_scheduler import app
from our_scheduler.scripts.auth import auth
app.register_blueprint(auth, url_prefix="/auth")
from our_scheduler.scripts.scheduler import scd
app.register_blueprint(scd, url_prefix="/auth/logged")
from our_scheduler.scripts import *
