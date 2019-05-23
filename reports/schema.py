import graphene
from graphene_django.types import DjangoObjectType
from graphene import relay

from reports.models import ProjectsList,\
							UsersList,\
							UsersSummaryReport,\
							HolidayList,\
							UserDailyReport,\
							UserProfile
from graphene_django.filter import DjangoFilterConnectionField

class ProjectsListType(DjangoObjectType):
    class Meta:
        model = ProjectsList

class UsersListType(DjangoObjectType):
    class Meta:
        model = UsersList

class UsersSummaryReportType(DjangoObjectType):
    class Meta:
        model = UsersSummaryReport


class HolidayListType(DjangoObjectType):
    class Meta:
        model = HolidayList

class UserDailyReportNode(DjangoObjectType):
    class Meta:
        model = UserDailyReport
        filter_fields = {
                         'username': ['exact', 'icontains', 'istartswith'],
                         'created_at':['exact', 'icontains'],
                        }
        interfaces = (relay.Node, )

class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile

class Query(object):
    daily_report = relay.Node.Field(UserDailyReportNode)
    all_projects_list = graphene.List(ProjectsListType)
    all_users_list = graphene.List(UsersListType)
    all_users_summart_report = graphene.List(UsersSummaryReportType)
    all_holiday_list = graphene.List(HolidayListType)
    #all_daily_report = graphene.List(UserDailyReportType)
    all_profile = graphene.List(UserProfileType)

    all_daily_report = DjangoFilterConnectionField(UserDailyReportNode)

    def resolve_projects_list(self, info, **kwargs):
        return ProjectsList.objects.all()

    def resolve_all_users_list(self, info, **kwargs):
        return UsersList.objects.all()

    def resolve_all_users_summart_report(self, info, **kwargs):
        return UsersSummaryReport.objects.all()

    def resolve_all_holiday_list(self, info, **kwargs):
        return HolidayList.objects.all()

    def resolve_all_daily_report(self, info, **kwargs):
        print(kwargs,"key word arguments")
        username = kwargs.get("username")
        created_at = kwargs.get("created_at")
        print(username,type(username))
        print(created_at,type(created_at))
        if username and created_at:
                print("entered into both user and created")
                return UserDailyReport.objects.filter(username__icontains=username,created_at=created_at)
        elif username:
                print("entered into user")
                return UserDailyReport.objects.filter(username__icontains=username)
        else:
                print("no user")
                return UserDailyReport.objects.all()

    def resolve_all_profile(self, info, **kwargs):
        return UserProfile.objects.all()
