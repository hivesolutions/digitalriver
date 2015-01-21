{% extends "partials/layout_simple.html.tpl" %}
{% block links %}
    {% if link == "home" %}
        <a href="{{ url_for('base.index') }}" class="active">home</a>
    {% else %}
        <a href="{{ url_for('base.index') }}">home</a>
    {% endif %}
    //
    {% if link == "droplets" %}
        <a href="{{ url_for('droplet.list') }}" class="active">droplets</a>
    {% else %}
        <a href="{{ url_for('droplet.list') }}">droplets</a>
    {% endif %}
    //
    {% if link == "provisions" %}
        <a href="{{ url_for('provision.list') }}" class="active">provisions</a>
    {% else %}
        <a href="{{ url_for('provision.list') }}">provisions</a>
    {% endif %}
    //
    {% if link == "about" %}
        <a href="{{ url_for('base.about') }}" class="active">about</a>
    {% else %}
        <a href="{{ url_for('base.about') }}">about</a>
    {% endif %}
{% endblock %}
