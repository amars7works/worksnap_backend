from reports.views import users_summary
from report.models import RemainingAccruedLeaves

def add_remaining_leaves(from_date,to_date,year,month,user_name):
	'''
		This Function will get the number of leaves taken by the employee
		 and add to the remaing leaves table
	'''
	users_list_remaining_leaves = { user.user.username:user.remaining_leaves \
					for user in RemainingAccruedLeaves.objects.all()}
	#sorted_remaining_leaves = dict(sorted(users_list_remaining_leaves.items()))
	all_users_data = users_summary(from_date,to_date,year,month,user_name)
	all_users_data = all_users_data[0].pop('s7_worksnaps')
	#sorted_all_users_data = dict(sorted(all_users_data.items()))
	for key,user_data in all_users_data.items():
		present_leaves = users_list_remaining_leaves.get(key) - user_data.get('No of leaves')
		#print(present_leaves,key)
		RemainingAccruedLeaves.objects.filter(user=key).update(remaining_leaves=present_leaves)
