"""
Tests for the DELETE /activities/{activity_name}/signup endpoint
"""
import pytest


def test_unsignup_from_activity_success(client):
    """Test successful removal from an activity"""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.delete(f"/activities/Chess Club/signup?email={email}")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert "Chess Club" in data["message"]


def test_unsignup_removes_participant_from_activity(client):
    """Test that unsignup actually removes the student from the activity"""
    email = "daniel@mergington.edu"  # Already in Chess Club
    
    # Verify student is in activity before removal
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]
    
    # Remove the student
    response = client.delete(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200
    
    # Verify the student was removed
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unsignup_from_different_activities(client):
    """Test that a student can be removed from different activities"""
    activities_to_remove = {
        "Chess Club": "michael@mergington.edu",
        "Programming Class": "emma@mergington.edu",
        "Gym Class": "john@mergington.edu"
    }
    
    for activity, email in activities_to_remove.items():
        response = client.delete(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
    
    # Verify students are removed from all activities
    activities_data = client.get("/activities").json()
    for activity, email in activities_to_remove.items():
        assert email not in activities_data[activity]["participants"]


def test_unsignup_from_nonexistent_activity(client):
    """Test that unsignup from non-existent activity returns 404"""
    response = client.delete("/activities/Nonexistent Club/signup?email=student@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unsignup_non_participant_raises_error(client):
    """Test that removing a non-participant raises an error"""
    email = "notamember@mergington.edu"  # Not in Chess Club
    
    response = client.delete(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "not a participant" in data["detail"]
