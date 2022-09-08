import json

from flask import Flask

import query
import version

risk_data = version.load_last_version()

app = Flask(__name__)


@app.route('/admin/refresh/')
def refresh_admin():
        print('Start to Refresh')
        global risk_data
        risk_data = query.main()
        print('Refresh Success')


@app.errorhandler(404)
def page_not_found():
	return "Not found", 404


@app.errorhandler(403)
def forbidden():
	return "Forbidden", 403


@app.route('/time')
def api_time():
	v = [i.split('/')[-1] for i in version.list_version()]
	return json.dumps(v)


@app.route('/search/<string:area>')
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
	return 'Hey! This is just an api'


if __name__ == "__main__":
	app.run(port=7410)
