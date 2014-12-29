{% extends "partials/layout.html.tpl" %}
{% block title %}Droplets{% endblock %}
{% block name %}Droplets{% endblock %}
{% block content %}
    <ul class="filter" data-infinite="1" data-no_input="1" data-number_records="20">
        <div class="data-source" data-url="{{ url_for('droplet.list_json') }}" data-type="json" data-timeout="0"></div>
        <li class="table-row table-header">
            <div class="text-left" data-width="280">Name</div>
            <div class="text-center" data-width="100">Memory</div>
            <div class="text-center" data-width="100">Disk</div>
            <div class="text-center" data-width="100">Region</div>
            <div class="table-clear"></div>
        </li>
        <li class="template table-row">
            <div class="text-left" data-width="280">
                <a href="{{ url_for('droplet.show', id = 0) }}%[id]">%[name]</a>
            </div>
            <div class="text-center" data-width="100">%[memory] MB</div>
            <div class="text-center" data-width="100">%[disk] GB</div>
            <div class="text-center" data-width="100">%[region.slug]</div>
            <div class="table-clear"></div>
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
