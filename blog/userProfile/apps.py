from django.apps import AppConfig


class UserprofileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userProfile'
    verbose_name = 'Профили пользователей'

    def ready(self):
        #  импортируем сигналы при готовности приложения
        import userProfile.signals
