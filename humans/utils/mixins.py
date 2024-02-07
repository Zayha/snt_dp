from humans.models import Category
from humans.utils.menu import menu


class MyContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) | kwargs
        context['menu'] = menu
        context['login_menu'] = self._get_login_menu()
        context['cats'] = Category.objects.filter(news__isnull=False, news__is_published=True).distinct()
        return context

    def _get_login_menu(self):
        return [
            {'desc': 'Выход', 'url_name': 'logout'}
        ] if self.request.user.is_authenticated else [
            {'desc': 'Вход', 'url_name': 'login'},
            {'desc': 'Регистрация', 'url_name': 'registration'}
        ]
