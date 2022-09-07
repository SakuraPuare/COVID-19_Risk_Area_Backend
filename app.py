from flask import Flask

import query
import version

risk_data = version.load_last_version()

app = Flask(__name__)


@app.route('/admin/refresh')
def refresh_admin():
	global risk_data
	risk_data = query.main()
	return "OK", 200


@app.errorhandler(404)
def page_not_found():
	return "Not found", 404


@app.errorhandler(403)
def forbidden():
	return "Forbidden", 403


@app.route('/api/search/<string:area>')
def api_search(area):
	search_results = {}
	for t in risk_data:
		search_results[t] = []
	for types, value in risk_data.items():
		for place, location in value.items():
			if area in place:
				search_results[types].append({'area': place, 'location': location})
	return {'data': search_results, 'status': '200'}


@app.route("/")
def hello_world():
	return {'msg': 'Hey! This is just an api', 'status': 200}


if __name__ == "__main__":
	app.run(debug=True, port=8080)
