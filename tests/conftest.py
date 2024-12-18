import pytest
from unittest.mock import patch, MagicMock
import src.main as main

@pytest.fixture(autouse=True)
def reset_globals():
    """Reset global variables before each test"""
    # Store original values
    original_values = {
        'timer': main.timer,
        'reps': main.reps,
        'work_sessions': main.work_sessions,
        'is_paused': main.is_paused,
        'remaining_time': main.remaining_time,
        'current_mode': main.current_mode
    }
    
    yield
    
    # Reset to original values after test
    main.timer = None
    main.reps = 0
    main.work_sessions = 0
    main.is_paused = False
    main.remaining_time = 0
    main.current_mode = ""
