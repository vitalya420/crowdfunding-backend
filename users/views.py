from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser

from users.models import User, CustomizationSettings, CustomizationData
from users.serializers import AuthorizedUserSerializer, UserSerializer, MinimalUserSerializer, \
    CustomizationDataSerializer


class AuthorizedUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AuthorizedUserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        serializer = AuthorizedUserSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = []
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, id):
        user = User.objects.get(pk=id)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


class UserRegistration(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSubtier(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            tier_data = request.data
            updated_user = request.user.create_new_sub_tier(**tier_data)
            serializer = AuthorizedUserSerializer(updated_user, context={'request': request})
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        try:
            updated_user = request.user.delete_sub_tier(uuid)
            return Response(AuthorizedUserSerializer(updated_user, context={'request': request}).data)
        except:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)


class UserAddLink(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            link_data = request.data
            updated_user = request.user.add_link(**link_data)
            serializer = AuthorizedUserSerializer(updated_user, context={'request': request})
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserSubscribe(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request):
        sub_data = request.data
        target_user = User.objects.get(pk=sub_data["id"])
        tier = target_user.sub_tiers.all().filter(uuid=sub_data['uuid']).first()
        request.user.sub_to_user(target_user, tier)
        return Response(UserSerializer(target_user, context={'request': request}).data, status=status.HTTP_200_OK)


class UserUnsubscribe(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, **kwargs):
        updated_user = request.user.cancel_sub(sub_id=int(kwargs.get('id')))
        return Response(UserSerializer(updated_user, context={'request': request}).data)


class UserTopView(ListAPIView):
    queryset = User.objects.all().order_by('id')[:20]
    serializer_class = MinimalUserSerializer


class UserUpdateProfilePicture(APIView):

    def post(self, request):
        request.user.profile_picture = request.data['profile_picture']
        request.user.save()
        return Response(AuthorizedUserSerializer(request.user, context={'request': request}).data, status=status.HTTP_200_OK)


class CustomizerView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    field = None

    def patch(self, request):
        if not request.data:
            return Response(status=status.HTTP_202_ACCEPTED)
        serializer = CustomizationDataSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_settings = self.get_or_create_settings(request.user)
            setattr(user_settings, self.field, serializer.instance)
            request.user.customizing.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_or_create_settings(user):
        customizing = user.customizing
        if not customizing:
            new = CustomizationSettings.objects.create()
            new.save()
            user.customizing = new
            user.save()
        return user.customizing


class UserBanner(CustomizerView):
    field = 'banner'


class UserBackground(CustomizerView):
    field = 'background'


class UserBannerSwitch(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.customizing.banner_enabled = request.data['value']
        request.user.customizing.save()
        return Response(status=200)


class UserBackgroundSwitch(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.customizing.background_enabled = request.data['value']
        request.user.customizing.save()
        return Response(status=200)
