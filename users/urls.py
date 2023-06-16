from django.urls import path

from .views import (
    AuthorizedUserView,
    UserView,
    UserRegistration,
    UserSubtier,
    UserAddLink,
    UserSubscribe,
    UserUnsubscribe,
    UserTopView,
    UserUpdateProfilePicture,
    UserBanner,
    UserBackground,
    UserBannerSwitch,
    UserBackgroundSwitch
)

urlpatterns = [
    path('', AuthorizedUserView.as_view()),
    path('<id>/', UserView.as_view()),
    path('top', UserTopView.as_view()),
    path('register', UserRegistration.as_view()),
    path('profile_picture', UserUpdateProfilePicture.as_view()),
    path('subtier', UserSubtier.as_view()),
    path('subtier/<uuid>', UserSubtier.as_view()),
    path('add_link', UserAddLink.as_view()),
    path('subscribe', UserSubscribe.as_view()),
    path('unsubscribe/<id>', UserUnsubscribe.as_view()),
    path('banner', UserBanner.as_view()),
    path('background', UserBackground.as_view()),
    path('switch_banner', UserBannerSwitch.as_view()),
    path('switch_background', UserBackgroundSwitch.as_view()),
]


