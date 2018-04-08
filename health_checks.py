import requests
import json
from global_variables import *

class HealthChecks:

    @staticmethod
    def get_health_checks():
        get_health_checks_url = "/api/nutanix/v2.0/health_checks/"
        response = requests.get(base_url + get_health_checks_url,
                                auth = (username,password),
                                verify=False)

        parsed_response = json.loads(response.text)
        return parsed_response["entities"]
