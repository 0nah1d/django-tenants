from django.db.models import Q
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.contrib.auth import get_user_model

Account = get_user_model()


class SocialAuthAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        try:
            if sociallogin.user.email:
                user = Account.objects.get(email=sociallogin.user.email)
                if user:
                    if SocialAccount.objects.filter(
                            Q(user_id=user.pk) & Q(provider='google') | Q(provider='github')).count() == 0:
                        sociallogin.connect(request, user)

        # Create a response object
        except Account.DoesNotExist:
            pass
