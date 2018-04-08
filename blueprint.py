import requests
from global_variables import *

class Blueprint:
    run_blueprint_json = """
        {
           "blueprint_name": "%s",
           "team_name": "%s",
           "application_name": "%s"
         }
         """

    @staticmethod
    def run_blueprint(blueprint_name, team_name, application_name):
        run_blueprint_url = "/public/api/1/default/blueprints/run"
        json = (Blueprint.run_blueprint_json % (blueprint_name, team_name, application_name))

        response = requests.post(calm_base_url + run_blueprint_url,
                                 data=json,
                                 auth=(calm_username,calm_password),
                                 verify=False)
        return response.status_code
