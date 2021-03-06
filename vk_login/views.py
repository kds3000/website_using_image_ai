from django.shortcuts import render, redirect
import vk_api

MAIN_URL = 'http://kds3000.pythonanywhere.com/vk_login/'


def index(request):
    context = {}

    # Если токен есть, значит юзер в системе
    try:
        access_token = request.session['token']['access_token']
    # Если токена нет, пытаемся получить токен по коду и редиректим на главную
    except KeyError:
        code = request.GET.get('code')
        if code:
            vk_session = start_session()
            request.session['token'] = get_token(vk_session, code)
            return redirect(MAIN_URL)
    # Токен есть, передаем нужный контекст на страницу
    else:
        if request.method == 'POST':
            add_search_results_to_context(request, context, access_token)
        add_user_and_friends_basic_info_to_context(request, context, access_token)

    return render(request, 'vk_login.html', context)


def get_name_and_url_from_item(item: dict):
    """
    Функция, извлекающая только нужны нам данные о друге.
    Имя, фамилию и ссылку на профиль.
    """
    name = '{} {}'.format(item['first_name'], item['last_name'])
    url = 'https://vk.com/id{}'.format(item['id'])
    return {'name': name, 'url': url}


def add_search_results_to_context(request, context, access_token):
    """Функция, добавляющая в контекст список найденных друзей.
    В результаты добавляется {'name': 'Имя Фамилия', 'url': ссылка на профиль}.
    """
    vk_session = start_session(access_token)

    # метод позволяет обращаться к методам API как к обычным классам
    vk = vk_session.get_api()

    # Имя, по которому ведется поиск
    searching_for = request.POST.get('search')
    response = vk.friends.search(q=searching_for)
    context['search_results'] = []
    for item in response['items']:
        name_and_url = get_name_and_url_from_item(item)
        context['search_results'].append(name_and_url)

    # Индикатор того, что поиск был произведен. Нужен для добавления блока на странице.
    context['search_complete'] = True


def add_user_and_friends_basic_info_to_context(request, context, access_token):
    """Функция, добавляющая в контекст имя и фамилию пользователя, количество
    его друзей, ссылки на пять случайных друзей, а также ссылку на аватарку
    пользователя
    """
    try:
        vk_session = start_session(access_token)

        # метод позволяет обращаться к методам API как к обычным классам
        vk = vk_session.get_api()

        response = vk.friends.get(fields='count', count=5, order='random')

        # Число друзей
        count = response['count']
        context['count'] = count

        # Список для друзей, отображаемых по умолчанию на главной странице
        context['friends_for_index'] = []
        items = response['items']
        for item in items:
            name_and_url = get_name_and_url_from_item(item)
            if name_and_url not in context['friends_for_index']:
                context['friends_for_index'].append(name_and_url)

        # Контакт возвращает список словарей (по словарю на каждого пользователя)
        response = vk.users.get(fields='photo_200')
        # В данном запросе вернется список из одного словаря, поэтому берем индекс [0]
        data = response[0]
        context['photo'] = data['photo_200']
        context['name'] = '{} {}'.format(data['first_name'], data['last_name'])

    # Перехват исключения в случае попытки пользователя зайти с устаревшим токеном
    except vk_api.exceptions.ApiError:
        logout(request)


def start_session(access_token=None):
    """
    Функция создает сессию ВК с помощью библиотеки vk_api
    В данном случае заходим при помощи ID приложения, защищенного ключа, и токена
    при его наличии. Пока экземпляру класса не будет присвоен токен авторизация
    не будет осуществлена
    """
    app_id = 7355560
    client_secret = 'GcnwNwSbuSc61P6fmcIb'
    return vk_api.VkApi(app_id=app_id,
                        client_secret=client_secret,
                        token=access_token
                        )


def get_token(session, code):
    """Функция, возвращающая токен. Использует функцию VkApi.code_auth()
    для получения access_token из code"""
    redirect_url = MAIN_URL
    _token = session.code_auth(code, redirect_url)
    return _token


def logout(request):
    """Функция, стриающая сессионный кэш. Основное предназначение - стереть
    access_token пользователя из request.session.
    """
    request.session.flush()
    return redirect(MAIN_URL)
