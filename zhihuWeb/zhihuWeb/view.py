from django.http import HttpResponse
from django.shortcuts import render


def zhihuQuestionTop(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'questionTop.html', context)