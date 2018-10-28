import abc


class CodeFactory(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_import_code(self):
        pass

    @abc.abstractmethod
    def get_dataset_code(self):
        pass

    @abc.abstractmethod
    def get_feature_selection_code(self, parameters):
        pass

    @abc.abstractmethod
    def get_test_size_selection_code(self, test_size):
        pass

    @abc.abstractmethod
    def get_algorithm_selection_code(self):
        pass

    def get_code(self, parameters, test_size):
        return self.get_import_code()+self.get_dataset_code()\
               + self.get_feature_selection_code(parameters) + \
               self.get_test_size_selection_code(test_size) \
               + self.get_algorithm_selection_code()


# ConcereteFactory
class AbaloneLinearRegressionFactory(CodeFactory):

    def get_import_code(self):
        return CPImportCodeLinearRegression().get_code()

    def get_dataset_code(self):
        return CPDatasetCodeAbalone().get_code()

    def get_feature_selection_code(self, parameters):
        return CPFeatureSelectionCode().get_code(parameters)

    def get_test_size_selection_code(self, test_size):
        return CPTestSizeSelectionCode().get_code(test_size)

    def get_algorithm_selection_code(self):
        return CPAlgorithmSelectionCodeLinearRegression().get_code()


# ConcereteFactory
class BreastCancerLogisticRegressionFactory(CodeFactory):

    def get_import_code(self):
        return CPImportCodeLogisticRegression().get_code()

    def get_dataset_code(self):
        return CPDatasetCodeBreastCancer().get_code()

    def get_feature_selection_code(self, parameters):
        return CPFeatureSelectionCode().get_code(parameters)

    def get_test_size_selection_code(self, test_size):
        return CPTestSizeSelectionCode().get_code(test_size)

    def get_algorithm_selection_code(self):
        return CPAlgorithmSelectionCodeLogisticRegression().get_code()


# AbstractProduct
class APImportCode(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_code(self):
        pass


# ConcreteProduct
class CPImportCodeLinearRegression(APImportCode):
    def get_code(self):
        return 'import pandas as pd<br/>' \
               'import numpy as np<br/>' \
               'from sklearn.model_selection import train_test_split<br/>' \
               'from sklearn.linear_model import LinearRegression<br/>' \
               'from sklearn.metrics import mean_squared_error<br/>'


# ConcreteProduct
class CPImportCodeLogisticRegression(APImportCode):
    def get_code(self):
        return 'import pandas as pd<br/>' \
               'import numpy as np<br/>' \
               'from sklearn.model_selection import train_test_split<br/>' \
               'from sklearn.linear_model import LogisticRegression<br/>' \
               'from sklearn.metrics import accuracy_score<br/>'


# AbstractProduct
class APDatasetCode(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_code(self):
        pass


# ConcreteProduct
class CPDatasetCodeAbalone(APDatasetCode):
    def get_code(self):
        return 'df = pd.read_csv(\'abalone.csv\',sep=\',\', header=None)<br/>' \
               'arr = np.array(df)<br/>' \
               'X =arr[:,0:7]<br/>' \
               'y=arr[:,7]<br/>'


# ConcreteProduct
class CPDatasetCodeBreastCancer(APDatasetCode):
    def get_code(self):
        return 'df = pd.read_csv(\'breast_cancer.csv\',sep= \',\' , header=None)<br/>' \
               'arr = np.array(df)<br/>' \
               'X =arr[:,0:9]<br/>' \
               'y=arr[:,9]<br/>'


# AbstractProduct
class APFeatureSelectionCode(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_code(self, parameters):
        pass


# ConcreteProduct
class CPFeatureSelectionCode(APFeatureSelectionCode):
    def get_code(self, parameters):
        ret = 'selections = np.array('
        ret += str(parameters)+')<br/>X=X[:, selections]<br/>'
        return ret


# AbstractProduct
class APTestSizeSelectionCode(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_code(self, test_size):
        pass


# ConcreteProduct
class CPTestSizeSelectionCode(APTestSizeSelectionCode):
    def get_code(self, test_size):
        return 'X_train, X_test, y_train, y_test = train_test_split(X, y, test_size='+str(test_size) +\
               ', random_state=42)<br/>'


# AbstractProduct
class APAlgorithmSelectionCode(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_code(self):
        pass


# ConcreteProduct
class CPAlgorithmSelectionCodeLinearRegression(APAlgorithmSelectionCode):
    def get_code(self):
        return 'clf = LinearRegression()<br/>' \
               'clf.fit(X_train,y_train)<br/>' \
               'y_pred = clf.predict(X_test)<br/>' \
               'print(mean_squared_error(y_pred,y_test))<br/>'


# ConcreteProduct
class CPAlgorithmSelectionCodeLogisticRegression(APAlgorithmSelectionCode):
    def get_code(self):
        return 'clf = LogisticRegression()<br/>' \
               'clf.fit(X_train,y_train)<br/>' \
               'y_pred = clf.predict(X_test)<br/>' \
               'print(accuracy_score(y_pred,y_test))<br/>'
