"""Manual recommendation smoke test for a specific account.

Set TEST_USER_ID to an existing account that owns monitoring_id before running:
    TEST_USER_ID=1 python test_recommendation.py
"""
import os



def main():
    from services.recommendation_service import generate_recommendation

    user_id = os.getenv("TEST_USER_ID")
    if not user_id:
        raise RuntimeError("Set TEST_USER_ID to the account ID that owns the monitoring record.")
    result = generate_recommendation(monitoring_id=1, fase_id=1, user_id=int(user_id))
    print(result)


if __name__ == "__main__":
    main()
