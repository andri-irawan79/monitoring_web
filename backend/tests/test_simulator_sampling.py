from pathlib import Path

import pandas as pd

from backend.simulator.simulator import (
    DATASET_PATH,
    FRUIT_LABELS,
    RECORD_LIMIT,
    SAMPLE_QUOTAS,
    SAMPLE_SEED,
    load_sample,
)


def test_simulator_samples_only_the_six_reference_fruit_labels():
    sampled = load_sample()

    assert len(sampled) == RECORD_LIMIT == 365
    assert set(sampled["label"].unique()) == set(FRUIT_LABELS)
    assert sampled["label"].value_counts().to_dict() == SAMPLE_QUOTAS


def test_simulator_sampling_matches_zip_reference_algorithm():
    source = pd.read_csv(DATASET_PATH)
    fruit_rows = source[source["label"].isin(FRUIT_LABELS)].copy()

    assert len(fruit_rows) == 600

    # Replikasi tepat algoritma riset/siapkan_data.py pada skripsi-durian.zip:
    # sample per label dengan seed 42, gabungkan, lalu acak kembali dengan seed 42.
    expected_groups = [
        group.sample(n=SAMPLE_QUOTAS[label], random_state=SAMPLE_SEED)
        for label, group in fruit_rows.groupby("label")
    ]
    expected = (
        pd.concat(expected_groups)
        .sample(frac=1.0, random_state=SAMPLE_SEED)
        .reset_index(drop=True)
    )

    actual = load_sample()
    pd.testing.assert_frame_equal(actual, expected)


def test_dataset_contains_expected_source_file():
    assert Path(DATASET_PATH).is_file()
