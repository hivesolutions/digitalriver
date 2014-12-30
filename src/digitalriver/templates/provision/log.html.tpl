{% extends "partials/layout_provision.html.tpl" %}
{% block title %}Provisions{% endblock %}
{% block name %}Provision :: {{ provision.ptype }}{% endblock %}
{% block content %}
    <div class="log" data-key="c4669efec89dfb6bddcbcbec5a259fe6adfd4f2cd1dff8b10a54ca1fca25a365"
         data-channel="{{ provision.pid }}">
        {% for line in provision.log %}
            <div class="line">{{ line|nl_to_br|sp_to_nbsp }}</div>
        {% endfor %}
    </div>
{% endblock %}
