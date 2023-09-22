# import face_recognition
from datetime import date
import json
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.db import connections
import requests
import xmltodict
from rest_framework.response import Response
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from djangoproject.api_app.models.models_SdTicket import SdTicket
# Create your views here.
def update():
    print("db updated")
    #if new user added
    #add encoding for that user

# Api Url
def ApiUrl():
    # url = '''http://10.83.152.184:8000/'''
    # url = '''http://43.204.98.242/'''
    # url = '''http://3.109.2.19/'''
    # url = '''http://10.83.152.184:8000/'''
    #  url = '''http://3.110.103.247/'''
     url = '''http://3.110.123.67/'''
     return url

def ApiGatewayUrl():
    url="https://8aj3hddov3.execute-api.ap-south-1.amazonaws.com/Production/"

    # https://z3ye58733c.execute-api.ap-south-1.amazonaws.com/Development/insert-pcv-engineer
    return url

#DB Connection
def db_connection():
    # server = '10.83.135.25'
    # database = 'ksubscribers'
    # username = 'chatbot'
    # password = 'Axsw@#$4321'
    # cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};TrustServerCertificate=YES;SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    # cursor = cnxn.cursor()
    cursor = connections['gsd'].cursor()
    return cursor

def trunc_table(table_name):
    table_name.objects.all().delete()
    
# push sd
def insert_sd():
        query = "SELECT id,ref FROM kasadmin.orgServDeskDefn"
        cursor = db_connection()
        cursor.execute(query)
        rows = cursor.fetchall()

        custom_url = ApiUrl()
        url = "{custom_url}api/add_sd/".format(custom_url = custom_url)
        headers = {
        "Content-type": "application/json"
        }
        for i in range(len(rows)):
            payload = {
            "objectid": str(rows[i][0]),
            "ref": rows[i][1]
            }
            print(payload)
            payload = json.dumps(payload)
            # models = SD(id=rows[i][0],ref=rows[i][1])
            response = requests.post(url=url, headers=headers, data=payload, verify=False)
            # print(response.text)
            # body = response.text
#Tickets
def insert_tickets():
    cursor = db_connection()
    # query = "SELECT t.id,t.TicketNumber,t.ServiceDesk, t.Status, t.Description, t.Stage, t.Category, t.Created, t.Severity, t.Summary, t.SubmitterName, t.SubmitterEmail, t.Organization, t.Modified, t.Due, c.String1 as engineername FROM ksd.CustomFieldsValues c inner join kasadmin.vSDTicket t on c.Id=t.id where (t.Status != 'Closed' AND t.Status != 'Resolved') OR (DATEPART(m, t.Modified) = DATEPART(m, DATEADD(m, -1, getdate())) AND DATEPART(yyyy, t.Modified) = DATEPART(yyyy, DATEADD(m, -1, getdate())))"
    query = "SELECT t.id,t.TicketNumber,t.ServiceDesk, t.Status, t.Description, t.Stage, t.Category, t.Created, t.Severity, t.Summary,t.SubmitterName, t.SubmitterEmail, t.Organization, t.Modified, t.Due, c.String1 as engineername FROM ksd.CustomFieldsValues c inner join kasadmin.vSDTicket t on c.Id=t.id where (t.Status != 'Closed' AND t.Status != 'Resolved') and datediff(HH,cast(t.Modified as datetime),cast(GETDATE() as datetime))<=24"
    # query1 = "SELECT * from kasadmin.vSDTicket"
    cursor.execute(query)
    # column=cursor.description
    # print('column',column)
    
    rows = cursor.fetchall()

    # Django Server
    # custom_url = ApiUrl()
    # url = "{custom_url}api/add_ticket/".format(custom_url = custom_url)
    headers = {
    "Content-type": "application/json"
    }
    # payload_obj = []
    # # print(len(rows))
    # for i in range(len(rows)):
    #     payload = {
    #         "objectid":str(rows[i][0]),
    #         "TicketNumber":rows[i][1],
    #         "ServiceDesk":rows[i][2],
    #         "Status":rows[i][3],
    #         "Description":rows[i][4],
    #         "Stage":rows[i][5],
    #         "Category":rows[i][6],
    #         "Created":str(rows[i][7]),
    #         "Severity":rows[i][8],
    #         "Summary":rows[i][9],
    #         "SubmitterName":rows[i][10],
    #         "SubmitterEmail":rows[i][11],
    #         "Organization":rows[i][12],
    #         "Modified":str(rows[i][13]),
    #         "Due":str(rows[i][14]),
    #         "Engineer":rows[i][15],
           
    #     }
    #     # print(url)
    #     # print(payload)
    #     # payload = json.dumps("helllo",payload,indent=4, sort_keys=True, default=str)
    #     payload_obj.append(payload)
    # # print(url)
    # data = {"data": payload_obj}
    #     # models = SD(id=rows[i][0],ref=rows[i][1])
    # response = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False)


    #1  API GATEWAY

    Customgateway_Url= ApiGatewayUrl()

    gateWayUrl="{Customgateway_Url}scheduler/".format(Customgateway_Url = Customgateway_Url)
    print('apiGateway!!!',rows[i][0])
    Api_gateway_payload_obj=[]
    for i in range(len(rows)):
        gatewaypayload = {
            "object":str(rows[i][0]),
            "ticketnumber":rows[i][1],
            "servicedesk":rows[i][2],
            "status":rows[i][3],
            "description":rows[i][4],
            "stage":rows[i][5],
            "category":rows[i][6],
            "created":str(rows[i][7]),
            "severity":rows[i][8],
            "summary":rows[i][9],
            "submitter_name":rows[i][10],
            "submitter_email":rows[i][11],
            "organization":rows[i][12],
            "modified":str(rows[i][13]),
            "due":str(rows[i][14]),
            "engineer":rows[i][15],
           
        }
        print("hello",gatewaypayload,gateWayUrl)
       
        Api_gateway_payload_obj.append(gatewaypayload)

    print("hello",)
    Gatewaydata = {"data": Api_gateway_payload_obj,"action":"insert_ticket"}
    
    response = requests.post(url=gateWayUrl, headers=headers, data=json.dumps(Gatewaydata), verify=False)
    print(response.text,'API GATEWAY RESPONSE!!!')


#Tickets
def insert_tickets_updated():
    cursor = db_connection()
    query = "SELECT t.id,t.TicketNumber,t.ServiceDesk, t.Status, t.Description, t.Stage, t.Category, t.Created, t.Severity, t.Summary,t.SubmitterName, t.SubmitterEmail, t.Organization, t.Modified, t.Due, c.String1 as engineername FROM ksd.CustomFieldsValues c inner join kasadmin.vSDTicket t on c.Id=t.id where (t.Status != 'Closed') and datediff(HH,cast(t.Modified as datetime),cast(GETDATE() as datetime))<=1"
    cursor.execute(query)
    rows = cursor.fetchall()


    # print('test-rowssss',rows)
    # custom_url = ApiUrl()
    # url = "{custom_url}api/add_ticket/".format(custom_url = custom_url)
   
    # payload_obj = []
    # # print(len(rows))
    # # print('rows',rows)
    # for i in range(len(rows)):
    #     payload = {
    #         "objectid":str(rows[i][0]),
    #         "TicketNumber":rows[i][1],
    #         "ServiceDesk":rows[i][2],
    #         "Status":rows[i][3],
    #         "Description":rows[i][4],
    #         "Stage":rows[i][5],
    #         "Category":rows[i][6],
    #         "Created":str(rows[i][7]),
    #         "Severity":rows[i][8],
    #         "Summary":rows[i][9],
    #         "SubmitterName":rows[i][10],
    #         "SubmitterEmail":rows[i][11],
    #         "Organization":rows[i][12],
    #         "Modified":str(rows[i][13]),
    #         "Due":str(rows[i][14]),
    #         "Engineer":rows[i][15]
    #     }
    #     # print(url)
    #     # payload = json.dumps(payload,indent=4, sort_keys=True, default=str)
    #     payload_obj.append(payload)
    # # print(url)
    # data = {"data": payload_obj}
    #     # models = SD(id=rows[i][0],ref=rows[i][1])
    # response = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False)



    # 2 API GATEWAY UPDATE TICKETS   # update_ticket_scheduler
    Customgateway_Url= ApiGatewayUrl()
    gatewayUrl="{Customgateway_Url}update_ticket_scheduler/".format(Customgateway_Url=Customgateway_Url)

    headers = {
    "Content-type": "application/json"
    }

    Api_gateway_payload_obj=[]
    for i in range(len(rows)):
        if rows[i][4] !=None:
            html_data="""{}""".format(rows[i][4])
            soup = BeautifulSoup(html_data,'html.parser')
            text=soup.get_text('\n')
            description=json.dumps(text).replace("'","")
        else:
            description=None

        # print("description \n",description,"\n ",rows[i][1],"\n")
        gatewaypayload = {
            "objectid":str(rows[i][0]),
            "ticketnumber":rows[i][1],
            "servicedesk":rows[i][2],
            "status":rows[i][3],
            "description":str(description),
            "stage":rows[i][5],
            "category":rows[i][6],
            "created":str(rows[i][7]),
            "severity":rows[i][8],
            "summary":rows[i][9],
            "submitter_name":rows[i][10],
            "submitter_email":rows[i][11],
            "organization":rows[i][12],
            "modified":str(rows[i][13]),
            "due":str(rows[i][14]),
            "engineer":rows[i][15],
           
        }
        print('body',gatewaypayload)
        
        Api_gateway_payload_obj.append(gatewaypayload)


    Gatewaydata = {"data": Api_gateway_payload_obj,"action":"update_ticket"}
   
    response = requests.post(url=gatewayUrl, headers=headers, data=json.dumps(Gatewaydata), verify=False)
    print('API GATEWAY UPDATE RESPONSE!!!',response.text)

def insert_SdStage():
        query = "SELECT id, codeRef, ref FROM kasadmin.SDStage"
        cursor = db_connection()
        cursor.execute(query)
        rows = cursor.fetchall()
        custom_url = ApiUrl()
        url = "{custom_url}api/add_stage/".format(custom_url = custom_url)
        headers = { 
        "Content-type": "application/json"
        }
        for i in range(len(rows)):
            payload = {
            "objectid": str(rows[i][0]),
            "coderef":rows[i][1],
            "ref": rows[i][2]
            }
            # print(url)
            payload = json.dumps(payload)
            # models = SD(id=rows[i][0],ref=rows[i][1])
            response = requests.post(url=url, headers=headers, data=payload, verify=False)

def insert_SdStatus():
        query = "SELECT id, codeRef, ref FROM kasadmin.SdStatus"
        cursor = db_connection()
        cursor.execute(query)
        rows = cursor.fetchall()
        custom_url = ApiUrl()
        url = "{custom_url}api/add_status/".format(custom_url = custom_url)
        headers = {
        "Content-type": "application/json"
        }
        for i in range(len(rows)):
            payload = {
            "objectid": str(rows[i][0]),
            "coderef":rows[i][1],
            "ref": rows[i][2]
            }
            # print(url)
            payload = json.dumps(payload)
            # models = SD(id=rows[i][0],ref=rows[i][1])
            response = requests.post(url=url, headers=headers, data=payload, verify=False)

def insert_SdPriority():
        query = "SELECT id, codeRef, ref FROM kasadmin.SdPriority"
        cursor = db_connection()
        cursor.execute(query)
        rows = cursor.fetchall()

        custom_url = ApiUrl()
        url = "{custom_url}api/add_prior/".format(custom_url = custom_url)
        headers = {
        "Content-type": "application/json"
        }
        for i in range(len(rows)):
            payload = {
            "objectid": str(rows[i][0]),
            "coderef":rows[i][1],
            "ref": rows[i][2]
            }
            print(url)
            payload = json.dumps(payload)
            # models = SD(id=rows[i][0],ref=rows[i][1])
            response = requests.post(url=url, headers=headers, data=payload, verify=False)

def insert_SdSeverity():
        query = "SELECT id, codeRef, ref FROM kasadmin.SdSeverity"
        cursor = db_connection()
        cursor.execute(query)
        rows = cursor.fetchall()
        custom_url = ApiUrl()
        url = "{custom_url}api/add_severity/".format(custom_url = custom_url)
        headers = {
        "Content-type": "application/json"
        }
        for i in range(len(rows)):
            payload = {
            "objectid": str(rows[i][0]),
            "coderef":rows[i][1],
            "ref": rows[i][2]
            }
            print(url)
            payload = json.dumps(payload)
            # models = SD(id=rows[i][0],ref=rows[i][1])
            response = requests.post(url=url, headers=headers, data=payload, verify=False)

def insert_PcvEng():
        query = "SELECT Email, EngineerName, EmployeeCode FROM pcv_Engineer"
        cursor = db_connection()
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # custom_url = ApiUrl()
        # url = "{custom_url}api/add_eng/".format(custom_url = custom_url)
        # print(url)
# https://z3ye58733c.execute-api.ap-south-1.amazonaws.com/Development/insert-pcv-engineer
        apiGateway_Url = ApiGatewayUrl()
        url = "{apiGateway_Url}insert-pcv-engineer/".format(apiGateway_Url=apiGateway_Url)
        headers = {
        "Content-type": "application/json"
        }
        Api_gateway_payload_obj=[]
        for i in range(len(rows)):
            gatewaypayload = {
            "Email": str(rows[i][0]),
            "EngineerName":rows[i][1],
            "EmployeeCode": rows[i][2]
            }
           
            Api_gateway_payload_obj.append(gatewaypayload)
            
        Gatewaydata = {"data": Api_gateway_payload_obj,"action":"insert_PcvEng"}    
        response = requests.post(url=url, headers=headers, data=json.dumps(Gatewaydata), verify=False)
        print("Insert PCV Engineer!!",response.text)
            

def insert_cusFields():
        query = "SELECT c.id, c.String1 FROM ksd.CustomFieldsValues c inner join kasadmin.vSDTicket t on c.Id=t.id where (t.Status != 'Closed' AND t.Status != 'Resolved') OR (DATEPART(m, t.Modified) = DATEPART(m, DATEADD(m, -1, getdate())) AND DATEPART(yyyy, t.Modified) = DATEPART(yyyy, DATEADD(m, -1, getdate())))"
        cursor = db_connection()
        cursor.execute(query)
        rows = cursor.fetchall()
        custom_url = ApiUrl()
        url = "{custom_url}api/add_field/".format(custom_url = custom_url)
        headers = {
        "Content-type": "application/json"
        }
        for i in range(len(rows)):
            payload = {
            "objectid": str(rows[i][0]),
            "String1":rows[i][1]
            }
            payload = json.dumps(payload)
            response = requests.post(url=url, headers=headers, data=payload, verify=False)

def cat_for_partition():
        query = "SELECT id, codeRef, ref, sdCategoryFK FROM [kasadmin].[fnGetCategoryFullPathForPartition] (1)"
        cursor = db_connection()
        cursor.execute(query)
        rows = cursor.fetchall()
        custom_url = ApiUrl()
        url = "{custom_url}api/category_partition/".format(custom_url = custom_url)
        headers = {
        "Content-type": "application/json"
        }
        # data = []
        # print("rowss", rows)
        for i in range(len(rows)):
            payload = {
            "id":str(rows[i][0]),"codeRef":rows[i][1],"ref":rows[i][2],"sdCategoryFK":str(rows[i][3])
            }
            payload = json.dumps(payload)
            print(payload)
            # data.append(payload)
            response = requests.post(url=url, headers=headers, data=payload, verify=False)

def cat_for_desk():
        query = "SELECT id,ref FROM kasadmin.orgServDeskDefn"
        cursor = db_connection()
        cursor.execute(query)
        rows = cursor.fetchall()
        for i in range(len(rows)):
            serviceDesk = rows[i][1]
            query = "SELECT id,codeRef, ref, Level FROM [kasadmin].fnGetCategoryFullPathForDesk('"+serviceDesk+"', 1)"
            cursor = db_connection()
            cursor.execute(query)
            rows = cursor.fetchall()
            custom_url = ApiUrl()
            url = "{custom_url}api/category_desk/".format(custom_url = custom_url)
            headers = {
            "Content-type": "application/json"
            }
            for i in range(len(rows)):
                payload = {
                "id":str(rows[i][0]),"codeRef":rows[i][1],"ref":rows[i][2],"Level":rows[i][3]
                }
                payload = json.dumps(payload)
                response = requests.post(url=url, headers=headers, data=payload, verify=False)





