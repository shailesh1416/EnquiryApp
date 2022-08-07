from django.contrib import admin

from .models import Enquiry, Course, Admission
# Register your models here.


@admin.register(Enquiry)
class EnquiryModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'gender',
        'address',
        'dob',
        'qualification',
        'enquiry_for',
        'other_course',
        'phone',
        'whatsapp',
        'emplyment_status',
        'reference']


@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'fees']


@admin.register(Admission)
class AdmissionModelAdmin(admin.ModelAdmin):
    list_display = [
        'enquiry_id',
        'admission_for',
        'last_modified',
        'admission_date',
        'payment'
    ]
