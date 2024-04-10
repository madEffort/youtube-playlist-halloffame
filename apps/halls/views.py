from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall, Video
from .forms import VideoForm, SearchForm

# Create your views here.
def home(request):
    return render(request, 'halls/home.html')

def dashboard(request):
    return render(request, 'halls/dashboard.html')

def add_video(request, pk):
    form = VideoForm()
    search_form = SearchForm()
    
    if request.method == 'POST':
        filled_form = VideoForm(request.POST)
        if filled_form.is_valid():
            video = Video()
            video.title = filled_form.cleaned_data.get('title')
            video.url = filled_form.cleaned_data.get('url')
            video.youtube_id = filled_form.cleaned_data.get('youtube_id')
            video.hall = Hall.objects.get(pk=pk)
            video.save()

            # 같은 코드
            # Video.objects.create(
            #     title=filled_form.cleaned_data.get('title'),
            #     url=filled_form.cleaned_data.get('url'),
            #     youtube_id=filled_form.cleaned_data.get('youtube_id'),
            #     hall=Hall.objects.get(pk=pk),
            # )
            
    return render(request, 'halls/add_video.html', {'form': form, 'search_form': search_form})

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/signup.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        valid = super(SignUp, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(request=self.request, username=username, password=password)
        login(self.request, user)
        return valid

class CreateHall(CreateView):
    model = Hall
    fields = ['title']
    template_name = 'halls/create_hall.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super(CreateHall, self).form_valid(form)
    
class DetailHall(DetailView):
    model = Hall
    template_name = 'halls/detail_hall.html'

class UpdateHall(UpdateView):
    model = Hall
    fields = ['title']
    template_name = 'halls/update_hall.html'
    success_url = reverse_lazy('dashboard')
    

class DeleteHall(DeleteView):
    model = Hall
    template_name = 'halls/delete_hall.html'
    success_url = reverse_lazy('dashboard')