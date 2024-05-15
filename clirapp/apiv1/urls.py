from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.SignUpView.as_view()),
    path('login', views.LoginView.as_view()),
    path('user', views.UserView.as_view()),
    path('logout', views.LogoutView.as_view()),

    path('invitations', views.InvitationUserCompanyView.as_view()),
    path('invitations/<uuid:uuid>', views.InvitationUserCompanyView.as_view()),

    path('companies', views.CompanyView.as_view()),
    path('companies/<uuid:uuid>', views.CompanyView.as_view()),

    path('projects', views.ProjectView.as_view()),
    path('projects/<uuid:uuid>', views.ProjectView.as_view()),

#    path('user-stories', views.UserStoryView.as_view()),
#    path('user-stories/<uuid:uuid>', views.UserStoryView.as_view()),

#    path('tickets', views.TicketView.as_view()),
#    path('tickets/<uuid:uuid>', views.TicketView.as_view()),
#    path('tickets/<uuid:uuid>/cancel', views.cancel_ticket)
]