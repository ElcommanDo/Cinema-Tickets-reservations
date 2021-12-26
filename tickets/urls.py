
from django.urls import path, include
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('movies', MoviesViewSet)
router.register('reservations', ReservationViewSet)
router.register('guests', GuestsViewSet)

urlpatterns = [
    path('django_non_rest/', no_rest_no_model),
    path('user_model_func/', user_model_func),
    path('api-view-decorator-guest-list/', guest_list),
    path('api-view-pk-guest/<int:pk>/', pk_guest),
    path('routers/', include(router.urls)),
    path('search-movie/', search_movie),
    path('new_reservation/', new_reservation),
    path('auth-token', obtain_auth_token),
    path("api-auth/", include("rest_framework.urls")),
    path('post_list_pk/<int:pk>/', Post_pk.as_view()),

]
