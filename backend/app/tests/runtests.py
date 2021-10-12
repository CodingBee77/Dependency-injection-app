import sqlalchemy

from . import common

def runtests():
    engine = sqlalchemy.create_engine('sqlite://')

    # It's a scoped_session, and now is the time to configure it.
    common.Session.configure(bind=engine)

    