import requests
import json
from global_variables import *

class Tasks:

    task_post_json = """
        {
          "cut_off_time_usecs": 0,
          "include_completed": true,
          "include_subtasks_info": true
        }
    """

    @staticmethod
    def get_tasks():
        get_tasks_url = "/api/nutanix/v2.0/tasks/list"
        response = requests.post(base_url + get_tasks_url,
                                data = Tasks.task_post_json,
                                auth = (username,password),
                                verify=False)

        parsed_response = json.loads(response.text)
        return parsed_response["entities"]
