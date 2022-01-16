import pysolr
from flask import *

from index_actions import *
from main import main
from main_backoffice import main_backoffice

from apscheduler.schedulers.background import BackgroundScheduler


###
#   Background task that sends a request every X time and if the response is not null then update the index with
#   the meta_references passed in the response.
###
def check_site_updates():
    print("Checking for newly added/updated pages!")
    solr = pysolr.Solr('')
    if is_updated(solr):
        pass


###
#   Run the background task and initialize Flask app
###
sched = BackgroundScheduler(daemon=True)
sched.add_job(check_site_updates(), 'interval', minutes=60)
sched.start()

app = Flask(__name__)


###
#   Sub-url to perform Solr index actions
#   If a user enters the site the main.py file is called, executing the specified action, in the action url parameter.
#   If an action needs a meta_reference (such as add, reset_category or remove), an additional parameter is asked.
###
@app.route('/add_to_solr_index/', methods=["GET"])
def add_to_solr_index():
    action = request.args.get('action', default='add', type=str)
    meta_reference = request.args.get('meta_reference', default='A1', type=str)
    print(action + "   " + meta_reference)
    main([action, meta_reference])
    return jsonify(
        action=action,
        meta_reference=meta_reference,
        status=200
    )

@app.route('/add_to_solr_index_backoffice/', methods=["GET"])
def add_to_solr_index_backoffice():
    action = request.args.get('action', default='add', type=str)
    meta_reference = request.args.get('meta_reference', default='A1', type=str)
    print(action + "   " + meta_reference)
    main_backoffice([action, meta_reference])
    return jsonify(
        action=action,
        meta_reference=meta_reference,
        status=200
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
