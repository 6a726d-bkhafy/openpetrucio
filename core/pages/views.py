from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from . import urls
from .models import Hosts,Unknow,Switch
from .forms import UnwForm,CreateForm
from django.shortcuts import render,redirect,get_list_or_404
from django.http import JsonResponse
import subprocess
from django.db.models import Q
# Create your views here.

class HostList(ListView):
    model=Hosts
    template_name='pages/host_inventory/host_inventory.html'
    paginate_by=30

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['order'] = self.request.GET.get('ordering')
        return context

    def get_queryset(self):
        queryset=super(HostList,self).get_queryset()
        ordering=self.request.GET.get('ordering')
        if ordering:
            if ordering.startswith('-'):
                order=ordering.replace('-','')
            else:
                order='-'+ordering
            return Hosts.objects.all().order_by(order)
        data=self.request.GET
        search_field=data.get('search_field')
        if search_field:
            queryset=queryset.filter(
                Q(ip__icontains=search_field) |
                Q(hostname__icontains=search_field) |
                Q(host_type__icontains=search_field) |
                Q(mac_1__icontains=search_field)
            )
        return queryset

class HostCreate(CreateView):
    model=Hosts
    form_class=CreateForm
    template_name='pages/forms/create_forms.html'
    success_url=reverse_lazy('host_inventory')

    def get_form(self,form_class=None):
        form=super().get_form(form_class)
        form.fields['hostname'].initial=''
        form.fields['host_type'].initial=''
        form.fields['mac_1'].initial=''
        form.fields['mac_2'].initial=''
        return form

class HostUpdate(UpdateView):
    model=Hosts
    form_class=CreateForm
    template_name='pages/forms/update_forms.html'
    success_url=reverse_lazy('host_inventory')

def delete_host(request,id):
    host=Hosts.objects.get(id=id)
    host.delete()
    return redirect('host_inventory')

class UnwList(ListView):
    model=Unknow
    template_name='pages/host_inventory/unknow.html'

class UnwDelete(DeleteView):
    model=Unknow
    form_class=UnwForm
    template_name='pages/forms/unw_forms.html'
    success_url=reverse_lazy('unknow')

    def get_form(self,form_class=None):
        form=super().get_form(form_class)
        form.fields['hostname'].initial=''
        form.fields['host_type'].initial=''
        return form

def unw_to_main(request,id):
    host=Unknow.objects.get(id=id)
    host.delete()
    ip=host.ip
    mac_1=host.mac
    hostname=request.POST.get('hostname')
    host_type=request.POST.get('host_type')
    hosts=Hosts(
        ip=ip,
        mac_1=mac_1,
        hostname=hostname,
        host_type=host_type,
    )
    hosts.save()
    return redirect('unknow')

def att(request):
    process=subprocess.Popen(['python3','/home/danilobertin/petrucio/scripts/integrator.py'])
    out, err=process.communicate()
    return JsonResponse({'status': 'running'})

class SwitchList(ListView):
    model=Switch
    template_name='pages/host_inventory/overview.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        pk=self.kwargs.get('pk')
        host=Hosts.objects.get(pk=pk)
        context['host']=host
        context['pk'] = str(pk)
        return context

