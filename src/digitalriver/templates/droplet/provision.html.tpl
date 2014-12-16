{% extends "partials/layout_droplet.html.tpl" %}
{% block title %}Droplets{% endblock %}
{% block name %}Droplet #{{ droplet.id }}{% endblock %}
{% block content %}
    <form action="{{ url_for('droplet.create_provision', id = droplet.id) }}" method="post" class="form">
        <input type="hidden" name="droplet_id" value="{{ droplet.id }}" />
        <input type="hidden" name="droplet_address" value="{{ droplet.networks.v4[0].ip_address }}" />
        <div class="label">
            <label>Name</label>
        </div>
         <div class="input">
            <input class="text-field" value="{{ droplet.name }}" data-disabled="1" />
        </div>
        <div class="label">
            <label>Image</label>
        </div>
         <div class="input">
            <input class="text-field" value="{{ droplet.image.name }}" data-disabled="1" />
        </div>
        <div class="label">
            <label>URL</label>
        </div>
        <div class="input">
            <input class="text-field" name="url" placeholder="eg: https://github.com/hivesolutions/example" value="{{ provision.url }}"
                   data-error="{{ errors.url }}" />
        </div>
        <span class="button" data-link="{{ url_for('droplet.show', username = droplet.id) }}">Cancel</span>
        //
        <span class="button" data-submit="true">Provision</span>
    </form>
{% endblock %}