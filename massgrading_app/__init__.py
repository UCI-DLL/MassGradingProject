import os
import openai

from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
from .utils.chatgpt_client import ChatGPTClient

load_dotenv('.flaskenv')
load_dotenv('.env')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    assert os.getenv('API_KEY', None) is not None and os.getenv('ORG_ID', None) is not None
    openai.api_key = os.getenv('API_KEY', None)
    openai.organization = os.getenv('ORG_ID', None)

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/fetch_dir_path', methods=["POST"])
    def directory_selection():
        dir_name = request.get_json().get('dir_name')
        full_path = os.path.abspath(os.path.join(os.getcwd(), app.name, "static", "files", dir_name))
        return jsonify({'message': f'Selected directory full path:\n {full_path}'})

    @app.route('/grading', methods=["POST"])
    def process_grading():
        data = request.get_json()
        dir_name, temp_val = data.get('dir_name'), data.get('temp_val')

        # check up input
        if not dir_name or not 0 <= temp_val <= 2:
            return jsonify({'message': 'You have not selected a directory yet.'}), 400

        full_dir_path = os.path.abspath(os.path.join(os.getcwd(), app.name, "static", "files", dir_name))

        client = ChatGPTClient(full_dir_path, temp_val)
        client.grading()

        return jsonify({'message': f'Grading Completed. See artifacts under: {client.get_outcome_dirname()}'}), 200

    return app
