from django.shortcuts import render
from django.http import HttpResponse

highest_five_rated = [1,2,3,4,5]
def index(request):
  return render(request, 'homepage\index.html', context={"highest_five_rated":highest_five_rated})
