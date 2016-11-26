from datasimulation.TransactionManager import TransactionManager
from classifier_trainer import get_training_data
from classification.classify import load_model


def predict(path):
    # Load model
    model = load_model('./model_architecture.json', './model_weights.h5', 'sgd')

    # Load data from path
    tm = TransactionManager()
    tm.load(path)
    user_transactions = tm.accounts['1']

    # Cluster data
    x_data, y_true = get_training_data(user_transactions)

    # Predict classes
    y_pred = model.predict_classes(x_data, batch_size=17)
    print(y_true)
    print(y_pred)
    return x_data, y_pred


if __name__ == '__main__':
    clusters, labels = predict('./datasimulation/tm.json')
