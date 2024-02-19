window.onload = function() {
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                alert("{{ message }}");
            {% endfor %}
        {% endif %}
    {% endwith %}
};