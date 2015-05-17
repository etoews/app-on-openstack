from flask import Flask

api = Flask(__name__)

@api.route('/')
def index():
    return '<h1>Welcome to the API</h1>'

if __name__ == '__main__':
    api.run(debug=True)
