import requests
import base64

from django.shortcuts import render
from django.http.response import JsonResponse

from reports.models import ProjectsList
# Create your views here.

def get_projects(url):
	token = '23Mh2bkhQkUoqlU0KDfpVaYg9wXXsSgHr7YKdSm8'
	project_url = 'https://api.worksnaps.com/api/{}.json'.format(url)
	client_token = '{}:{}'.format(token,"ignored").encode()
	headers = {
		'Authorization':'Basic'+' '+base64.b64encode(client_token).decode('utf-8'),
		'Accept':'application/json',
		'Content-Type':'application/json',
	}
	request_data = requests.get(project_url,headers=headers)
	# print(request_data,"project data")
	request_data_json = request_data.json()
	
	return request_data_json

def create_project(request):
	projects_qs = ProjectsList.objects.only('project_id')
	project_ids = [single_project.project_id for single_project in projects_qs]
	worksnaps_project = get_projects('projects')
	print(project_ids,"kliojiwk-[rgepmkgk-,o")
	for i,value in enumerate(worksnaps_project.get("projects")):
			if value.get('id',0) not in project_ids:
				print(value.get('id',0),"cooollllllll")
				ProjectsList.objects.create(
					project_id=value.get('id',''),project_name=value.get(
						'name',''),project_description=value.get(
						'description',''),project_status=value.get('status',''))

	return JsonResponse({"Refresh":"Success"})
