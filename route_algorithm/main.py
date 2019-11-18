import numpy as np


def ahp(comparison):
  random_index = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]

  criteria_w = np.mean(comparison / comparison.sum(axis=0), axis=1)
  lambda_max = np.mean(np.sum(comparison * criteria_w, axis=1) / criteria_w)
  consistency_index = (lambda_max - len(comparison)) / (len(comparison) - 1)
  consistency_ratio = consistency_index / random_index[len(comparison) - 1]

  print('Consistency ratio is:', consistency_ratio)
  return criteria_w


# Criteria
# distance, rating, satisfaction

ahp(np.array([[1, 5, 11],
              [1/5, 1, 5],
              [1/11, 1/5, 1]]))
