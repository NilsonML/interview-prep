"""Тесты ML с нуля: сверка с sklearn и с известными свойствами алгоритмов."""

import numpy as np
import pytest
from sklearn import metrics as skm
from sklearn.datasets import make_blobs, make_classification
from sklearn.linear_model import LogisticRegression as SkLogisticRegression

from ml_basics import metrics as m
from ml_basics import models as md
from ml_basics import preprocessing as pp

rng = np.random.default_rng(0)

# ---------------------------------------------------------------- metrics


def test_confusion_and_prf():
    y_true = rng.integers(0, 2, 200)
    y_pred = rng.integers(0, 2, 200)
    assert np.array_equal(m.confusion_matrix(y_true, y_pred), skm.confusion_matrix(y_true, y_pred))
    p, r, f1 = m.precision_recall_f1(y_true, y_pred)
    assert p == pytest.approx(skm.precision_score(y_true, y_pred))
    assert r == pytest.approx(skm.recall_score(y_true, y_pred))
    assert f1 == pytest.approx(skm.f1_score(y_true, y_pred))
    assert m.precision_recall_f1(np.array([0, 0]), np.array([0, 0])) == (0.0, 0.0, 0.0)


def test_roc_auc_matches_sklearn_with_ties():
    for _ in range(20):
        y = rng.integers(0, 2, 300)
        scores = rng.integers(0, 10, 300).astype(float)  # много одинаковых скоров
        if y.min() == y.max():
            continue
        assert m.roc_auc(y, scores) == pytest.approx(skm.roc_auc_score(y, scores))
    assert m.roc_auc(np.array([0, 0, 1, 1]), np.array([0.1, 0.2, 0.8, 0.9])) == 1.0


def test_log_loss_and_r2():
    y = rng.integers(0, 2, 100)
    p = rng.uniform(0, 1, 100)
    assert m.log_loss(y, p) == pytest.approx(skm.log_loss(y, p))
    assert np.isfinite(m.log_loss(np.array([1, 0]), np.array([0.0, 1.0])))  # без log(0)
    y_true = rng.normal(size=50)
    y_pred = y_true + rng.normal(scale=0.3, size=50)
    assert m.r2_score(y_true, y_pred) == pytest.approx(skm.r2_score(y_true, y_pred))


# ---------------------------------------------------------------- preprocessing


def test_train_test_split_stratified():
    X = np.arange(100).reshape(-1, 1)
    y = np.array([0] * 80 + [1] * 20)
    X_tr, X_te, y_tr, y_te = pp.train_test_split(X, y, test_size=0.25, seed=1, stratify=True)
    assert len(X_te) == 25 and len(X_tr) == 75
    assert y_te.sum() == 5  # 25% от 20 положительных
    assert set(X_tr.ravel()) | set(X_te.ravel()) == set(range(100))
    assert not set(X_tr.ravel()) & set(X_te.ravel())
    again = pp.train_test_split(X, y, test_size=0.25, seed=1, stratify=True)
    assert np.array_equal(again[1], X_te)  # детерминизм по seed


def test_k_fold_indices():
    folds = pp.k_fold_indices(103, 5, seed=0)
    assert len(folds) == 5
    val = np.concatenate([v for _, v in folds])
    assert sorted(val) == list(range(103))  # каждый объект ровно раз в валидации
    sizes = [len(v) for _, v in folds]
    assert max(sizes) - min(sizes) <= 1
    for tr, v in folds:
        assert not set(tr) & set(v) and len(tr) + len(v) == 103


def test_standard_scaler():
    X = rng.normal(5, 3, size=(200, 3))
    X[:, 2] = 7.0  # константный столбец
    sc = pp.StandardScaler().fit(X)
    Z = sc.transform(X)
    assert np.allclose(Z[:, :2].mean(0), 0) and np.allclose(Z[:, :2].std(0), 1)
    assert np.all(np.isfinite(Z)) and np.allclose(Z[:, 2], 0)
    X_new = rng.normal(size=(5, 3))
    assert np.allclose(
        sc.transform(X_new), (X_new - X.mean(0)) / np.where(X.std(0) == 0, 1, X.std(0))
    )


def test_one_hot():
    assert np.array_equal(pp.one_hot(np.array([0, 2, 1])), np.eye(3)[[0, 2, 1]])
    assert pp.one_hot(np.array([1]), n_classes=4).shape == (1, 4)


# ---------------------------------------------------------------- models


@pytest.mark.parametrize("method", ["normal", "gd"])
def test_linear_regression(method):
    X = rng.normal(size=(300, 3))
    true_w, true_b = np.array([2.0, -1.0, 0.5]), 3.0
    y = X @ true_w + true_b + rng.normal(scale=0.01, size=300)
    model = md.LinearRegression(method=method).fit(X, y)
    assert np.allclose(model.coef_, true_w, atol=0.02)
    assert model.intercept_ == pytest.approx(true_b, abs=0.02)
    assert m.r2_score(y, model.predict(X)) > 0.999


def test_sigmoid_is_stable():
    z = np.array([-1000.0, 0.0, 1000.0])
    with np.errstate(over="raise"):  # переполнение exp превратится в ошибку
        s = md.sigmoid(z)
    assert np.allclose(s, [0.0, 0.5, 1.0])


def test_logistic_regression():
    X, y = make_classification(n_samples=500, n_features=5, n_informative=3, random_state=0)
    model = md.LogisticRegression(lr=0.5, n_iter=3000).fit(X, y)
    proba = model.predict_proba(X)
    assert proba.shape == (500,) and np.all((proba >= 0) & (proba <= 1))
    reference = SkLogisticRegression().fit(X, y).score(X, y)
    assert (model.predict(X) == y).mean() >= reference - 0.02  # не хуже sklearn
    strong = md.LogisticRegression(lr=0.5, n_iter=3000, l2=1.0).fit(X, y)
    assert np.linalg.norm(strong.coef_) < np.linalg.norm(model.coef_)  # L2 сжимает веса


def test_knn():
    X, y = make_blobs(n_samples=300, centers=3, cluster_std=0.8, random_state=1)
    knn = md.KNNClassifier(k=5).fit(X[:200], y[:200])
    assert (knn.predict(X[200:]) == y[200:]).mean() > 0.95
    one = md.KNNClassifier(k=1).fit(X, y)
    assert np.array_equal(one.predict(X), y)  # 1-NN на обучающей выборке без ошибок


def test_kmeans():
    centers = np.array([[0, 0], [10, 10], [0, 10]])
    X, labels = make_blobs(n_samples=300, centers=centers, cluster_std=0.5, random_state=2)
    km = md.KMeans(k=3, n_init=10, seed=0).fit(X)
    assert km.cluster_centers_.shape == (3, 2) and km.labels_.shape == (300,)
    # Каждый найденный центр близок к одному из истинных
    for c in km.cluster_centers_:
        assert np.min(np.linalg.norm(centers - c, axis=1)) < 0.5
    assert km.inertia_ == pytest.approx(((X - km.cluster_centers_[km.labels_]) ** 2).sum())
    assert np.array_equal(km.predict(X), km.labels_)
    single = md.KMeans(k=3, n_init=1, seed=0).fit(X)
    assert km.inertia_ <= single.inertia_ + 1e-9  # лучший из 10 запусков не хуже одного
