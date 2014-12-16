{% extends "partials/layout_provision.html.tpl" %}
{% block title %}Provisions{% endblock %}
{% block name %}{{ provision.id }}{% endblock %}
{% block content %}
    <div class="quote">{{ provision.id }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">droplet</td>
                <td class="left value" width="50%">
                    <a href="{{ url_for('droplet.show', id = provision.droplet_id) }}">#{{ provision.droplet_id }}</a>
                </td>
            </tr>
            <tr>
                <td class="right label" width="50%">url</td>
                <td class="left value" width="50%">{{ provision.url }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
