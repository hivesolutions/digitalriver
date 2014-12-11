<div id="footer">
    {% block footer %}
        &copy; Copyright 2008-2014 by <a href="http://hive.pt">Hive Solutions</a>.<br />
        {% if session['username'] %}<span>{{ session['username'] }}</span> // <a href="{{ url_for('base.logout') }}">logout</a><br />{% endif %}
    {% endblock %}
</div>
