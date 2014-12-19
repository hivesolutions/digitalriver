{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "info" %}
            <a href="{{ url_for('provision.show', pid = provision.pid) }}" class="active">info</a>
        {% else %}
            <a href="{{ url_for('provision.show', pid = provision.pid) }}">info</a>
        {% endif %}
        //
        {% if sub_link == "log" %}
            <a href="{{ url_for('provision.log', pid = provision.pid) }}" class="active">log</a>
        {% else %}
            <a href="{{ url_for('provision.log', pid = provision.pid) }}">log</a>
        {% endif %}
    </div>
{% endblock %}
