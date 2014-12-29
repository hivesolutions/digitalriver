{% extends "partials/layout_provision.html.tpl" %}
{% block title %}Provisions{% endblock %}
{% block name %}Provision :: {{ provision.ptype }}{% endblock %}
{% block content %}
    <div class="quote">{{ provision.pid }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">status</td>
                <td class="left value" width="50%">
                    <span class="tag {{ provision.pstatus }}">{{ provision.pstatus }}</span>
                </td>
            </tr>
            <tr>
                <td class="right label" width="50%">type</td>
                <td class="left value" width="50%">{{ provision.ptype }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">droplet</td>
                <td class="left value" width="50%">
                    <a href="{{ url_for('droplet.show', id = provision.droplet_id) }}">#{{ provision.droplet_id }}</a>
                </td>
            </tr>
            <tr>
                <td class="right label" width="50%">url</td>
                <td class="left value" width="50%">
                    <a href="{{ provision.url }}">{{ provision.url.rsplit("/", 2)[1] }}</a>
                </td>
            </tr>
        </tbody>
    </table>
    {% if provision.config %}
        <div class="separator-horizontal"></div>
        <table>
            <tbody>
                {% for key, value in provision.config %}
                    <tr>
                        <td class="right label" width="50%">{{ key }}</td>
                        <td class="left value" width="50%">{{ value }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% endif %}
{% endblock %}
