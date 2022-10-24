from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from timetrack.models import Timesheet

# Create your views here.

class HomeView(TemplateView):
    template_name = 'base.html'
    page_title = "Home Page"
    page_heading = "A home landing page for the system"
    page_subheading = "The world is yours"

class TimesheetsListView(ListView):
    template_name = "timesheet_list.html"
    page_title = "Timesheets"
    page_heading = "List of timesheets for user"
    page_subheading = "create new sheets using link"
    model = Timesheet