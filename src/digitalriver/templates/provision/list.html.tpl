{% extends "partials/layout.html.tpl" %}
{% block title %}Provisions{% endblock %}
{% block name %}Provisions{% endblock %}
{% block content %}
    <ul class="filter" data-infinite="true" data-original_value="Search Provisions">
        <div class="data-source" data-url="{{ url_for('provision.list_json') }}" data-type="json" data-timeout="0"></div>
        <li class="template clear">
            <div class="name"><a href="{{ url_for('provision.show', id = 0) }}%[id]">%[id]</a></div>
            <div class="description">Droplet #%[droplet_id]</div>
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
