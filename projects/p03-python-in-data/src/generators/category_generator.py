from datetime import datetime

import pandas as pd

from src.utils.faker_utils import build_faker


CATEGORY_ROWS = [
    {"category_id": 1, "category_name": "Electronics", "parent_category_id": None, "level": 1},
    {"category_id": 2, "category_name": "Fashion", "parent_category_id": None, "level": 1},
    {"category_id": 3, "category_name": "Home & Living", "parent_category_id": None, "level": 1},
    {"category_id": 4, "category_name": "Beauty", "parent_category_id": None, "level": 1},
    {"category_id": 5, "category_name": "Sports", "parent_category_id": None, "level": 1},
    {"category_id": 6, "category_name": "Mobile Phones", "parent_category_id": 1, "level": 2},
    {"category_id": 7, "category_name": "Laptops", "parent_category_id": 1, "level": 2},
    {"category_id": 8, "category_name": "Cameras", "parent_category_id": 1, "level": 2},
    {"category_id": 9, "category_name": "Audio", "parent_category_id": 1, "level": 2},
    {"category_id": 10, "category_name": "Gaming", "parent_category_id": 1, "level": 2},
    {"category_id": 11, "category_name": "Men Clothing", "parent_category_id": 2, "level": 2},
    {"category_id": 12, "category_name": "Women Clothing", "parent_category_id": 2, "level": 2},
    {"category_id": 13, "category_name": "Shoes", "parent_category_id": 2, "level": 2},
    {"category_id": 14, "category_name": "Bags", "parent_category_id": 2, "level": 2},
    {"category_id": 15, "category_name": "Kitchen", "parent_category_id": 3, "level": 2},
    {"category_id": 16, "category_name": "Furniture", "parent_category_id": 3, "level": 2},
    {"category_id": 17, "category_name": "Decor", "parent_category_id": 3, "level": 2},
    {"category_id": 18, "category_name": "Bedding", "parent_category_id": 3, "level": 2},
    {"category_id": 19, "category_name": "Skincare", "parent_category_id": 4, "level": 2},
    {"category_id": 20, "category_name": "Makeup", "parent_category_id": 4, "level": 2},
    {"category_id": 21, "category_name": "Hair Care", "parent_category_id": 4, "level": 2},
    {"category_id": 22, "category_name": "Fragrance", "parent_category_id": 4, "level": 2},
    {"category_id": 23, "category_name": "Fitness Equipment", "parent_category_id": 5, "level": 2},
    {"category_id": 24, "category_name": "Outdoor Gear", "parent_category_id": 5, "level": 2},
    {"category_id": 25, "category_name": "Team Sports", "parent_category_id": 5, "level": 2},
]


def generate_categories(row_count: int = 10) -> pd.DataFrame:
    fake = build_faker()
    rows = [
        {
            **category,
            "created_at": fake.date_time_between(
                start_date=datetime(2024, 1, 1),
                end_date=datetime(2024, 12, 31, 23, 59, 59),
            ),
        }
        for category in CATEGORY_ROWS[:row_count]
    ]

    return pd.DataFrame(rows)
