from software.ai_engine.dataset_generator import generate_synthetic_uz_dataset


def test_synthetic_dataset_has_expected_facilities_and_rows():
    data = generate_synthetic_uz_dataset(days=3, seed=7)
    assert len(data) > 3 * 40 * 20
    assert data["facility_id"].nunique() == 22
    assert {"normal", "kitchen_breakfast_peak"}.issubset(set(data["event_type"]))


def test_synthetic_dataset_is_physically_reasonable():
    data = generate_synthetic_uz_dataset(days=2, seed=9)
    assert (data["kva"] >= data["avg_kw"]).all()
    assert data["power_factor"].between(0.65, 1.0).all()
    assert (data["kwh"] > 0).all()
    assert (data["current_a"] >= 0).all()
