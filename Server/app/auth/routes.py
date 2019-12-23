"""Auth routes."""

import traceback
from flask import request
from flask_login import login_user, logout_user, login_required
from flask_cors import cross_origin
from app.auth import authentication as at
from app.auth.models import User


def get_data():
    """Get data from request."""
    data = None
    try:
        data = request.json
        if data == {}:
            data = request.data
    except:
        traceback.print_exc()
        data = {}

    return data

@at.route('/api/auth/registeradmin', methods=['POST'])
@cross_origin()
def user_registerAdmin():
    """Register user."""
    try:
        # Extract data from request.
        data_dict = get_data()
        name = data_dict['name']
        email = data_dict['email']
        password = data_dict['password']

        # Create user in db.
        User.create_user(
            user=name,
            email=email,
            password=password,
            is_admin=True
        )

        # Registration was success.
        return {"result": True, "message": "Registration successfull."}
    except Exception as exc:
        traceback.print_exc()
        return {"result": False, "message": str(exc)}

@at.route('/api/auth/register', methods=['POST'])
@cross_origin()
def user_register():
    """Register user."""
    try:
        # Extract data from request.
        data_dict = get_data()
        name = data_dict['name']
        email = data_dict['email']
        password = data_dict['password']

        # Create user in db.
        User.create_user(
            user=name,
            email=email,
            password=password
        )

        # Registration was success.
        return {"result": True, "message": "Registration successfull."}
    except Exception as exc:
        traceback.print_exc()
        return {"result": False, "message": str(exc)}


@at.route('/api/auth/login', methods=['GET', 'POST'])
@cross_origin()
def user_login():
    try:
        # Extract data from request.
        data_dict = get_data()
        email = data_dict['email']
        password = data_dict['password']
        user = User.query.filter_by(user_email=email).first()

        # If user not exists or wrong password break.
        if not user or not user.check_password(password):
            return {"result": False, "message": "Wrong creds."}

        # Login manager code.
        login_user(user)
        print("Prosao sam")
        # Login was success.
        return {"result": True, "message": "Login successfull.","user_id": user.id}
    except Exception as exc:
        traceback.print_exc()
        return {"result": False, "message": "Error occured while login."}


@at.route('/api/auth/logout')
@login_required
@cross_origin()
def user_logout():
    """Log out user."""
    try:
        logout_user()
        return {"result": True, "message": "Logut successfull."}
    except Exception as exc:
        traceback.print_exc()
        return {"result": False, "message": "Error occured while logout."}


@at.after_request
def creds(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
