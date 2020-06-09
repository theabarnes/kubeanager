from django.shortcuts import render
from .models import ClusterData
from django.contrib import messages
#from kubeanager.forms import VerifyBucketForm
import os.path
from django.views.generic import TemplateView
import requests
import sys
import os
from subprocess import run,PIPE

currentDirectory = os.getcwd()

class HomeView(TemplateView):
    template_name = 'kubeanager/home.html'

    def get(self, request):
        clusters =  ClusterData.objects.all()
#        form = VerifyBucketForm()
        return render(request, self.template_name, {'clusters':clusters})

def testing(request):
    clusters =  ClusterData.objects.all()
    return render(request,'kubeanager/home.html', {'clusters':clusters})

def create_cluster_home(request):

    return render(request,'kubeanager/create_cluster.html')

def create_cluster(request):
    a1 = request.POST.get('bucket_name')
    a2 = request.POST.get('cluster_name')
    a3 = request.POST.get('dnszone')
    a4 = request.POST.get('profile')
    out = run([sys.executable, '//home//opal//repos//kubeanager//kubeanager//scripts//create_cluster.py', a1, a2, a3, a4], shell=False, stdout=PIPE)
    clustercreated = os.path.isfile(currentDirectory + '/kubeanager/clusters/' + a2 + '/completed')
    if clustercreated == True:
        if request.method == 'POST':
            if request.POST.get('cluster_name') and request.POST.get('bucket_name') and request.POST.get('date'):
                update_table = ClusterData()
                update_table.cluster_name = request.POST.get('cluster_name')
                update_table.bucket_name = request.POST.get('bucket_name')
                update_table.date = request.POST.get('date')
                update_table.save()
                return render(request, 'kubeanager/cluster.html', {'creatingCluster':out.stdout})
        else:
                return render(request, 'kubeanager/cluster.html', {'creatingCluster':out.stdout})
        print(out)
    else:
            return render(request, 'kubeanager/cluster.html', {'creatingCluster':out.stdout})
    print(out)
    return render(request, 'kubeanager/cluster.html', {'creatingCluster':out.stdout})

def check_bucket(request):

    return render(request, 'kubeanager/check_bucket.html')

def checked_bucket(request):
    a1 = request.POST.get('verifybucket')
    out = run([sys.executable, '//home//opal//repos//kubeanager//kubeanager//scripts//test.py', a1], shell=False, stdout=PIPE)
    if out == "Bucket Does Not Exist!":
        print(out)
        return render(request, 'kubeanager/bucket.html', {'checkedBucket':out.stdout})
    else:
        print(out)
        return render(request, 'kubeanager/bucket.html', {'checkedBucket':out.stdout})
