{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "info" %}
            <a href="{{ url_for('droplet.show', id = droplet.id) }}" class="active">info</a>
        {% else %}
            <a href="{{ url_for('droplet.show', id = droplet.id) }}">info</a>
        {% endif %}
        //
        {% if sub_link == "provision" %}
            <a href="{{ url_for('droplet.provision', id = droplet.id) }}" class="active">provision</a>
        {% else %}
            <a href="{{ url_for('droplet.provision', id = droplet.id) }}">provision</a>
        {% endif %}
    </div>
{% endblock %}
