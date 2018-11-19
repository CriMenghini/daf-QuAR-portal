from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for


import ast
import json
import datetime
import numpy as np
import pandas as pd
from collections import defaultdict


import static.src.write_credentials
from static.src.utils import valori_dict


print(valori_dict)

list_centraline = ["Francia", "Preneste", "Malagrotta", "Villa Ada", "Castel di Guido","Cavaliere","Fermi","Bufalotta","Cipro","Magna Grecia","Tiburtina",
"Arenula", "Cinecitta"]

with open('static/data/portale_values.js', 'w') as f:
	f.write('var listaCentraline = [')
	for c in list_centraline:
		f.write("{'" + str(c) + "':" +str(int(valori_dict[c])) + '},')

	f.write(']')


app = Flask(__name__,
			template_folder='templates/',
			static_folder='static/',
			static_url_path='')


@app.route("/")
def home_page():
	return render_template('index_portale.html')


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)
