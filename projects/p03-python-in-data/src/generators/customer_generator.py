from datetime import datetime

import numpy as np
import pandas as pd

from src.utils.faker_utils import build_faker


GENDERS = ["Male", "Female"]


def generate_customers(row_count: int = 30_000) -> pd.DataFrame:
    fake = build_faker()
    data = {
        "customer_id": [customer_id for customer_id in range(1, row_count + 1)],
        "customer_name": [fake.name() for _ in range(row_count)],
        "email": [fake.unique.email() for _ in range(row_count)],
        "phone": [fake.unique.numerify(text="09########") for _ in range(row_count)],
        "gender": np.random.choice(GENDERS, size=row_count),
        "address": [fake.address().replace("\n", ", ")[:255] for _ in range(row_count)],
        "city": [fake.city() for _ in range(row_count)],
        "created_at": [
            fake.date_time_between(
                start_date=datetime(2024, 1, 1),
                end_date=datetime(2024, 12, 31, 23, 59, 59),
            )
            for _ in range(row_count)
        ],
    }

    fake.unique.clear()
    return pd.DataFrame(data)
