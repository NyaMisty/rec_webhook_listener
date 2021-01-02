import json
from datetime import datetime

import dateutil.parser
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import *

def index(request):
    return HttpResponse("Hello, world from misty's vtbrec webhook listener")


# {"EventRandomId":"6b99e438-d9a6-42ef-9cc1-cbc2fc9bae24","RoomId":23058,"Name":"3号直播间","Title":"哔哩哔哩音悦台","RelativePath":"23058-3号直播间/录制-23058-20201220-205436-哔哩哔哩音悦台.flv","FileSize":296522,"StartRecordTime":"2020-12-20T20:54:36.9523326+08:00","EndRecordTime":"2020-12-20T20:54:37.4386879+08:00"}
@method_decorator(csrf_exempt, name='dispatch')
class BilirecHookView(View):
    def post(self, request):
        contributor = request.GET.get('i', None)
        if not contributor:
            return HttpResponse("Invalid request! please enclose your contributor name in url's 'i' parameter!", status=400)
        CRITICAL_KEYS = ["EventRandomId", "RoomId", "Name", "Title", "StartRecordTime", "EndRecordTime"]
        try:
            inputData = json.loads(request.body.decode("utf-8"))
            if any((c not in inputData for c in CRITICAL_KEYS)):
                return HttpResponse('Invalid json! At least you should have these in the json: ' + str(CRITICAL_KEYS), status=400)
        except json.JSONDecodeError:
            return HttpResponse('Failed to parse json input!', status=401)

        startDate = None
        endDate = None
        try:
            startDate = dateutil.parser.parse(inputData["StartRecordTime"])
            endDate = dateutil.parser.parse(inputData["EndRecordTime"])
        except:
            return HttpResponse('Failed to parse date!', status=400)
        rec = LiveRecRecord(
            rec_uuid=inputData["EventRandomId"],
            rec_type="bilirec",
            user_id="",
            room_id=inputData["RoomId"],
            user_name=inputData["Name"],
            live_title=inputData["Title"],
            start_date=startDate,
            end_date=endDate,
            rec_extra_data=json.dumps({k:v for k,v in inputData.items() if k not in CRITICAL_KEYS}, ensure_ascii=False),
            contributor_info=contributor
        )
        rec.save()
        return HttpResponse('Successfully received & saved record!')

@method_decorator(csrf_exempt, name='dispatch')
class VtbrecHookView(View):
    def post(self, request):
        contributor = request.GET.get('i', None)
        if not contributor:
            return HttpResponse("Invalid request! please enclose your contributor name in url's 'i' parameter!", status=400)
        CRITICAL_KEYS = ["uuid", "type", "provider", "user"]
        try:
            inputData = json.loads(request.body.decode("utf-8"))
            if any((c not in inputData for c in CRITICAL_KEYS)):
                return HttpResponse('Invalid json! At least you should have these in the json: ' + str(CRITICAL_KEYS), status=400)
        except json.JSONDecodeError:
            return HttpResponse('Failed to parse json input!', status=401)

        if inputData["type"] == "start":
            _, _, roomId = inputData.get("target", "").rpartition("/")

            startDate = datetime.now()

            rec = LiveRecRecord(
                rec_uuid=inputData["uuid"],
                rec_type="vtbrec-" + inputData["provider"],
                user_id=inputData["user"].get("TargetId"),
                room_id=roomId,
                live_title=inputData.get("title"),
                start_date=startDate,
                rec_extra_data=json.dumps({k:v for k,v in inputData.items() if k not in CRITICAL_KEYS}, ensure_ascii=False),
                contributor_info=contributor
            )
            rec.save()
            return HttpResponse('Successfully received & saved liveStart record!')
        elif inputData["type"] == "end":
            o = LiveRecRecord.objects.get(rec_uuid=inputData["uuid"])
            o.end_date = datetime.now()
            try:
                oriData = json.loads(o.rec_extra_data)
                for k,v in inputData.items():
                    if k not in CRITICAL_KEYS:
                        oriData[k] = v
                o.rec_extra_data = json.dumps(oriData, ensure_ascii=False)
            except:
                o.rec_extra_data = json.dumps({k:v for k,v in inputData.items() if k not in CRITICAL_KEYS}, ensure_ascii=False)
            o.save()
            return HttpResponse('Successfully received & saved liveEnd record!')
        else:
            return HttpResponse('Unknown type %s of webhook request!' % inputData["type"], status=400)