from django.forms.fields import DateTimeField
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count





# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()


        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                username = form.cleaned_data.get('username')
                UserProfile.objects.create(
                    user=user,
                    name=user.username,
                    email=user.eamil,
                )
                messages.success(request, 'Account has been created for '+ username)
                return redirect('home')

        context = {'form':form}
        return render(request, 'register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR Password is incorrect')
        context = {}
        return render(request, 'login.html', context) 

def logoutUser(request):
    logout(request)
    return redirect('login')

    

@login_required(login_url='login')
def home(request):
    if 'q' in request.GET:
        q=request.GET['q']
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(q_title__icontains=q).order_by('-add_time')
    else:
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).all().order_by('-add_time')
    paginator=Paginator(quests,5)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request,'main.html',{"quests":quests})

@login_required(login_url='login')
def detail(request,id):
    quest=Question.objects.get(pk=id)
    tags=quest.tags.split(',')
    answers=Answer.objects.filter(question=quest).order_by('add_time')
    answerform=AnswerForm
    if request.method=='POST':
        answerData=AnswerForm(request.POST)
        if answerData.is_valid():
            answer=answerData.save(commit=False)
            answer.question=quest
            answer.user=request.user
            answer.save()
            messages.success(request,'Answer has been submitted.')


    return render(request,'detail.html',{'quest':quest,
                                        'tags':tags,
                                        'answers':answers,
                                        'answerform':answerform
                                        })

@login_required(login_url='login')
def save_comment(request):
    if request.method=='POST':
        comment = request.POST.get('comment')
        answerid = request.POST.get('answerid')
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        Comment.objects.create(
            answer=answer,
            user=user,
            comment=comment
        )
        return JsonResponse({'bool':True})

def save_upvote(request):
    if request.method=='POST':
        answerid = request.POST.get('answerid')
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=UpVote.objects.filter(answer=answer,user=user).count()
        if check>0:
            return JsonResponse({'bool':False})
        else:
            UpVote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool':True})

def save_downvote(request):
    if request.method=='POST':
        answerid = request.POST.get('answerid')
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=DownVote.objects.filter(answer=answer,user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            DownVote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool':True})

@login_required(login_url='login')
def ask_form(request):
    form=QuestionForm
    if request.method=='POST':
        questForm=QuestionForm(request.POST)
        if questForm.is_valid():
            questForm=questForm.save(commit=False)
            questForm.user=request.user
            questForm.save()
            messages.success(request,'Question has been added.')
    return render(request,'askques.html',{'form':form})


def tag(request,tag):
    quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(tags__icontains=tag).order_by('-id')
    paginator=Paginator(quests,10)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request,'tag.html',{'quests':quests,'tag':tag})

@login_required(login_url='login')
def profile(request):
	user = request.user.userprofile
	form = ProfileForm(instance=user)

	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES,instance=user)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'profile.html', context)

@login_required(login_url='login')
def profileinfo(request):
    quests=Question.objects.filter(user=request.user).order_by('-id')
    answers=Answer.objects.filter(user=request.user).order_by('-id')
    comments=Comment.objects.filter(user=request.user).order_by('-id')
    upvotes=UpVote.objects.filter(user=request.user).order_by('-id')
    downvotes=DownVote.objects.filter(user=request.user).order_by('-id')
    return render(request,'profileinfo.html',{
        'quests':quests,
        'answers':answers,
        'comments':comments,
        'upvotes':upvotes,
        'downvotes':downvotes,
    })

@login_required(login_url='login')
def tags(request):
    quests=Question.objects.all()
    tags=[]
    for quest in quests:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    return render(request,'tags.html',{'tags':tag_with_count})

def otheruser(request,name):
    userinfo = UserProfile.objects.filter(name=name)
    if name == request.user.username:
        return render(request,'profileinfo.html')
    else:
        return render(request,'otheruser.html',{'otheruser':userinfo})
