{% extends "partials/layout_droplet.html.tpl" %}
{% block title %}Droplets{% endblock %}
{% block name %}Droplet :: #{{ droplet.id }}{% endblock %}
{% block content %}
    <form action="{{ url_for('droplet.create_provision', id = droplet.id) }}" method="post" class="form provision">
        <input type="hidden" name="ptype" value="deploy" />
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
        <div class="label">
            <label>Options</label>
        </div>
        <div class="input">
            <div class="option">
                <span class="float-left">Force deployment ?</span>
                {% if provision.force %}
                    <input class="float-right" type="checkbox" name="force" checked="1" />
                {% else %}
                    <input class="float-right" type="checkbox" name="force" />
                {% endif %}
                <div class="clear"></div>
            </div>
        </div>
        <div class="extras"></div>
        <span class="button" data-link="{{ url_for('droplet.show', id = droplet.id) }}">Cancel</span>
        //
        <span class="button" data-submit="true">Provision</span>
    </form>
{% endblock %}
