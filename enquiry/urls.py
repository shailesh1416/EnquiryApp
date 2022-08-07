from django.urls import path
from enquiry import views

urlpatterns = [
    path('', views.enquiry.as_view(), name='enquiry'),
    path('search', views.EnquirySearch.as_view(), name='search'),
    path('admission/<int:pk>/', views.admission.as_view(), name='admission'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('followup/', views.enquiry_index, name='enquiry_index'),
    path('enquiry_details/<int:pk>/',
         views.enquiry_details, name='enquiry_details'),
    path(
        "edit/<int:pk>",
        views.EnquiryUpdateView.as_view(),
        name="enquiry_update"
    ),


]
