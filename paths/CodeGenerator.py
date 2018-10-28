from flask import render_template, Blueprint, request
from Service.CodeGenerator import CodeGenerator as service

app = Blueprint('code_generator', __name__)


@app.route('/code-generator/', methods=['POST', 'GET'])
def code_generator():
    if request.method == 'POST':
        return service.code_generator(request.form)
    else:
        return render_template(
            'code_generator/code_generator.html', **locals())


@app.route('/code-generator/get-dataset', methods=['POST', 'GET'])
def code_generator_get_data():
    if request.method == 'POST':
        return service.code_generator_get_data(request.form)


@app.route('/code-generator/get-feature-distribution', methods=['POST', 'GET'])
def code_generator_get_feature_distribution():
    if request.method == 'POST':
        return service.code_generator_get_feature_distribution(request.form['dataset'], request.form['feature'])