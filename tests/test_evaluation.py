import pytest
from src.evaluation.run import ndcg_at_k


def test_ndcg_rewards_order_and_handles_no_relevance():
    assert ndcg_at_k([2, 1, 0]) == 1
    assert ndcg_at_k([0, 1, 2]) == pytest.approx(0.58688267)
    assert ndcg_at_k([0, 0, 0]) == 0
