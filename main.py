# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import subprocess
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from datetime import datetime

class MainPage(webapp2.RequestHandler):
	compute = discovery.build('compute','v1',
		credentials=GoogleCredentials.get_application_default())
	resource_manager = discovery.build('cloudresourcemanager','v1',
		credentials=GoogleCredentials.get_application_default())
	def list_projects():
		projects = []
		request = resource_manager.projects().list()
		response = request.execute()
		projects_list = response.get('projects', {})
		for project in projects_list:
			if project['lifecycleState'] == "ACTIVE":
				projects.append(project['projectId'])
		return projects
                                                        
                                                        
	def list_instances(project_id):
		request = compute.instances().aggregatedList(project=project_id)
		response = request.execute()
		zones = response.get('items', {})
		instances = []
		for zone in zones.values():
			for instance in zone.get('instances', []):
				if instance['status'] == 'RUNNING':
					instances.append(instance)
		return instances
	
	def list_projects1():
		project_lst = []
		proc = subprocess.Popen(["gcloud projects list", ""], stdout=subprocess.PIPE, shell=True)
		(project_names, err) = proc.communicate()
		#print "program output:", project_names
		# print project_names
		for project in project_names.splitlines():
			project_name =  project.split(' ', 1)[0]
			project_lst.append(project_name)
		project_lst = project_lst[1:]
		return project_lst

	def main():
		x = list_projects1()
		print x
		for project in x:
			print project
			y = list_instances(project)
			count = 1
			for instance in y:
				print count, instance['name']
				count += 1

	if __name__== "__main__":
		main()
	

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
