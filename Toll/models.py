from Toll import db,app,login_manager
from Toll import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    try:
        return UserInput.query.get(int(user_id))
    except (ValueError, TypeError):
        return None
 
class RouteData(db.Model):
    __tablename__='route_data'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    time = db.Column(db.Float, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    toll = db.Column(db.Float, nullable=False)

class UserInput(db.Model,UserMixin):
    __tablename__ = 'UserInput'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30),nullable = False, unique=True)
    email_address = db.Column(db.String(length=50),nullable = False, unique=True)
    password_hash = db.Column(db.String(length=60),nullable = False)


    @property
    def password(self):
        raise AttributeError('Password is not readable')
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


