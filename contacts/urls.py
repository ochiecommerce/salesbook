from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from .api_view import ContactsViewSet, InviteViewSet, MembershipViewSet

router = DefaultRouter()
router.register(r'contacts',ContactsViewSet, basename='contact')
router.register(r'memberships',MembershipViewSet, basename='membership')
router.register(r'invites',InviteViewSet, basename='invite')

urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('api/',include(router.urls)),
    path('api/token/',obtain_auth_token,),
    path('api/auth/',include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')), 
    path('add_contact/',views.add_contact, name='add_contact'),
    path('register/',views.register, name='register'),
    path('login/',views.login,name='login'),
    path('group/',views.group,name='group'),
    path('invite/',views.group_invite,name='invite'),
    path('accept_invite/<int:invite_id>',views.accept_invite,name='accept_invite'),
    path('<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('<int:contact_id>/add_interaction/', views.add_interaction, name='add_interaction'),
]
