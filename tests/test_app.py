from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_all():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # expect at least one of the predefined keys
    assert "Basketball" in data


def test_signup_and_unregister_flow():
    # choose an activity and a fresh email
    activity_name = "Basketball"
    email = "teststudent@example.com"

    # ensure email is not already part of the activity
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    # signup
    signup_resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert signup_resp.json()["message"] == f"Signed up {email} for {activity_name}"

    # signup again should fail
    signup_resp2 = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_resp2.status_code == 400

    # unregister the email
    unreg_resp = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert unreg_resp.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert unreg_resp.json()["message"] == f"Unregistered {email} from {activity_name}"

    # unregister again should fail
    unreg_resp2 = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert unreg_resp2.status_code == 400
