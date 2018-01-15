Шаги установки приложения:

В settings.py INSTALLED_APPS добавить - 'complaint',

urls.py добавить путь - url(r'^complaint_text/', include('complaint.urls')),

///////////////////////////////////////////
В корне приложения лежит backup таблицы
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
В шаблоне должны быть подключены jquery и bootstrap css
<script src="{{ MEDIA_URL}}js/jquery-1.9.1.min.js"></script>
<link rel="stylesheet" type="text/css" href="{{ MEDIA_URL }}js/bootstrap/css/bootstrap.min.css">

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

В шаблоне:
1) Подгружается модуль с шаблонными тегами
{% load complaint_tags %}

2) Подключаем javascript
{% block extra_media %}{% get_comlaint_js %}{% endblock %}

3) Используем шаблонный тег get_complaint
{% get_complaint %}