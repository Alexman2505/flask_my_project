# from flask import Flask, request, g

# app = Flask(__name__)


# @app.before_request
# def before_request():
#     print("before_request() called")


# @app.after_request
# def after_request(response):
#     print("after_request() called")
#     return response


# @app.teardown_request
# def teardown_request(exception=None):
#     print("teardown_request() called")


# @app.route("/")
# def index():
#     print("index() called")
#     return '<p>Testings Request Hooks</p>'


# if __name__ == "__main__":
#     app.run(debug=True)
