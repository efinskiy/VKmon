from . import db

def commit(object):
    db.session.add(object)
    db.session.commit()
    db.session.refresh(object)
    return object

def delete(object) -> None:
    db.session.delete(object)
    db.session.commit()