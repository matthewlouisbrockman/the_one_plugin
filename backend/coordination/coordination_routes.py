from flask import Blueprint, g, request, send_file
from wrappers.auth_required import auth_required
from models.jobs import TOPJob
from utils.json_helper import jsonify_payload
import pandas as pd
from models.job_results import TOPJobResult

bp = Blueprint("coordination", __name__, url_prefix="/coordination")

@bp.route("/initialize", methods=["GET"])
def start_tasks():
    return "We need to play hangman until we win. No ask just go."

@bp.route("/view_jobs", methods=["GET"])
@auth_required
def get_jobs_for_plugin():
    print('user info: ', g.user_id)

    jobs = TOPJob.find_by_user_id(g.user_id)

    jobs = [job.serialize() for job in jobs]

    jobs = [
        {
            'job_id': job['job_id'],
            'job_name': job['job_name'],
        } for job in jobs
    ]

    return jsonify_payload({'jobs': jobs})

@bp.route("/execute_job", methods=["POST"])
@auth_required
def execute_job():
    payload = request.get_json()

    job_id = payload.get('job_id')

    job = TOPJob.find_by_id(job_id)

    job = job.serialize()

    description = job['job_description']

    return jsonify_payload({'goal': description + "\n\nExecute the goal. No questions just go. If you encounter errors, try to troubleshoot, if you can't fix it just keep going through the rest of the tasks. Log the results after each section as an object {} back to  /coordination/log_results."})

@bp.route("/log_results", methods=["POST"])
@auth_required
def log_results():
    payload = request.get_json()

    job_id = payload.get('job_id')
    results = payload.get('results')
    if not results:
        results = payload.get("result")

    new_result = TOPJobResult(
        job_id,
        results,
        g.user_id
    )
    new_result.save()

    res = new_result.serialize()

    job_id = str(res.get('result_id'))

    host = request.headers['Host']
    url = f"{host}/coordination/download_results/{job_id}"

    return jsonify_payload({'hello': 'world', "url": url})

@bp.route("/download_results/<result_id>", methods=["GET"])
def download_results(result_id):

  result = TOPJobResult.find_by_id(result_id)

  result = result.serialize()

  results = result.get('result_data')

  print('results: ', results)

  df = pd.DataFrame(results)

  filename = f"results_{result_id}.xlsx"

  df.to_excel(filename, index=False)

  return send_file(filename, as_attachment=True)