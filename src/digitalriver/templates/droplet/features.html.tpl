{% extends "partials/layout_droplet.html.tpl" %}
{% block title %}Droplets{% endblock %}
{% block name %}Droplet :: #{{ droplet.id }}{% endblock %}
{% block content %}
    <div class="features">
        {% for feature in instance.features %}
            <div class="feature">
                <div class="description">
                    <h2 class="name">{{ instance.fname(feature) }}</h2>
                    <h3 class="status running">running</h3>
                </div>
                <div class="actions">
                    <div class="line">
                        <a href="#">stop</a>
                    </div>
                    <div class="line">
                        <a href="{{ url_for('droplet.remove_feature', id = droplet.id, feature = feature) }}" class="warning link-confirm"
                           data-message="Do you really want to remove {{ instance.fname(feature) }} ?">remove</a>
                        //
                        <a href="{{ url_for('droplet.rebuild_feature', id = droplet.id, feature = feature) }}" class="warning link-confirm"
                           data-message="Do you really want to rebuild {{ instance.fname(feature) }} ?">rebuild</a>
                    </div>
                </div>
                <div class="clear"></div>
            </div>
        {% endfor %}
    </div>
{% endblock %}
