{% extends "partials/layout_simple.html.tpl" %}
{% block htitle %}{{ own.description }} / {% block title %}{% endblock %}{% endblock %}
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
    {% if link == "about" %}
        <a href="{{ url_for('base.about') }}" class="active">about</a>
    {% else %}
        <a href="{{ url_for('base.about') }}">about</a>
    {% endif %}
{% endblock %}
