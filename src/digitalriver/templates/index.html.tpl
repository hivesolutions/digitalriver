{% extends "partials/layout.html.tpl" %}
{% block title %}Deploy{% endblock %}
{% block name %}Welcome To DigitalRiver{% endblock %}
{% block content %}
    <div class="quote">
        DigitalRiver is a simple web application for testing of DigitalOcean API infra-structure system.<br />
        To be able to access the system please use you <strong>DigitalOcean account</strong>.
    </div>
    <div class="button login" data-link="{{ url_for('base.deploy') }}"></div>
{% endblock %}
