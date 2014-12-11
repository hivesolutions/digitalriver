{% extends "partials/layout_droplet.html.tpl" %}
{% block title %}Droplets{% endblock %}
{% block name %}{{ droplet.name }}{% endblock %}
{% block content %}
    <div class="quote">{{ droplet.name }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">name</td>
                <td class="left value" width="50%">{{ droplet.name }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
