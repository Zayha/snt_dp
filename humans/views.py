from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from datetime import datetime, date

from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, TemplateView

from humans.forms import FeedbackForm, AddNewsForm, CustomRegistrationForm
from humans.models import News, Category
from humans.utils.mixins import MyContextMixin
from humans.utils.menu import menu

# def index(request):
#     cats = Category.objects.filter(news__isnull=False, news__is_published=True).distinct()
#     data = News.objects.filter(is_published=True).order_by('-time_create')
#     context = {
#         'cats': cats,
#         'menu': menu,
#         'posts': data,
#         'title': 'Главная страница'
#     }
#
#     return render(request, 'humans/index.html', context=context)
#
#
# def time_page(request):
#     return HttpResponse(f"<h1 style='color: red;'>Текущее время: "
#                         f"{datetime.now().strftime('%H:%M:%S')}</h1> ")
#
#
# def get_parameters(request, param_id):
#     if param_id == 1:
#         today = date.today()
#         formatted_date = today.strftime("%d.%m.%Y")
#         result = f'Дата: {formatted_date}'
#     elif param_id == 2:
#         result = f'Привет!'
#     else:
#         result = f'Параметр {param_id} отсутствует'
#     return HttpResponse(result)
#
#
# def regular(request, year):
#     if year == '8888' or int(year) > 9000:
#         raise Http404()
#     if int(year) == 2222:
#         return redirect('home', permanent=True)
#     if int(year) == 3333:
#         return redirect('time')
#     return HttpResponse(f'Год: {year}')
#
#
# def get_get(request):
#     # проверим, пришли ли к нам какие-то данные в словаре,
#     # обезопасим себя от возможных ошибок и выполнения лишнего кода
#     if request.GET:
#         # получим словарь
#         data = request.GET
#         # выведем его в консоль
#         print(data)
#         # при помощи генератора списков сформируем кортежи(в нашем случае пары)
#         # (ключ, значение)
#         key_value_list = [(key, value) for key, value in data.items()]
#         # при помощи генератора и строкового метода join получим
#         # html код, для отображения
#         response = '<br>'.join([f'{key} - {value}' for key, value in key_value_list])
#         # выведем в консоль результаты
#         print(response)
#         return HttpResponse(response)
#     else:
#         # если словарь пуст, то так и сообщим
#         return HttpResponse('<p>нет никаких параметров в GET запросе</p>')


def page404(request, exception):
    return HttpResponseNotFound('<h1>Page404 | Страница не найдена</h1>')


def plug(request):
    context = {
        'menu': menu,
        'title': 'Заглушка',
    }

    return render(request, 'humans/plug.html', context=context)


# def show_news(request, news_pk):
#     # data = News.objects.get(id=news_pk)
#     data = get_object_or_404(News, id=news_pk)
#     # data = get_object_or_404(News, id=news_pk, is_published=True)
#     context = {
#         'post': data,
#         'menu': menu,
#         'title': data.title,
#     }
#     return render(request, 'humans/show_news.html', context=context)
#
#
# def show_category(request, cat_pk):
#     # data = Category.objects.get(id=cat_pk)
#     data = get_object_or_404(Category, id=cat_pk)
#     cat = data.news_set.filter(is_published=True).order_by('-time_create')
#     cats = Category.objects.filter(news__isnull=False).distinct()
#     if len(cat) == 0:
#         raise Http404()
#     context = {
#         'cats': cats,
#         'menu': menu,
#         'posts': cat,
#         'title': data.name,
#         'current_cat': cat_pk
#     }
#
#     return render(request, 'humans/index.html', context=context)


# def feedback(request):
#     cats = Category.objects.filter(news__isnull=False, news__is_published=True).distinct()
#     context = {
#         'cats': cats,
#         'menu': menu,
#         'title': 'Форма обратной связи'
#     }
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             print(email)
#             message = form.cleaned_data['message']
#             return render(request, 'humans/success.html', {'name': name})
#     else:
#         form = FeedbackForm()
#
#     return render(request, 'humans/show_form.html', {'form': form} | context)


def add_news(request):
    cats = Category.objects.filter(news__isnull=False, news__is_published=True).distinct()
    context = {
        'cats': cats,
        'menu': menu,
        'title': 'Добавить новость'
    }
    if request.method == 'POST':
        form = AddNewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'humans/success.html')
    else:
        form = AddNewsForm()

    return render(request, 'humans/show_form.html', {'form': form} | context)


class NewsDisplay(MyContextMixin, ListView):
    model = News
    template_name = 'humans/index.html'
    context_object_name = 'posts'

    def get_context_data(self):
        context = super().get_context_data(title='Главная страница')
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).order_by('-time_create')


class ShowCategory(MyContextMixin, ListView):
    model = Category
    template_name = 'humans/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['current_cat'] = self.kwargs['cat_pk']
        context['title'] = context['posts'][0].category
        return context

    def get_queryset(self):
        return get_object_or_404(Category, id=self.kwargs['cat_pk']).news_set.filter(is_published=True).order_by(
            '-time_create')


class ShowNews(MyContextMixin, DetailView):
    model = News
    context_object_name = 'post'
    template_name = 'humans/show_news.html'
    pk_url_kwarg = 'news_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(News, id=self.kwargs['news_pk'], is_published=True)


class AddNews(LoginRequiredMixin, MyContextMixin, CreateView):
    login_url = reverse_lazy('home')
    form_class = AddNewsForm
    template_name = 'humans/show_form.html'
    success_url = reverse_lazy('form_success')

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(title='Добавить новость')


# !!!! тут можно добавить имя из формы логина
class ShowFormSuccess(TemplateView):
    template_name = 'humans/success.html'


class UserRegistration(MyContextMixin, CreateView):
    form_class = CustomRegistrationForm
    template_name = 'humans/registration.html'
    success_url = reverse_lazy('form_success')


class AuthUser(MyContextMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'humans/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(title='Авторизация')

    def get_success_url(self):
        return reverse_lazy('home')


class Contacts(MyContextMixin, TemplateView):
    template_name = 'humans/contacts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(title='Контакты')



def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('home'))
