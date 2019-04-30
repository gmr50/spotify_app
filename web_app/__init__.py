# adapted from: https://github.com/prof-rossetti/products-api-flask/blob/csv/products_api/__init__.py

import os
import werkzeug
from dotenv import load_dotenv
from flask import Flask, render_template

from web_app.routes.home import home_routes

def create_app():
	load_dotenv()

	app_env = os.environ.get("FLASK_ENV", "development") # set to "production" in the production environment
	secret_key = os.environ.get("SECRET_KEY", "my super secret") # overwrite this in the production environment
	testing = False # True if app_env == "test" else False

	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(ENV=app_env, SECRET_KEY=secret_key, TESTING=testing)
	app.register_blueprint(home_routes)
	app.static_folder = 'static'



	#error handling
	@app.errorhandler(werkzeug.exceptions.NotFound)
	def handle_bad_request(e):
		return render_template("page_not_found.html"), 404

	@app.errorhandler(werkzeug.exceptions.Unauthorized)
	def handle_unauthorized_request(e):
		print("***")
		print(e)
		return render_template("page_not_found.html"), 401

	app.register_error_handler(404, handle_bad_request)
	app.register_error_handler(401, handle_unauthorized_request)





	return app

if __name__ == "__main__":
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	my_app = create_app()
	my_app.run(debug=True) # debug mode allows you to see printed content in development environment
