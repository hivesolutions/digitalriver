{% extends "partials/layout_droplet.html.tpl" %}
{% block title %}Droplets{% endblock %}
{% block name %}Droplet :: #{{ droplet.id }}{% endblock %}
{% block content %}
    {% if instance.features %}
        <div class="features">
            {% for feature in instance.features %}
                <div class="feature">
                    <div class="description">
                        <h2 class="name">{{ feature.name }}</h2>
                        <h3 class="status running">running</h3>
                    </div>
                    <div class="actions">
                        <div class="line">
                            <a href="#">stop</a>
                        </div>
                        <div class="line">
                            <a href="{{ url_for('droplet.remove_feature', id = droplet.id, feature = feature.url) }}" class="warning link-confirm"
                               data-message="Do you really want to remove {{ feature.name }} ?">remove</a>
                            //
                            <a href="{{ url_for('droplet.rebuild_feature', id = droplet.id, feature = feature.url) }}" class="warning link-confirm"
                               data-message="Do you really want to rebuild {{ feature.name }} ?">rebuild</a>
                        </div>
                    </div>
                    <div class="clear"></div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="quote">
            There are currently <strong>no features for the droplet</strong> you can start by<br/>
            creating a <a href="{{ url_for('droplet.create_provision', id = droplet.id) }}">new provision</a>
            to add features to the current droplet.
        </div>
    {% endif %}
{% endblock %}
