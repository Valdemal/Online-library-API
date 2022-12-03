from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import mixins
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import SAFE_METHODS, IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from main.permissions import IsStaffOrReadOnly, IsAuthorOrStaff, CanCreateIfAuthenticatedOrCanAllIfStuff
from user.models import Comment, Reading
from user.serializers import CommentGetSerializer, CommentSetSerializer, ReadingGetSerializer, ReadingSetSerializer


class UserViewSet(DjoserUserViewSet):
    lookup_field = 'username'

    @action(methods=['GET'], detail=True)
    def readings(self, request, username):
        serialized = ReadingGetSerializer(Reading.objects.filter(user__username=username), many=True)
        return Response(serialized.data)

    @action(methods=['GET'], detail=True)
    def comments(self, request, username):
        serialized = CommentGetSerializer(Comment.objects.filter(user__username=username), many=True)
        return Response(serialized.data)

    @action(methods=['GET'], url_path='me/comments', detail=False)
    def my_comments(self, request):
        serialized = CommentGetSerializer(Comment.objects.filter(user=request.user), many=True)
        return Response(serialized.data)

    @action(methods=['GET'], url_path='me/readings', detail=False)
    def my_readings(self, request):
        serialized = ReadingGetSerializer(Reading.objects.filter(user=request.user), many=True)
        return Response(serialized.data)

    def get_permissions(self):
        if self.action in ('my_comments', 'my_readings'):
            return IsAuthenticated(),
        elif self.action in ('readings', 'comments'):
            return IsAdminUser(),

        return super().get_permissions()


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        return CommentGetSerializer if self.request.method in SAFE_METHODS else CommentSetSerializer

    def get_permissions(self):
        if self.action == 'list':
            return AllowAny(),
        elif self.action == 'create':
            return IsAuthenticated(),
        else:
            return IsAuthorOrStaff(),


class ReadingViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Reading.objects.all()

    def get_serializer_class(self):
        return ReadingGetSerializer if self.request.method in SAFE_METHODS else ReadingSetSerializer

    def get_permissions(self):
        if self.action == 'create':
            return IsAuthenticated(),
        elif self.action == 'destroy':
            return IsAuthorOrStaff(),
        else:
            return IsAdminUser(),
