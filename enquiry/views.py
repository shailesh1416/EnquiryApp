from .forms import EnquirySearchForm, AdmissionForm
from django.shortcuts import render
from .forms import EnquiryForm
from enquiry.models import Enquiry, Admission
from django.views import View
from django.views.generic import (
    CreateView,
    UpdateView,
)

# new to learn
from datetime import timedelta, datetime

from django.urls import reverse_lazy

from django.db.models import Q

# New to learn
from django.db.models.functions import TruncMonth, ExtractDay
from django.db.models import Sum, Count
# Create your views here.


class enquiry(CreateView):
    def get(self, request):
        form = EnquiryForm()
        context = {
            'form': form
        }
        return render(request, 'enquiry.html', context)

    # saving form after submit
    def post(self, request):
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
        context = {
            'form': form
        }
        return render(request, 'enquiry.html', context)


class admission(CreateView):
    def get(self, request, pk):
        enquiry = Enquiry.objects.get(pk=pk)
        form = AdmissionForm()
        context = {
            'enquiry': enquiry,
            'form': form
        }
        return render(request, 'admission.html', context)

    # saving form after submit
    def post(self, request, pk):
        form = AdmissionForm(request.POST)
        if form.is_valid():
            form.save()
        context = {
            'form': form,
            'message': "Admission Successful!"
        }
        return render(request, 'admission_success.html', context)


# indexing enquiries
def enquiry_index(request):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # order descending
    # enquiries = Enquiry.objects.order_by('-enquiry_date')
    enquiries = Enquiry.objects.filter(
        enquiry_date__date=datetime.today()-timedelta(3))

    # todays Follow up
    # enquiries = Enquiry.objects.filter(
    #     enquiry_date__date=datetime.today()-timedelta(2)
    # )
    # tommorows followup
    # enquiries = Enquiry.objects.filter(
    #     enquiry_date__date=datetime.today()-timedelta(3)
    # )

    context = {
        'enquiries': enquiries,
    }
    return render(request, 'followups.html', context)


# Enquiry details view

def enquiry_details(request, pk):
    enquiry = Enquiry.objects.get(pk=pk)

    context = {
        'enquiry': enquiry,
    }
    return render(request, 'enquiry_details.html', context)

# Enquiry Edit view


class EnquiryUpdateView(UpdateView):
    model = Enquiry
    fields = [
        'last_enquiry',
        'next_enquiry',
        'last_enquiry_info',
        'name',
        'gender',
        'address',
        'dob',
        'qualification',
        'specialisation',
        'enquiry_for',
        'other_course',
        'phone',
        'whatsapp',
        'emplyment_status',
        'reference'
    ]
    success_url = reverse_lazy("enquiry")


# Dashboard View
def dashboard(request):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    # Total Enquiries
    all_enquries_count = Enquiry.objects.all().count()

    # Total Enquiries this month
    this_month_count = Enquiry.objects.filter(
        enquiry_date__month=datetime.today().month).count()

    # Total Enquiries by each month of year
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                  'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_count = []

    for i in range(1, 13):
        count = Enquiry.objects.filter(enquiry_date__year=datetime.today().year).filter(
            enquiry_date__month=i).count()
        monthly_count.append(count)

    # total enquiries today
    today = Enquiry.objects.filter(enquiry_date__date=datetime.today()).count()
    # total Admissions today
    today_admission = Admission.objects.filter(
        admission_date__date=datetime.today()).count()
    # Total Followups today
    today_followups = Enquiry.objects.filter(
        enquiry_date__date=datetime.today()-timedelta(3)).count()
    today_followups_done = Enquiry.objects.filter(
        last_enquiry__date=datetime.today()).count()
    today_followups_done_percent = int(
        today_followups_done/today_followups*100)

    data = Enquiry.objects.annotate(month=TruncMonth('enquiry_date')).values(
        'month').annotate(c=Count('id')).values('month', 'c')

    # Counting Total Course Enquiries
    courses = ['Computer', 'Excel', 'Tally',
               'Graphic', 'AutoCAD', 'Programming']
    total_course_enquries = []
    count = 0
    for course_name in courses:
        count = Enquiry.objects.filter(
            enquiry_for__contains=course_name).count()
        total_course_enquries.append(count)

    # This months total enquiry
    this_month = Enquiry.objects.filter(
        enquiry_date__month=datetime.today().month)

    # Each day count of month
    month_daywise = this_month.annotate(day=ExtractDay(
        'enquiry_date')).values('day').annotate(n=Count('pk'))
    month_daywise_data = []
    month_daywise_label = []
    for j in month_daywise:
        month_daywise_data.append(j['n'])
        month_daywise_label.append(j['day'])

    # Coursewise count of month
    this_month_course_enquiry = []
    for course_name in courses:
        this_month_course_enquiry.append(this_month.filter(enquiry_for__contains=course_name).count()
                                         )
    context = {
        'month_list': month_list,
        'monthly_count': monthly_count,
        'month_daywise_data': month_daywise_data,
        'month_daywise_label': month_daywise_label,
        'today': today,
        'today_admissions': today_admission,
        'today_followups': today_followups,
        'today_followups_done': today_followups_done,
        'today_followups_done_percent': today_followups_done_percent,
        'this_month_count': this_month_count,
        'this_month_course_enquiry': this_month_course_enquiry,
        'data': data,
        'course':  total_course_enquries,
    }
    return render(request, 'dashboard.html', context)


# Enquiry Search Form


class EnquirySearch(CreateView):
    def get(self, request):
        form = EnquirySearchForm()
        context = {
            'form': form
        }
        return render(request, 'enquiry/search_form.html', context)

    def post(self, request):
        newform = EnquirySearchForm()
        form = EnquirySearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            dob = form.cleaned_data['dob']
            enquiries = Enquiry.objects.filter(
                Q(name__contains=name) | Q(dob__contains=dob))
            context = {
                'form': newform,
                'enquiries': enquiries
            }
            return render(request, 'enquiry/search_form.html', context)
        # return render(request, 'enquiry/search_form.html', {'form': form})
