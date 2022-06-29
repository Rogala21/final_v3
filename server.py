from flask_app.__init__ import app
from flask_app.controllers import login_register
from flask_app.controllers import cars


if __name__ == '__main__':
    app.run(debug=True)