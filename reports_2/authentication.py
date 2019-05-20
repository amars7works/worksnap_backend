from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailAuthBackend(ModelBackend):

	'''
		Custom Authentication backed to let user log in 
		using both username (case insensitive) or email id
	'''
	
	def authenticate(self, request, username=None, password=None, **kwargs):
		UserModel = get_user_model()
		if username is None:
		    username = kwargs.get(UserModel.USERNAME_FIELD)
		try:
			user = UserModel._default_manager.get(email = username)
			if user.check_password(password):
				return user
		except UserModel.DoesNotExist:
			try:
				case_insensitive_username_field = "{}__iexact".format(UserModel.USERNAME_FIELD)
				user = UserModel._default_manager.get(**{case_insensitive_username_field:username})
				if user.check_password(password):
					return user
			except UserModel.DoesNotExist:
				# Run the default password hasher once to reduce the timing
	            # difference between an existing and a non-existing user 
	            # (security bug #20760).
				UserModel().set_password(password)
			else:
				if user.check_password(password) and self.user_can_authenticate(user):
					return user

	def get_user(self,user_id):
		try:
			UserModel = get_user_model()
			return UserModel._default_manager.get(pk = user_id)
		except UserModel.DoesNotExist:
			return None



