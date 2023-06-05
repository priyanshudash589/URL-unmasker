import re,requests,json,urllib
from django.contrib import messages
from django.shortcuts import render,redirect   
from urllib.parse import urlencode
from urllib.request import urlretrieve 
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from googleapiclient.discovery import build
import base64
from .models import UnsafeURL
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UnsafeURLSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,RetrieveUpdateAPIView
from django.contrib.auth.mixins import LoginRequiredMixin
import pyshorteners




API_KEY = 'AIzaSyB-UHjPUoPnsLn-lsUssooU7KPcOa_FTgI'
API_NAME = 'safebrowsing'
API_VERSION = 'v4'
CLIENT_ID = '697996555078-esioiq515iqvqob5g2acts129gotd4pq.apps.googleusercontent.com'
CLIENT_VERSION = '1.0.0'


# Create your views here.

def is_short_url(s_url):
    pattern = r"(?i)^https?://(?:www\.)?(?:bit\.ly|tinyurl\.com|l.instagram\.com|forms\.gle|t\.co|lnkd\.in|ow\.ly|goo\.gl|buz\.me|ad\.f.ly|adcrun\.ch|adfoc\.us|adf\.ly|adfoc\.es|admy\.link|bc\.vc|coinurl\.com|cur\.lv|cutt\.us|cutt\.ly|gg\.gg|is\.gd|ix\.st|j\.gs|j\.mp|krunchd\.com|lc\.cx|link\.zip\.net|moourl\.com|ow\.ly|po\.st|q\.gs|qr\.ae|qr\.net|snip\.li|snipurl\.com|soo\.gd|su\.pr|t\.cn|t\.co|t2m\.io|tiny\.cc|tinyurl\.com|tny\.im|tr\.im|trde\.es|twitthis\.com|u\.to|v\.gd|vzturl\.com|w\.tc|x\.co|yep\.it|zi\.ps|zpag\.es)/?[^\s/$.?#].[^\s]*$"
    if re.match(pattern, s_url):
        return True
    else:
        return False

def get_original_url(short_url):
    response = requests.head(short_url, allow_redirects=True)
    return response.url



class IPQS:
    key = 'uGnBVtNE7397wJ3zcTJ88TWnt13RaA0Q'
    def malicious_url_scanner_api(self, url: str, vars: dict = {}) -> dict:
        url = 'https://www.ipqualityscore.com/api/json/url/%s/%s' % (self.key, urllib.parse.quote_plus(url))
        x = requests.get(url, params = vars)
        # print(x.text)
        return (json.loads(x.text))


def is_phishing(url):
    service = build(API_NAME, API_VERSION, developerKey=API_KEY)
    threat_info = {
        "threatTypes": ["SOCIAL_ENGINEERING", "MALWARE",'POTENTIALLY_HARMFUL_APPLICATION','UNWANTED_SOFTWARE','THREAT_TYPE_UNSPECIFIED'],
        "platformTypes": ["ANY_PLATFORM"],
        "threatEntryTypes": ["URL"],
        "threatEntries": [{"url": url}]
    }
    request_body = {
        "client": {
            "clientId": CLIENT_ID,
            "clientVersion": CLIENT_VERSION
        },
        "threatInfo": threat_info
    }
    response = service.threatMatches().find(body=request_body).execute()
    if "matches" in response:
        for match in response["matches"]:
            print("Phishing URL found: ", match["threat"]["url"])
        return True
    else:
        return False


@xframe_options_exempt
@csrf_exempt
def home(request):
    if request.method == "POST":
        input_url = request.POST.get('uname')
        print(type(input_url))

        # check if url is short or not

        if is_short_url(input_url) == True:
            original_link = get_original_url(input_url)

            print(original_link)

            strictness = 2

            #custom feilds
            additional_params = {
                'strictness' : strictness
            }


            ipqs = IPQS()
            result = ipqs.malicious_url_scanner_api(f"{original_link}", additional_params)

   

            params = urlencode(dict(access_key="601a514c968647c8a9b74ff0dfea3a42",
                                    url=f"{original_link}"))
            ss = "https://api.apiflash.com/v1/urltoimage?" + params

            print(is_phishing(original_link))

    
            if result['unsafe'] == False and is_phishing(original_link) == True :
               
                result['unsafe'] = True
                result['malware'] = True
                result['suspicious'] = True
                result['phishing'] = True
                result['risk_score'] = 100
            
            # elif result['unsafe'] == True or result['suspicious'] == True and is_phishing(original_link) == False:
            #     result['unsafe'] = False
            #     result['malware'] = False
            #     result['suspicious'] = False
            #     result['phishing'] = False
            #     result['risk_score'] = 100



            if is_phishing(original_link) == True or result['suspicious'] == True:
                try:
                    check_data = UnsafeURL.objects.get(origianl_url=original_link)
                except ObjectDoesNotExist:
                    data = UnsafeURL(short_url=input_url, origianl_url=original_link, status="Unsafe")
                    data.save()

            



            return render(request,"urlunmasker/result.html",{"original_url":original_link,"security_details":result,
            "ss":ss,'short_url':input_url})

        
        


        else:
            messages.warning(request,"Please a short URL to unmask")
            return redirect('home')




    unsafe_data = UnsafeURL.objects.all()


    return render(request,"urlunmasker/home.html",{"unsafe_data":unsafe_data})


@xframe_options_exempt
@csrf_exempt
def chrome_req(request):
    if request.method == "POST":
        original_link = request.POST.get('url')
        print(original_link)
        strictness = 2
        #custom feilds
        additional_params = {
            'strictness' : strictness
        }

        ipqs = IPQS()
        result = ipqs.malicious_url_scanner_api(f"{original_link}", additional_params)
        params = urlencode(dict(access_key="601a514c968647c8a9b74ff0dfea3a42",
                                url=f"{original_link}"))
        ss = "https://api.apiflash.com/v1/urltoimage?" + params

        print(is_phishing(original_link))

        if result['unsafe'] == False and is_phishing(original_link) == True :
            
            result['unsafe'] = True
            result['malware'] = True
            result['suspicious'] = True
            result['phishing'] = True
            result['risk_score'] = 100
        
        elif result['unsafe'] == True or result['suspicious'] == True and is_phishing(original_link) == False:
            result['unsafe'] = False
            result['malware'] = False
            result['suspicious'] = False
            result['phishing'] = False
            result['risk_score'] = 100



        if result['suspicious'] == True:
            try:
                check_data = UnsafeURL.objects.get(origianl_url=original_link)
            except ObjectDoesNotExist:
                data = UnsafeURL(short_url=None, origianl_url=original_link, status="Unsafe")
                data.save()


        return render(request,"urlunmasker/result.html",{"original_url":original_link,"security_details":result,
        "ss":ss,'short_url':None})


        # else:
        #     messages.warning(request,"Please a short URL to unmask")
        #     return redirect('home')

    unsafe_data = UnsafeURL.objects.all()

    return render(request,"urlunmasker/home.html",{"unsafe_data":unsafe_data})



def create_safe_short_urls(request):
    if request.method == "POST":
        input_url = request.POST.get('lurl')

        if UnsafeURL.objects.filter(origianl_url=input_url).exists():
            messages.warning(request,"We won't allow you to shorten this site since this was marked as UNSAFE by our Service")
            return redirect('safeshorturls')
        elif bool(UnsafeURL.objects.filter(origianl_url=input_url).exists()) == False:

            strictness = 2

            #custom feilds
            additional_params = {
                'strictness' : strictness
            }

            ipqs = IPQS()
            result = ipqs.malicious_url_scanner_api(f"{input_url}", additional_params)


            if result['unsafe'] == True or result['malware'] == True or result['suspicious'] == True or result['phishing'] == True or result['risk_score'] >=35:

                params = urlencode(dict(access_key="601a514c968647c8a9b74ff0dfea3a42",
                                    url=f"{input_url}"))
                ss = "https://api.apiflash.com/v1/urltoimage?" + params

                try:
                    check_data = UnsafeURL.objects.get(origianl_url=input_url)
                except ObjectDoesNotExist:
                    data = UnsafeURL(short_url=None, origianl_url=input_url, status="Unsafe")
                    data.save()


                messages.warning(request,"We won't allow you to shorten this site since this was marked as UNSAFE by our Service")


                return render(request,"urlunmasker/result.html",{"original_url":input_url,"security_details":result,
                "ss":ss,'short_url':None})
                
            elif result['adult'] == True:
                messages.warning(request,"Site may have some adult content")
                return redirect('safeshorturls')

            else:
                s = pyshorteners.Shortener(api_key='e2d087c4211fe4848311a7278bfbb0302d7073ff')
                safe_short_url = s.bitly.short(input_url)
                return render(request,'urlunmasker/safeshort.html', {'gen_url':safe_short_url})



    return render(request,'urlunmasker/safeshort.html')




#https://djangostars.com/blog/rest-apis-django-development/
class unsafeurls(ListCreateAPIView):
    """
    API view to retrieve list of posts or create new
    """
    serializer_class = UnsafeURLSerializer
    queryset = UnsafeURL.objects.all()

class unsafeurls_details(RetrieveUpdateAPIView):
    """
    API view to retrieve, update or delete post
    """
    serializer_class = UnsafeURLSerializer
    queryset = UnsafeURL.objects.all()