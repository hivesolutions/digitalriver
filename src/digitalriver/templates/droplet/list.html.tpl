{% extends "partials/layout.html.tpl" %}
{% block title %}Droplets{% endblock %}
{% block name %}Droplets{% endblock %}
{% block content %}
    <ul class="filter" data-infinite="true" data-original_value="Search Droplets">
        <div class="data-source" data-url="{{ url_for('droplet.list_json') }}" data-type="json" data-timeout="0"></div>
        <li class="template clear">
            <div class="name"><a href="{{ url_for('droplet.show', id = 0) }}%[id]">%[name]</a></div>
            <div class="description">%[image.name]</div>
        </li>
        <div class="filter-no-results quote">
            No results found
        </div>
        <div class="filter-more">
            <span class="button more">Load more</span>
            <span class="button load">Loading</span>
        </div>
    </ul>
{% endblock %}
