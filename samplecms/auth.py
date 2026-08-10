"""Okta/OIDC authentication backend, only imported when OKTA_AUTH is enabled."""
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class NDOIDCAuthBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super().create_user(claims)
        return self.update_user(user, claims)

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()

        return user
