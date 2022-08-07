from .models import Enquiry, Course, Admission

from django import forms


GENDER_CHOICE = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

QUALIFICATION_CHOICE = [
    ('Tenth', 'Tenth'),
    ('Twelfth', 'Twelfth'),
    ('Diploma', 'Diploma'),
    ('Graduate', 'Graduate'),
    ('Post Graduate', 'Post Graduate'),
]


COURSE_CHOICE = []
course = Course.objects.all()
for c in course:
    COURSE_CHOICE.append((c.name, c.name),)

# IDS_CHOICES = []
# ids = Enquiry.objects.all()
# for i in ids:
#     IDS_CHOICES.append((i, i))

EMPLOYMENT_STATUS_CHOICE = [
    ('Student', 'Student'),
    ('Working', 'Working'),
    ('Part-Time', 'Part-Time'),
    ('Un-Employed', 'Un-Employed'),
]


class EnquiryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reference'].required = False
        self.fields['whatsapp'].required = False
        self.fields['other_course'].required = False

    gender = forms.ChoiceField(
        choices=GENDER_CHOICE, widget=forms.RadioSelect)
    qualification = forms.ChoiceField(choices=QUALIFICATION_CHOICE)
    enquiry_for = forms.MultipleChoiceField(
        choices=COURSE_CHOICE, widget=forms.CheckboxSelectMultiple)
    emplyment_status = forms.ChoiceField(
        choices=EMPLOYMENT_STATUS_CHOICE, widget=forms.RadioSelect)

    class Meta:
        model = Enquiry
        fields = [
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
            'reference']

        labels = {
            'dob': "Date of Birth",
            'enquiry_for': "Enquiry For",
            'other_course': "Any other Course",
            'emplyment_status': "Employment Status",
            'last_enquiry_info': 'Info'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'other_course': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(),
            'whatsapp': forms.NumberInput(),
            'reference': forms.TextInput(attrs={'class': 'form-control'})
        }


class EnquirySearchForm(forms.Form):
    name = forms.CharField(max_length=100)
    dob = forms.CharField(max_length=100)


class AdmissionForm(forms.ModelForm):
    # enquiry_id = forms.ChoiceField(choices=IDS_CHOICES)
    admission_for = forms.CharField()
    payment = forms.IntegerField()
    admission_for = forms.MultipleChoiceField(
        choices=COURSE_CHOICE, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Admission
        labels = {
            'admission_for': "Course",
            'enquiry_id': "ID",

        }

        fields = [
            'enquiry_id',
            'admission_for',
            'payment'
        ]
