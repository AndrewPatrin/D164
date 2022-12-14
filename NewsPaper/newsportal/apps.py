from django.apps import AppConfig


class NewsportalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsportal'

    def ready(self):
        import newsportal.signals

        # from .tasks import send_mail
        # from .scheduler import newsportal_scheduler
        # print('started')
        # newsportal_scheduler.add_job(
        #     id='send mail',
        #     func=send_mail,
        #     trigger='interval',
        #     seconds=5,
        # )
        # newsportal_scheduler.start()
