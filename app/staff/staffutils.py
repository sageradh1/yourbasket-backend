from app.user.models import User

def getStaffs():
    return User.query.filter_by(urole="staff").all()
