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
        {% if sub_link == "features" %}
            <a href="{{ url_for('droplet.features', id = droplet.id) }}" class="active">features</a>
        {% else %}
            <a href="{{ url_for('droplet.features', id = droplet.id) }}">features</a>
        {% endif %}
        //
        {% if sub_link == "config" %}
            <a href="{{ url_for('droplet.config', id = droplet.id) }}" class="active">config</a>
        {% else %}
            <a href="{{ url_for('droplet.config', id = droplet.id) }}">config</a>
        {% endif %}
        //
        {% if sub_link == "provision" %}
            <a href="{{ url_for('droplet.new_provision', id = droplet.id) }}" class="active">provision</a>
        {% else %}
            <a href="{{ url_for('droplet.new_provision', id = droplet.id) }}">provision</a>
        {% endif %}
        //
        <a href="{{ url_for('droplet.sync', id = droplet.id) }}" class="warning link-confirm"
           data-message="Do you really want to sync #{{ droplet.id }}  ?">sync</a>
    </div>
{% endblock %}
