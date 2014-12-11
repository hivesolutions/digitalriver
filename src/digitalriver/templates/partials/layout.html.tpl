{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>DigitalRiver</title>
    {% endblock %}
</head>
<body class="ux romantic">
    <div id="header">
        {% block header %}
            <h1>{% block name %}{% endblock %}</h1>
            <div class="links">
                {% if link == "home" %}
                    <a href="{{ url_for('base.index') }}" class="active">home</a>
                {% else %}
                    <a href="{{ url_for('base.index') }}">home</a>
                {% endif %}
               	//
                {% if link == "customers" %}
                    <a href="{{ url_for('droplet.list') }}" class="active">customers</a>
                {% else %}
                    <a href="{{ url_for('droplet.list') }}">customers</a>
                {% endif %}
                //
                {% if link == "about" %}
                    <a href="{{ url_for('base.about') }}" class="active">about</a>
                {% else %}
                    <a href="{{ url_for('base.about') }}">about</a>
                {% endif %}
            </div>
        {% endblock %}
    </div>
    <div id="content">{% block content %}{% endblock %}</div>
    {% include "partials/footer.html.tpl" %}
</body>
{% include "partials/end_doctype.html.tpl" %}
