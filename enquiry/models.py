from django.db import models
# Create your models here.


class Enquiry(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    address = models.TextField(max_length=500)
    dob = models.DateField()
    qualification = models.CharField(max_length=200)
    specialisation = models.CharField(null=True, max_length=200, blank=True)
    enquiry_for = models.CharField(max_length=200, null=True)
    other_course = models.CharField(max_length=200, blank=True)
    phone = models.BigIntegerField()
    whatsapp = models.BigIntegerField(null=True, blank=True)
    emplyment_status = models.CharField(max_length=200)
    reference = models.CharField(null=True, max_length=200, blank=True)
    next_enquiry = models.DateField(null=True)
    last_enquiry = models.DateTimeField(null=True)
    last_enquiry_info = models.CharField(
        max_length=200, default='Not answered')
    enquiry_date = models.DateTimeField(auto_now_add=True)
    admission_confirm = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


class Admission(models.Model):
    enquiry_id = models.ForeignKey(Enquiry, on_delete=models.CASCADE)
    admission_for = models.CharField(max_length=200, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    admission_date = models.DateTimeField(auto_now_add=True)
    payment = models.BigIntegerField(null=True, blank=True)


class Course(models.Model):
    name = models.CharField(max_length=200)
    fees = models.IntegerField()
