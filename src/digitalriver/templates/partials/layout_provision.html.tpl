{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "info" %}
            <a href="{{ url_for('provision.show', id = provision.id) }}" class="active">info</a>
        {% else %}
            <a href="{{ url_for('provision.show', id = provision.id) }}">info</a>
        {% endif %}
        //
        {% if sub_link == "status" %}
            <a href="#" class="active">log</a>
        {% else %}
            <a href="#">log</a>
        {% endif %}
    </div>
{% endblock %}
