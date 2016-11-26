from datasimulation.TransactionManager import TransactionManager
from classifier_trainer import get_training_data
from classification.classify import load_model
import numpy as np


def predict(path_to_user_data):
    # Load model
    model = load_model('./model_architecture.json', './model_weights.h5', 'sgd')

    # Load data from path
    tm = TransactionManager()
    tm.load(path_to_user_data)
    user_transactions = tm.accounts['1']

    # Cluster data
    x_data, y_true, unique_labels = get_training_data(user_transactions=user_transactions)

    # Predict classes
    y_pred = model.predict_classes(x_data.as_matrix(), batch_size=17)
    real_classes = []
    for i in y_true:
        real_classes.append(np.where(i == 1)[0][0])
    # for i in range(len(y_pred)):
    #     predicted_label = unique_labels[y_pred[i]]
    #     true_label = unique_labels[real_classes[i]]
    #     print(predicted_label, true_label)
    # print(list(y_pred))
    # print(real_classes)
    return x_data, y_pred, unique_labels


if __name__ == '__main__':
    clusters, labels, unique_labels = predict('./datasimulation/tm.json')
    # TODO: budget
    budget = 2000
    # TODO: merge clusters with same label
    # TODO: dict with thresholds (% of monthly budget) for all labels
    threshold = {
        'dinner': budget * 0.1
    }
    # TODO: trigger hints for all lables where sum exceeds threshold
