"""Newly designed schema; these proxies are not questionnaire items."""

ATTITUDE_COLUMNS = (
    "price_attention",
    "meal_planning_interest",
    "convenience_preference",
    "discovery_interest",
    "cooking_interest",
    "shopping_time_pressure",
    "cross_category_interest",
)
BEHAVIOR_COLUMNS = ("monthly_store_visits", "weekly_other_channel_visits")
REQUIRED_COLUMNS = ("participant_id", "data_status", *BEHAVIOR_COLUMNS, *ATTITUDE_COLUMNS)
SYNTHETIC_NOTICE = (
    "SYNTHETIC: illustrative results on independently generated data; "
    "not findings from the ADK consumer survey."
)
