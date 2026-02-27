"""
Tests for the GET /activities endpoint
"""
import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all 9 activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 9
    
    # Verify all expected activity names are present
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Music Band",
        "Debate Team",
        "Science Club"
    ]
    assert set(data.keys()) == set(expected_activities)


def test_get_activities_has_correct_structure(client):
    """Test that each activity has the required fields"""
    response = client.get("/activities")
    data = response.json()
    
    # Check first activity for structure
    activity = data["Chess Club"]
    
    # Verify required fields exist
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    
    # Verify field types
    assert isinstance(activity["description"], str)
    assert isinstance(activity["schedule"], str)
    assert isinstance(activity["max_participants"], int)
    assert isinstance(activity["participants"], list)


def test_get_activities_has_correct_initial_participants(client):
    """Test that activities have the correct initial participants"""
    response = client.get("/activities")
    data = response.json()
    
    # Verify Chess Club has initial participants
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
    
    # Verify Programming Class has initial participants
    assert "emma@mergington.edu" in data["Programming Class"]["participants"]
    assert "sophia@mergington.edu" in data["Programming Class"]["participants"]
