{% extends "partials/layout_droplet.html.tpl" %}
{% block title %}Droplets{% endblock %}
{% block name %}Droplet :: #{{ droplet.id }}{% endblock %}
{% block content %}
    <div class="quote">{{ droplet.name }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">image</td>
                <td class="left value" width="50%">{{ droplet.image.name }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">region</td>
                <td class="left value" width="50%">{{ droplet.region.slug }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">memory</td>
                <td class="left value" width="50%">{{ droplet.memory }} MB</td>
            </tr>
            <tr>
                <td class="right label" width="50%">vcpus</td>
                <td class="left value" width="50%">{{ droplet.vcpus }} CPU(s)</td>
            </tr>
            <tr>
                <td class="right label" width="50%">disk</td>
                <td class="left value" width="50%">{{ droplet.disk }} GB</td>
            </tr>
            <tr>
                <td class="right label" width="50%">ip v4</td>
                <td class="left value" width="50%">{{ droplet.networks.v4[0].ip_address }}</td>
            </tr>
            {% if droplet.networks.v6 %}
                <tr>
                    <td class="right label" width="50%">ip v6</td>
                    <td class="left value" width="50%">{{ droplet.networks.v6[0].ip_address }}</td>
                </tr>
            {% endif %}
            <tr>
                <td class="right label" width="50%">features</td>
                <td class="left value" width="50%">
                    {% if droplet.features %}
                        {% for feature in droplet.features %}
                            {{ feature }}{% if not loop.last %},{% endif %}
                        {% endfor %}
                    {% else %}
                        n/a
                    {% endif %}
                </td>
            </tr>
        </tbody>
    </table>
{% endblock %}
