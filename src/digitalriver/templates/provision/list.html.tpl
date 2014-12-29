{% extends "partials/layout.html.tpl" %}
{% block title %}Provisions{% endblock %}
{% block name %}Provisions{% endblock %}
{% block content %}
    <ul class="filter" data-infinite="1" data-no_input="1">
        <div class="data-source" data-url="{{ url_for('provision.list_json') }}" data-type="json" data-timeout="0"></div>
        <li class="table-row table-header">
            <div class="text-left" data-width="100">Date</div>
            <div class="text-left" data-width="320">PID</div>
            <div class="text-right" data-width="80">Droplet</div>
            <div class="text-right" data-width="80">Status</div>
            <div class="table-clear"></div>
        </li>
        <li class="template table-row">
            <div class="text-left timestamp" data-width="100" data-format="%d/%m %H:%M">%[created]</div>
            <div class="text-left" data-width="320">
                <a href="{{ url_for('provision.show', pid = '') }}%[pid]">%[pid]</a>
            </div>
            <div class="text-right" data-width="80">
                <a href="{{ url_for('droplet.show', id = '') }}%[droplet_id]">#%[droplet_id]</a>
            </div>
            <div class="text-right" data-width="80">
                <span class="%[pstatus]">%[pstatus]</span>
            </div>
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
