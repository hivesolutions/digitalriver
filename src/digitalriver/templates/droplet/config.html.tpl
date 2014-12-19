{% extends "partials/layout_droplet.html.tpl" %}
{% block title %}Droplets{% endblock %}
{% block name %}Droplet #{{ droplet.id }}{% endblock %}
{% block content %}
 	<form action="{{ url_for('droplet.do_config', id = droplet.id) }}" method="post" class="form">
        <table class="table table-edit" data-error="{{ errors.prices }}">
            <input name="address" type="hidden" class="table-empty-field" value="{{ droplet.networks.v4[0].ip_address }}" />
            <thead>
                <tr>
                    <th data-width="270">Name</th>
                    <th data-width="270">Value</th>
                </tr>
            </thead>
            <tbody>
                <tr class="template">
                    <td>
                        <input type="text" name="config[][name]" class="text-field" />
                    </td>
                    <td>
                        <input type="text" name="config[][value]" class="text-field" />
                    </td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <td class="table-new-line-row">
                        <span class="button table-new-line">Add Line</span>
                    </td>
                </tr>
            </tfoot>
        </table>
        <span class="button" data-link="{{ url_for('droplet.show', id = droplet.id) }}">Cancel</span>
        //
        <span class="button" data-submit="true">Submit</span>
    </form>
{% endblock %}
