import time
import requests
import base64
import logging
import ast
from datetime import datetime,timedelta,date
from calendar import monthrange
import xml.etree.ElementTree as ET

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets

from django.shortcuts import render
from django.http.response import JsonResponse
from django.db.models import Q
from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.contrib.auth.models import User

from reports.models import UserDailyReport


class daily_report(APIView):
    permission_classes(IsAuthenticated,)

    def post(self, request, format="json"):
        created_at = request.data.get("created_at", datetime.today())[:10]
        q1 = request.data.get("q1","Not filled!")
        q2 = request.data.get("q2","Not filled!")
        q3 = request.data.get("q3","Not filled!")
        q4 = request.data.get("q4","Not filled!")
        q5 = request.data.get("q5","Not filled!")
        UserDailyReport.objects.create(
            username=request.user.username,
            created_at=created_at,
            what_was_done_this_day=q1,
            what_is_your_plan_for_the_next_day = q2,
            what_are_your_blockers = q3,
            do_you_have_enough_tasks_for_next_three_days = q4,
            if_you_get_stuck_are_you_still_able_to_work_on_something_else = q5
        )
        return Response(status=status.HTTP_200_OK)

