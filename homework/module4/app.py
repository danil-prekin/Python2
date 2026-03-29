import os
import shlex
import subprocess
from flask import Flask, request, render_template_string
from .forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

FORM_TEMPLATE = '''
<!doctype html>
<html>
<head><title>Registration</title></head>
<body>
    <h1>Registration Form</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <p>{{ form.email.label }} {{ form.email(size=30) }}</p>
        <p>{{ form.phone.label }} {{ form.phone(size=30) }}</p>
        <p>{{ form.name.label }} {{ form.name(size=30) }}</p>
        <p>{{ form.address.label }} {{ form.address(size=30) }}</p>
        <p>{{ form.index.label }} {{ form.index(size=30) }}</p>
        <p>{{ form.comment.label }} {{ form.comment(rows=3, cols=40) }}</p>
        <p><input type="submit" value="Submit"></p>
    </form>
    {% if errors %}
        <h2>Errors:</h2>
        <ul>
        {% for field, err_list in errors.items() %}
            <li>{{ field }}: {{ err_list|join(', ') }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
'''

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        return f'Registration successful for {form.name.data}!'
    return render_template_string(FORM_TEMPLATE, form=form, errors=form.errors)


@app.route('/uptime')
def uptime():
    try:
        result = subprocess.run(['uptime'], capture_output=True, text=True, check=True)
        uptime_str = result.stdout.strip()
        return f'Current uptime is {uptime_str}'
    except subprocess.CalledProcessError:
        return 'Error getting uptime', 500


@app.route('/ps')
def ps_endpoint():
    args = request.args.getlist('arg')
    if not args:
        return 'No arguments provided', 400
    safe_args = [shlex.quote(arg) for arg in args]
    command = f"ps {' '.join(safe_args)}"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = e.stderr or str(e)
    return f'<pre>{output}</pre>'


if __name__ == '__main__':
    app.run(debug=True)
