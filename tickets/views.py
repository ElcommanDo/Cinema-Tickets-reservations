from django.shortcuts import render
from django.http.response import  JsonResponse
from .models import *
from .serializers import *
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, filters, viewsets, generics
from rest_framework.authentication import BaseAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permisssions import IsAuthorOrReadonly
# 1 FBV Without REST no model


def no_rest_no_model(request):
    guests = [
        {'id': 1,
         'name': 'Ali omar',
         'mobile': '875412'
         },
        {'id': 2,
         'name': 'abdelrhman mostafa',
         'mobile': '8755152'
         },
        {'id': 3,
         'name': 'yassin tag yassin',
         'mobile': '861512'
         },
        ]
    return JsonResponse(guests, safe=False)


# 2 Using Models FBV
def user_model_func(request):
    guests = Guest.objects.all()
    data = list(guests.values('pk', 'guest_name', 'guest_mobile'))
    return JsonResponse(data, safe=False)


'''
PK query --  GET
List     --  GET
Create   --  POST
update   --  PUT
Delete   --  DELETE   
'''


@api_view(['GET', 'POST'])
def guest_list(request):
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'GET', 'DELETE'])
def pk_guest(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = GuestSerializer(data=request.data,instance=guest)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MoviesViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [BaseAuthentication]
    # permission_classes = [IsAuthenticated]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class GuestsViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]


# Search for Movie
@api_view(['GET'])
def search_movie(request):
    movies = Movie.objects.filter(movie_name=request.data['movie_name'],
                              hall=request.data['hall'])
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(movie_name=request.data['movie_name'],
                              hall=request.data['hall'])
    guest = Guest.objects.create(guest_name=request.data['name'],
                                 guest_mobile=request.data['mobile'])
    guest.save()

    reservation = Reservation(guest=guest, movie=movie)
    reservation.save()
    return Response(status=status.HTTP_201_CREATED)


class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadonly, ]
