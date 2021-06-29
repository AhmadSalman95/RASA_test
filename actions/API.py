import requests
import json
import logging

def AddRequest(subject,description,email,name,mobile,ID_group):
    """ create request in manage engine 

    Args:
        subject (string): class of problem
        description (string): description of problem
        email (string): email of user
        name (string): name of user
        mobile (string): phone of user
        ID_group (string): id of group
    """
    # urlget = "https://ithelp.psau.edu.sa/api/v3/requests/{}"
    url = "https://ithelp.psau.edu.sa/api/v3/requests"
    # url = "https://demo.servicedeskplus.com/api/v3/requests"
    headers = {"technician_key": "054DBB7E-F913-441B-AFFA-E7139D2B4521"}
    # input_data = {
    #     "request": {
    #         "subject": subject,
    #         "description": description,
    #         "requester": {
    #             "email_id": email,
    #             "name": name,
    #             "mobile": mobile,
    #         },
    #         "group": {
    #             "id": ID_group
    #         }

    #     }
    # }
    input_data = {
            "request":{
            "subject":subject,
            "description":description,
            "requester":{
                "email_id":email
            },
            "request_type":{
                "id":"1"
            },
            "impact":{
                "id":"3"
            },
            "mode":{
                "id":"2"
            },
            "udf_fields":{
                "udf_sline_904":mobile,
                "udf_sline_903":"عمادة تقنية المعلومات وتعليم عن بعد"
            },
            "category":{
                "id":"1501"
            },
            "subcategory":{
                "id":"1845"
            },
            "group":{
                "id":ID_group
            }
            }
    }
    data = {'input_data': json.dumps(input_data)}
    logging.info("***********************: ".format(data))
    response = requests.post(url, headers=headers, data=data, verify=False)
    print(response.text)
    Json_Response=response.json()
    logging.info(Json_Response)
    ID_Of_Request = Json_Response["request"]["id"]
    return(ID_Of_Request)

def GetStatusFromRequest(IdOfRequest):
    """get of status request from manage engine

    Args:
        IdOfRequest (string): id of request
    """
    # url = "https://ithelp.psau.edu.sa/api/v3/requests/{}".format(IdOfRequest)
    headers = {"technician_key":"D2D76D61-11F1-4921-AA12-000C20AC77E8"}
    # headers = {"technician_key":"36F6AA36-710E-4B7C-A81E-83D1FB9EFAC9"}
    response = requests.get(url,headers=headers,verify=False)
    Json_Response=response.json()
    # Status_Of_Request = Json_Response["request"]["status"]["name"]
    Status_Of_Request = Json_Response["request"]
    print(Status_Of_Request)

# subject="blackboard"
# description = "i have problem in blackboared"
# email = "as@gmail.com"
# name = "Ahmad salman"
# mobile = "0599999999"
# ID_requster = "111"
# email_id_created= "blackboard@gmail.com"
# phone _created= "0000000000"
# name_created = "ChatBot"
# mobile_created = "0500000000"
# ID_created = "46505"
# ID_group = "1"




# ID_Of_Request = AddRequest(subject,description,email,name,mobile,ID_group)
# print("Id of request",ID_Of_Request)
# ID_Of_Request = 254
#GetStatusFromRequest(ID_Of_Request)