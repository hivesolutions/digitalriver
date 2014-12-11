{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "info" %}
            <a href="{{ url_for('droplet.show', id = droplet.id) }}" class="active">info</a>
        {% else %}
            <a href="{{ url_for('droplet.show', id = droplet.id) }}">info</a>
        {% endif %}
    </div>
{% endblock %}
