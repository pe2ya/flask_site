import re
import json
from flask import Flask, render_template
from flask import request, redirect, jsonify
import db.user as user
from redmail import outlook



# from sqlalchemy import create_engine
# from sqlalchemy.pool import SingletonThreadPool
# engine = create_engine('sqlite:///db.sqlite', poolclass=SingletonThreadPool)

app = Flask(__name__)
outlook.username = "pe2ya.flask@hotmail.com"
outlook.password = "flaskText123"

@app.route('/')
def index():
    return render_template('registration.html')


@app.route('/api/user/get', methods=["GET"])
def get_user():
    result = user.get_all_users()
    return jsonify(result), 200


@app.route('/api/user/check/<user_name>/<user_surname>', methods=["GET"])
def user_check(user_name, user_surname):
    id = user.find_user_id(user_name, user_surname)

    if id == 0:
        return jsonify(False), 200

    else:
        return jsonify(True), 200

@app.route('/api/user/confirm/<u_id>', methods=["GET"])
def confirm(u_id):
    try:
        c_id = int(u_id)
        if c_id > 0:
            user.delete_user_id(c_id)
            return jsonify(True), 200

        else:
            return jsonify(False), 200
    except Exception as e:
        print(e)



@app.route('/register')
def register():
    return render_template('registration.html')


@app.route('/api/user/create', methods=["POST"])
def create():
    tester = "^[_A-zA-Z]*((-|\s)*[_A-zA-Z])*$"
    email_tester = "^\S+@\S+\.\S+$"

    request_data = request.get_json()

    is_swimmer = request_data["is_swimmer"]
    name = request_data["name"]
    surname = request_data["surname"]
    email = request_data["email"]
    mate_name = request_data["mate_name"]
    mate_surname = request_data["mate_surname"]

    if re.search(tester, name) and 1 < len(name) < 21 and \
            re.search(tester, surname) and 1 < len(surname) < 21 and \
            re.search(email_tester, email):

        if not user.find_user_id(name, surname):

            outlook.send(
                receivers=[email],
                subject="Registration",
                text=f"{name}, thx you to choose us, we glad you are with as"
            )

            if not mate_name and not mate_surname:

                user.add_user(name, surname, email)
                return jsonify(True), 200

            else:
                u_id = user.find_user_id(mate_name, mate_surname)

                if u_id == 0:
                    return jsonify(False), 200
                else:
                    u_email = user.find_user(mate_name, mate_surname).email
                    c_id = user.find_user_id(name, surname).id
                    outlook.send(
                        receivers=[u_email],
                        subject="Confirm",
                        text=f"You want you be in team with {name}?\nFollow link http://127.0.0.1:8080/api/user/confirm/{c_id} or ignore if u doesn't "
                    )
                    user.add_user(name, surname, email, u_id)
                    return jsonify(True), 200
        else:
            return jsonify(False), 200

    else:
        return jsonify(False), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
