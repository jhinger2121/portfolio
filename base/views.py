from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied

from base.models import Entry, MyEntrySerializer, ContactSerializer

from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

@api_view(['GET', 'POST'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def all_entries(request):
    if request.method == 'GET':
        entries = Entry.objects.all()
        serializer = MyEntrySerializer(entries, many=True)
        return Response(serializer.data)
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            serializer = MyEntrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        raise PermissionDenied()
    
@api_view(['GET', 'PUT', 'DELETE'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def entry_detail(request, post_id):
    post = get_object_or_404(Entry, id=post_id)
    if request.method == 'GET':
        serializer = MyEntrySerializer(post)
        return Response(serializer.data)
    
    if request.user.is_authanticated:
        if request.method == 'DELETE':
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        elif request.method == 'PUT':
            serializer = MyEntrySerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        raise PermissionDenied()

@api_view(['POST'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def contact_me(request):
    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
