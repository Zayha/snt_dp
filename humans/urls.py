from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy, include
from machina import urls as machina_urls
from django.contrib.auth import alogout

from humans.views import plug, NewsDisplay, ShowCategory, AddNews, ShowNews, ShowFormSuccess, UserRegistration, \
    AuthUser, Contacts, user_logout

urlpatterns = [
    path('', NewsDisplay.as_view(), name='home'),
    # path('humans/time/', time_page, name='time'),
    # path('parametr/<int:param_id>', get_parameters),
    # re_path(r'^articles/(?P<year>[0-9]{4})/$', regular),
    # path('get/', get_get),
    path('plug/', plug, name='plug'),
    path('show_news/<int:news_pk>', ShowNews.as_view(), name='show_news'),
    # path('show_category/<int:cat_pk>', show_category, name='show_category'),
    path('show_category/<int:cat_pk>', ShowCategory.as_view(), name='show_category'),
    # path('feedback/', feedback, name='feedback'),
    path('add_news/', AddNews.as_view(), name='add_news'),
    path('form_success/', ShowFormSuccess.as_view(), name='form_success'),
    path('registration/', UserRegistration.as_view(), name='registration'),
    path('login/', AuthUser.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('logout/', user_logout, name='logout'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('forum/', include(machina_urls), name='forum_snt'),
]
