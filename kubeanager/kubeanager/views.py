from django.shortcuts import render, get_object_or_404
from .models import ClusterData
from django.contrib import messages
#from kubeanager.forms import VerifyBucketForm
import os.path
from django.views.generic import TemplateView
from django.http import StreamingHttpResponse, HttpResponse
import requests
import sys
import os
from subprocess import run,PIPE

currentDirectory = os.getcwd()

#class HomeView(TemplateView):
#    template_name = 'kubeanager/home.html'

#    def get(self, request):
#        clusters =  ClusterData.objects.all()
#        form = VerifyBucketForm()
#        return render(request, self.template_name, {'clusters':clusters})

def cluster_view(request):
    clusters =  ClusterData.objects.all()
    a1 = request.POST.get('delcluster')
    #out = run([sys.executable, '//home//opal//repos//kubeanager//kubeanager//scripts//print.py'], shell=False, stdout=PIPE)
    if request.method == 'POST':
        if request.POST.get('delcluster'):
            out = run([sys.executable, '//home//opal//repos//kubeanager//kubeanager//scripts//print.py', a1], shell=False, stdout=PIPE)
            update_table = ClusterData()
            update_table = ClusterData.objects.filter(cluster_name=request.POST.get('delcluster')).delete()
            return render(request, 'kubeanager/home.html', {'clusters':clusters})
        else:
            return render(request, 'kubeanager/home.html', {'clusters':clusters})
        print(out)
    return render(request,'kubeanager/home.html', {'clusters':clusters})

def check_bucket_home(request):

    return render(request, 'kubeanager/check_bucket.html')

def check_bucket(request):
    a1 = request.POST.get('verifybucket')
    out = run([sys.executable, '//home//opal//repos//kubeanager//kubeanager//scripts//check_bucket.py', a1], shell=False, stdout=PIPE)
    if out == "Bucket Does Not Exist!":
        print(out)
        return render(request, 'kubeanager/bucket.html', {'checkedBucket':out.stdout.decode("utf-8")})
    else:
        print(out)
        return render(request, 'kubeanager/bucket.html', {'checkedBucket':out.stdout.decode("utf-8")})

def create_cluster_home(request):

    return render(request,'kubeanager/create_cluster.html')

def create_cluster(request):
    a1 = request.POST.get('bucket_name')
    a2 = request.POST.get('cluster_name')
    a3 = request.POST.get('dnszone')
    a4 = request.POST.get('cloud_account')
    out = run([sys.executable, '//home//opal//repos//kubeanager//kubeanager//scripts//create_cluster.py', a1, a2, a3, a4], shell=False, stdout=PIPE)
    clustercreated = os.path.isfile(currentDirectory + '/kubeanager/clusters/' + a2 + '/completed')
    if clustercreated == True:
        if request.method == 'POST':
            if request.POST.get('cluster_name') and request.POST.get('bucket_name') and request.POST.get('cloud_account') and request.POST.get('date'):
                update_table = ClusterData()
                update_table.cluster_name = request.POST.get('cluster_name')
                update_table.bucket_name = request.POST.get('bucket_name')
                update_table.cloud_account = request.POST.get('cloud_account')
                update_table.date = request.POST.get('date')
                update_table.save()
                return render(request, 'kubeanager/cluster.html', {'creatingCluster':out.stdout.decode("utf-8")})
        else:
                return render(request, 'kubeanager/cluster.html', {'creatingCluster':out.stdout.decode("utf-8")})
        print(out)
    else:
            return render(request, 'kubeanager/cluster.html', {'creatingCluster':out.stdout.decode("utf-8")})
    print(out)
    return render(request, 'kubeanager/cluster.html', {'creatingCluster':out.stdout.decode("utf-8")})

def delete_cluster_home(request):

    return render(request,'kubeanager/delete_cluster.html')

def delete_cluster(request):
    a1 = request.POST.get('delcluster')
    out = run([sys.executable, '//home//opal//repos//kubeanager//kubeanager//scripts//test.sh', a1], shell=False, stdout=PIPE)
    if request.method == 'POST':
        if request.POST.get('delcluster'):
            update_table = ClusterData()
            update_table = ClusterData.objects.filter(cluster_name=request.POST.get('delcluster')).delete()
            return render(request, 'kubeanager/delcluster.html', {'deletingCluster':out.stdout.decode("utf-8")})
    else:
            return render(request, 'kubeanager/delcluster.html', {'deletingCluster':out.stdout.decode("utf-8")})
    print(out)


def manage_cluster(request, clusterdata_id):
    #a1 = request.POST.get('clusterprofile')
    #a2 = request.POST.get('clusterprofile')
    clusterdata = get_object_or_404(ClusterData, pk=clusterdata_id)
    #switch = run([sys.executable, '//home//opal//repos//kubeanager//kubeanager//scripts//skc.sh', a1, a2], shell=False, stdout=PIPE)
    return render(request, 'kubeanager/manage_cluster.html', {'clusterdata':clusterdata})
    #print(switch)
