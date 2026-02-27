"""
Tests for the POST /activities/{activity_name}/signup endpoint
"""
import pytest


def test_signup_for_activity_success(client):
    """Test successful signup for an activity"""
    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the student to the activity"""
    email = "newstudent@mergington.edu"
    
    # Signup the student
    response = client.post(f"/activities/Programming Class/signup?email={email}")
    assert response.status_code == 200
    
    # Verify the student was added by fetching activities
    activities = client.get("/activities").json()
    assert email in activities["Programming Class"]["participants"]


def test_signup_for_different_activities(client):
    """Test that a student can sign up for different activities"""
    email = "student@mergington.edu"
    activities_to_join = ["Chess Club", "Art Studio", "Music Band"]
    
    for activity in activities_to_join:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
    
    # Verify student is in all activities
    activities_data = client.get("/activities").json()
    for activity in activities_to_join:
        assert email in activities_data[activity]["participants"]


def test_signup_for_nonexistent_activity(client):
    """Test that signup for non-existent activity returns 404"""
    response = client.post("/activities/Nonexistent Club/signup?email=student@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_raises_error(client):
    """Test that signing up again raises an error"""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    # Try to signup with email already in activity
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]
