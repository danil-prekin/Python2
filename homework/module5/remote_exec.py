import shlex
import subprocess
from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

class ExecForm(FlaskForm):
    code = StringField('code', validators=[InputRequired()])
    timeout = IntegerField('timeout', validators=[InputRequired(), NumberRange(min=1, max=30)])

@app.route('/exec', methods=['POST'])
def execute_code():
    form = ExecForm()
    if not form.validate_on_submit():
        return jsonify({'errors': form.errors}), 400

    code = form.code.data
    timeout = form.timeout.data

    safe_code = shlex.quote(code)
    cmd = f'prlimit --nproc=1:1 python3 -c {safe_code}'

    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate(timeout=timeout)
        return jsonify({'stdout': stdout, 'stderr': stderr, 'returncode': proc.returncode})
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        return jsonify({'error': 'Execution timeout exceeded'}), 408

if __name__ == '__main__':
    app.run(debug=True)
