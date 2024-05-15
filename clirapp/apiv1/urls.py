from django.urls import path

from . import views

urlpatterns = [
    #path('signup', views.SignUpView.as_view()),
    #path('login', views.LoginView.as_view()),
    #path('user', views.UserView.as_view()),
    #path('logout', views.LogoutView.as_view()),

    # GET /api/projects/: Para obtener la lista de proyectos del usuario autenticado.
    # POST /api/projects/: Para crear un nuevo proyecto.
    # GET /api/projects/<project_id>/: Para obtener detalles de un proyecto específico.
    # PUT /api/projects/<project_id>/: Para actualizar detalles de un proyecto específico.
    # DELETE /api/projects/<project_id>/: Para eliminar un proyecto específico.
    # Operaciones relacionadas con Historias de Usuario:
    #
    # GET /api/user-stories/: Para obtener la lista de historias de usuario de un proyecto.
    # POST /api/user-stories/: Para crear una nueva historia de usuario.
    # GET /api/user-stories/<user_story_id>/: Para obtener detalles de una historia de usuario específica.
    # PUT /api/user-stories/<user_story_id>/: Para actualizar detalles de una historia de usuario específica.
    # DELETE /api/user-stories/<user_story_id>/: Para eliminar una historia de usuario específica.
    # Operaciones relacionadas con Tickets:
    #
    # GET /api/tickets/: Para obtener la lista de tickets de una historia de usuario.
    # POST /api/tickets/: Para crear un nuevo ticket.
    # GET /api/tickets/<ticket_id>/: Para obtener detalles de un ticket específico.
    # PUT /api/tickets/<ticket_id>/: Para actualizar detalles de un ticket específico.
    # DELETE /api/tickets/<ticket_id>/: Para eliminar un ticket específico.
    # Otras operaciones:
    #
    # POST /api/tickets/<ticket_id>/cancel/: Para cancelar un ticket activo.



    #path('projects', views.ProjectView.as_view()),
    #path('projects/<uuid:uuid>', views.ProjectView.as_view()),
    #path('user-stories', views.UserStoryView.as_view()),
    #path('user-stories/<uuid:uuid>', views.UserStoryView.as_view()),
    #path('tickets', views.TicketView.as_view()),
    #path('tickets/<uuid:uuid>', views.TicketView.as_view()),
    #path('tickets/<uuid:uuid>/cancel', views.cancel_ticket)
]