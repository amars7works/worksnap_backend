import graphene
from graphene_django.types import DjangoObjectType

from reports.models import ProjectsList,\
							UsersList,\
							UsersSummaryReport,\
							HolidayList,\
							UserDailyReport,\
							UserProfile


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

class UserDailyReportType(DjangoObjectType):
    class Meta:
        model = UserDailyReport

class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile

class Query(object):
    all_projects_list = graphene.List(ProjectsListType)
    all_users_list = graphene.List(UsersListType)
    all_users_summart_report = graphene.List(UsersSummaryReportType)
    all_holiday_list = graphene.List(HolidayListType)
    all_daily_report = graphene.List(UserDailyReportType)
    all_profile = graphene.List(UserProfileType)

    def resolve_projects_list(self, info, **kwargs):
        return ProjectsList.objects.all()

    def resolve_all_users_list(self, info, **kwargs):
        return UsersList.objects.all()

    def resolve_all_users_summart_report(self, info, **kwargs):
        return UsersSummaryReport.objects.all()

    def resolve_all_holiday_list(self, info, **kwargs):
        return HolidayList.objects.all()

    def resolve_all_daily_report(self, info, **kwargs):
        return UserDailyReport.objects.all()

    def resolve_all_profile(self, info, **kwargs):
        return UserProfile.objects.all()