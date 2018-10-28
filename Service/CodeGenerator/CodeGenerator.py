from classes.CodeGenerator import AbstractCodeFactory
from classes.CodeGenerator import abalone
from classes.CodeGenerator import breast_cancer


def code_generator(data):
    dataset = data['dataset']
    algorithm = data['algorithm']
    testsize = '0.' + data['testsize']
    parameters = [];
    for item in data['selections'].split(','):
        if item == 'true':
            parameters.append(True);
        else:
            parameters.append(False);
    if dataset == '1' and algorithm == '1':
        return AbstractCodeFactory.AbaloneLinearRegressionFactory().get_code(parameters, testsize)
    if dataset == '2' and algorithm == '2':
        return AbstractCodeFactory.BreastCancerLogisticRegressionFactory().get_code(parameters, testsize)
    return 'Not Supported'


def code_generator_get_data(data):
    if data['type'] == '0':
        if data['data'] == '0':
            return abalone.get_dataset()
        elif data['data'] == '1':
            return breast_cancer.get_dataset()
    if data['type'] == '1':
        if data['data'] == '0':
            return abalone.get_X()
        elif data['data'] == '1':
            return breast_cancer.get_X()
    if data['type'] == '2':
        if data['data'] == '0':
            return abalone.get_y()
        elif data['data'] == '1':
            return breast_cancer.get_y()
    if data['type'] == '3':
        if data['data'] == '0':
            return abalone.get_X_select(data['selections'])
        elif data['data'] == '1':
            return breast_cancer.get_X_select(data['selections'])
    return '0'


def code_generator_get_feature_distribution(dataset, feature):
    if dataset == '0':
        return abalone.get_feature_distribution(feature)
    if dataset =='1':
        return breast_cancer.get_feature_distribution(feature)
    return '0'
