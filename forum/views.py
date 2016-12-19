from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Survey, SurveyOffer, FeedbackFromOnePreson
from .forms import PostForm, SurveyForm, SurveyOfferForm, UserSelectorForm
from django.template import loader
from django.db.models import F
from settings import *
import numpy as np
import json
import collections
#log/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django import db
from django.db import transaction
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.yui import BarChart
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating
#@login_required(login_url="login/")
#def home(request):
#    return render(request,"home.html")


def welcome(request):
    #users = User.objects.all()
    #form = UserSelectorForm(request.POST or None, extra=users)
    #SELECTED_USER = 'None'
    if request.method == "POST":
        if 'newsurvey' in request.POST:
            form =  UserSelectorForm(request.POST or None)
            if form.is_valid():
                request.session["user_id"] = form.cleaned_data['user'].id
                return redirect('index')

    form = UserSelectorForm(request.POST or None)
    template = loader.get_template('forum/welcome.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))

def index(request):
    if(request.session.get('user_id') is None and not request.user.is_authenticated()):
        return redirect('welcome')
    if request.user.is_authenticated():
        request.session["user_id"] = request.user.id
        #welcome(request)
    user = User.objects.get(id=request.session.get('user_id'))
    """Main listing."""
    if request.method == "POST":
        if 'newpost' in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = user
                post.save()
                return redirect('index')
    else:
        form = PostForm()

    latest_post_list = Post.objects.filter(user=user).order_by('-id')[:10]
    template = loader.get_template('forum/index.html')
    context = {
        'latest_post_list': latest_post_list,
        'form': form,
    }
    return HttpResponse(template.render(context, request))
"""
def survey(request):
    latest_survey_list = Post.objects.all()
    template = loader.get_template('forum/survey.html')
    context = {
        'latest_survey_list': latest_survey_list,
    }
    return HttpResponse(template.render(context, request))
    """

def flush_transaction():
    transaction.commit()


def existing_survey(request):
    if(request.session.get('user_id') is None and not request.user.is_authenticated()):
        return redirect('welcome')
    if not request.user.is_authenticated():
        return redirect('welcome')
    if request.user.is_authenticated():
        request.session["user_id"] = request.user.id
    user_id = request.session.get('user_id')
    template = loader.get_template('forum/existing_survey.html')
    context = {
        'user_id' : user_id,
    }
    return HttpResponse(template.render(context, request))

def prepare(request):
    if(request.session.get('user_id') is None and not request.user.is_authenticated()):
        return redirect('welcome')
    if not request.user.is_authenticated():
        return redirect('welcome')
    if request.user.is_authenticated():
        request.session["user_id"] = request.user.id

    survey_offer_form = SurveyOfferForm()
    if request.method == "POST":
        if 'newsurvey' in request.POST:
            get_questions(request)
            template = loader.get_template('forum/prepare.html')
            context = {
                'survey_offer_form' : survey_offer_form,
            }
            return HttpResponse(template.render(context, request))
    template = loader.get_template('forum/prepare.html')
    context = {
        'survey_offer_form' : survey_offer_form,
    }
    return HttpResponse(template.render(context, request))

"""
@csrf_protect
def get_selected_survey(request):
    if request.is_ajax():
        # extract your params (also, remember to validate them)
        flush_transaction()

        mid = request.POST.get('id', None)

        # construct your JSON response by calling a data method from elsewhere
        survey = SurveyOffer.objects.get(survey_id = mid )

        return HttpResponse(json.dumps({'result': 'OK', 'data': {'title': survey.title, 'questions': survey.questions}}), content_type="application/json")
    return HttpResponseBadRequest()
"""
def get_statistics(request):
    if(request.session.get('user_id') is None and not request.user.is_authenticated()):
        return redirect('welcome')
    if not request.user.is_authenticated():
        return redirect('welcome')
    if request.user.is_authenticated():
        request.session["user_id"] = request.user.id

    #statistics bossa kontrolu eklenmeli
    #FeedbackFromOnePreson.objects.all().delete()
    statistics1 = ""
    statistics2 = ""
    i = 0
    user = User.objects.get(id=request.session.get('user_id'))
    statistic_list = []
    statistic_list_values = []
    new = []
    data_list = []
    keys = []
    values = []
    if not SurveyOffer.objects.filter(user=user):
        return redirect('prepare')
    s = SurveyOffer.objects.filter(user=user).latest('survey_id')
    survey_id = s.survey_id
    survey_title = s.title
    if not FeedbackFromOnePreson.objects.filter(user = user):
        return redirect('survey')
    if not FeedbackFromOnePreson.objects.filter(survey_id = survey_id):
        return redirect('survey')
    for answers in FeedbackFromOnePreson.objects.filter(user = user, survey_id = survey_id):
        statistics1+= answers.result_key
        statistics2+= answers.result_value
        new.append(answers.survey_id)
        if(i == 0): #do it for first time
            keys_unicode = answers.result_key.split("~")
            keys_unicode.remove('')
            keys = [x.encode('UTF8') for x in keys_unicode]
            i += 1
            #statistic_list.append(["Questions"] + keys)
        values_str =  answers.result_value.split("~")
        values_str.remove('')
        values = [int(s) for s in values_str]
        #statistic_list.append(values)
        statistic_list_values.append(values)
    matrx = np.array(statistic_list_values)
    row_list = ['Questions',"Strongly Disagree","Disagree","Neutral","Agree","Strongly Agree"]
    data_list.append(row_list)
    t=0
    for key in keys:
        occ = collections.Counter(matrx[:,t]) #occurences of every choise in questiont
        row_list = []
        row_list.append(key)
        row_list.append(0 if occ.get(1) is None else occ.get(1))
        row_list.append(0 if occ.get(2) is None else occ.get(2))
        row_list.append(0 if occ.get(3) is None else occ.get(3))
        row_list.append(0 if occ.get(4) is None else occ.get(4))
        row_list.append(0 if occ.get(5) is None else occ.get(5))
        data_list.append(row_list)
        t+=1


    """
    data =  [
        ['Year', 'Sales', 'Expenses'],
        ['2004', 1000, 400],
        ['2004', 1170, 460],
        ['2004', 660, 1120],
        ['2004', 1030, 540]
    ]
    """
    data_source = SimpleDataSource(data=data_list)
    chart = BarChart(data_source)
    context = {
        'statistics1' : statistics1,
        'statistics2' : statistics2,
        'i' : i,
        'chart': chart,
        'keys' : keys,
        'values' : values,
        'statistic_list' : statistic_list,
        'title': survey_title,
        #'column0' : column0,
        #'column1' : column1,
        #'nof1' : numOf1,
        #'nof2' : numOf2,
        #'nof3' : numOf3,
        #'occurences' : occurences,
        'new' : new,
        #'matrx' : matrx,
    }
    template = loader.get_template('forum/statistics.html')
    return HttpResponse(template.render(context, request))

def get_surveys(request):
    if(request.session.get('user_id') is None and not request.user.is_authenticated()):
        return redirect('welcome')
    if request.user.is_authenticated():
        request.session["user_id"] = request.user.id
    #id = urllib.quote(user_id, safe='')
    #user = User.objects.get(id=id)
    user = User.objects.get(id=request.session.get('user_id'))
    if request.is_ajax():
        q = request.GET.get('term', '')
        surveys = SurveyOffer.objects.filter(title__icontains = q, user = user)[:20]
        results = []
        for survey in surveys:
            survey_json = {}
            survey_json['id'] = survey.survey_id
            survey_json['label'] = survey.title
            survey_json['value2'] = survey.questions
            results.append(survey_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_questions(request):

    user = User.objects.get(id=request.session.get('user_id'))
    surver_offer_form = SurveyOfferForm(request.POST)
    if surver_offer_form.is_valid():
        #SurveyOffer.objects.all().delete()
        surver_offer = surver_offer_form.save(commit=False)
        surver_offer.user = User.objects.get(id=request.session.get('user_id'))
        surver_offer.save()
    #return redirect('survey')
    return

@csrf_exempt
def reactivate(request):
    if(request.session.get('user_id') is None and not request.user.is_authenticated()):
        return redirect('welcome')
    if request.user.is_authenticated():
        request.session["user_id"] = request.user.id
    user = User.objects.get(id=request.session.get('user_id'))
    survey_id = request.POST.get('survey_id')
    title = request.POST.get('survey_title')
    questions = request.POST.get('survey_questions')
    SurveyOffer.objects.filter( survey_id = int(survey_id)).delete()
    surver_offer = SurveyOffer(user = user, title = title, questions = questions)
    surver_offer.save()
    return HttpResponse(request)

def survey(request):
    if(request.session.get('user_id') is None and not request.user.is_authenticated()):
        return redirect('welcome')
    if request.user.is_authenticated():
        request.session["user_id"] = request.user.id
    user = User.objects.get(id=request.session.get('user_id'))
    #extra_questions = ['placeholder','placeholder']
    extra_questions = []
    s_id = [0]
    s_title = "placeholder"
    if request.method == "POST":
        if 'newsurvey' in request.POST:
            get_questions(request)
        if 'submit' in request.POST:
            survey_form = SurveyForm(request.POST, extra=extra_questions, survey_id=s_id, survey_title=s_title)
            if survey_form.is_valid():
                s1 = ""
                s2 = ""
                feedbackFromOnePerson = FeedbackFromOnePreson(user = user, survey_id=survey_form.cleaned_data['survey_id'])
                t = 0
                for i in range(15):
                    if(request.POST.get('choices_'+str(i))):
                        t+=1
                        s2+=str(i+1)
                        s1+=request.POST.get('choices_'+str(i))
                        feedbackFromOnePerson.result_key += "~"+ 'question_'+str(i+1)
                        feedbackFromOnePerson.result_value += "~"+ request.POST.get('choices_'+str(i))
                    else:
                        break;

                result_key = feedbackFromOnePerson.result_key
                value_key = feedbackFromOnePerson.result_value
                feedbackFromOnePerson.save()
                context = {
                    'result' : survey_form.__dict__.iteritems(),
                    's1' : s1,
                    's2' : s2,
                    'result_key':result_key,
                    'value_key':value_key,
                    'i' : t
                }
                template = loader.get_template('forum/result.html')
                return HttpResponse(template.render(context, request))

    if SurveyOffer.objects.filter(user=user):
        if SurveyOffer.objects.filter(user=user).latest('survey_id'):
            s = SurveyOffer.objects.filter(user=user).latest('survey_id')
            if s:
                extra_questions = s.questions.split("~")
                extra_questions = filter(None, extra_questions)
                s_id = s.survey_id
                s_title = s.title

    survey_offer_form = SurveyOfferForm()
    form = SurveyForm(request.POST or None, extra=extra_questions, survey_id=s_id, survey_title = s_title)
    template = loader.get_template('forum/survey.html')
    context = {
        'form' : form,
        'survey_offer_form' : survey_offer_form,
    }

    if form.is_valid():
        for (question, answer) in form.extra_answers():
            save_answer(request, question, answer)
        return redirect('index')

    return HttpResponse(template.render(context, request))

def upvote(request):
    if(request.session.get('user_id') is None and not request.user.is_authenticated()):
        return redirect('welcome')
    if request.user.is_authenticated():
        request.session["user_id"] = request.user.id
    post_id = None
    if request.method == 'GET':
        post_id = request.GET['post_id']

    votes = 0
    if post_id:
        post = Post.objects.get(id=int(post_id))
        if post:
            votes = post.votes + 1
            post.votes =  votes
            post.save()

    return HttpResponse(votes)
