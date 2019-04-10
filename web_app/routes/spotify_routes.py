
from web_app.spreadsheet_service import get_products, create_product

from flask import Blueprint, request, render_template, jsonify, flash, redirect #, url_for

spotify_routes = Blueprint("spotify_routes", __name__)




@spotify_routes.route("/login/create")
def Execute():
    print("im Executing login script!!!")
    print("p")

    return redirect("/login")
