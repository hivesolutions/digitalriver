{% extends "partials/layout_droplet.html.tpl" %}
{% block title %}Droplets{% endblock %}
{% block name %}Droplet #{{ droplet.id }}{% endblock %}
{% block content %}
    {% for feature in droplet.features %}
        <div>{{ feature }}</div>
    {% endfor %}
{% endblock %}
