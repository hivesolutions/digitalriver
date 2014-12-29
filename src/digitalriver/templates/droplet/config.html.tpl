{% extends "partials/layout_droplet.html.tpl" %}
{% block title %}Droplets{% endblock %}
{% block name %}Droplet :: #{{ droplet.id }}{% endblock %}
{% block content %}
     <form action="{{ url_for('droplet.do_config', id = droplet.id) }}" method="post" class="form">
        <table class="table table-edit" data-error="{{ errors.names }}{{ errors.values }}">
            <thead>
                <tr>
                    <th data-width="270">Name</th>
                    <th data-width="270">Value</th>
                </tr>
            </thead>
            <tbody>
                <tr class="template">
                    <td>
                        <input type="text" name="names" class="text-field" />
                    </td>
                    <td>
                        <input type="text" name="values" class="text-field" />
                    </td>
                </tr>
                {% for name, value in instance.join_config()  %}
                    <tr>
                        <td>
                            <input type="text" name="names" class="text-field" value="{{ name }}" />
                        </td>
                        <td>
                            <input type="text" name="values" class="text-field" value="{{ value }}" />
                        </td>
                    </tr>
                {% endfor %}
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
