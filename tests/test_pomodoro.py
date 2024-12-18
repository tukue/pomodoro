import pytest
from tkinter import *
from unittest.mock import MagicMock, patch
import src.main as main  # Import main module at the top level

@pytest.fixture
def app():
    """Create a test instance of PomodoroTimer"""
    app = main.PomodoroTimer(testing_mode=True)
    # Create mocks for UI components
    app.window = MagicMock()
    app.canvas = MagicMock()
    app.text_label = MagicMock()
    app.check_marks = MagicMock()
    app.start_button = MagicMock()
    app.stop_button = MagicMock()
    app.timer_text = 1
    yield app
    # Reset global variables after each test
    app.reset_timer()

def test_initial_state(app):
    """Test initial state of the application"""
    assert main.reps == 0
    assert main.work_sessions == 0
    assert main.is_paused is False
    assert main.remaining_time == 0
    assert main.current_mode == ""

def test_reset_timer(app):
    """Test reset functionality"""
    # Setup initial state
    main.reps = 5
    main.work_sessions = 3
    main.is_paused = True
    main.remaining_time = 100
    main.current_mode = "work"
    main.timer = app.window.after(1000, lambda: None)
    
    # Call reset_timer
    app.reset_timer()
    
    # Verify global state
    assert main.reps == 0, f"Expected reps to be 0, but got {main.reps}"
    assert main.work_sessions == 0, f"Expected work_sessions to be 0, but got {main.work_sessions}"
    assert main.is_paused is False, f"Expected is_paused to be False, but got {main.is_paused}"
    assert main.remaining_time == 0, f"Expected remaining_time to be 0, but got {main.remaining_time}"
    assert main.current_mode == "", f"Expected current_mode to be empty, but got {main.current_mode}"
    
    # Verify UI updates
    app.canvas.itemconfig.assert_called_once_with(1, text="00:00")
    app.text_label.config.assert_called_once_with(text="Timer", fg=main.GREEN)
    app.check_marks.config.assert_called_once_with(text="")
    app.start_button.config.assert_called_once_with(state=NORMAL)
    app.stop_button.config.assert_called_once_with(state=DISABLED)

def test_start_timer_work_session(app):
    """Test starting a work session"""
    # Setup initial state
    main.reps = 0
    main.work_sessions = 0
    main.current_mode = ""
    main.is_paused = False
    
    app.start_timer()
    
    assert main.current_mode == "work"
    assert main.work_sessions == 1
    assert main.reps == 1
    app.start_button.config.assert_called_once_with(state=DISABLED)
    app.stop_button.config.assert_called_once_with(state=NORMAL)
    app.text_label.config.assert_called_with(text="Work", fg=main.GREEN)

def test_start_timer_short_break(app):
    """Test starting a short break"""
    # Setup initial state
    main.reps = 1
    main.current_mode = "work"
    main.is_paused = False
    
    app.start_timer()
    
    assert main.current_mode == "short_break"
    assert main.reps == 2
    app.text_label.config.assert_called_with(text="Break", fg=main.PINK)

def test_start_timer_long_break(app):
    """Test starting a long break"""
    # Setup initial state
    main.reps = 7
    main.current_mode = "work"
    main.is_paused = False
    
    app.start_timer()
    
    assert main.current_mode == "long_break"
    assert main.reps == 8
    app.text_label.config.assert_called_with(text="Break", fg=main.RED)

def test_stop_timer(app):
    """Test stop timer functionality"""
    # Setup initial state
    main.is_paused = False
    main.timer = app.window.after(1000, lambda: None)
    
    app.stop_timer()
    
    assert main.is_paused is True
    app.start_button.config.assert_called_once_with(state=NORMAL)
    app.stop_button.config.assert_called_once_with(state=DISABLED)

def test_count_down(app):
    """Test countdown functionality"""
    # Setup initial state
    main.timer = None
    main.remaining_time = 0
    
    app.count_down(60)  # 1 minute
    
    assert main.remaining_time == 60
    app.canvas.itemconfig.assert_called_once_with(1, text="01:00")
    assert app.window.after.called

def test_update_checkmarks(app):
    """Test checkmark updates"""
    # Setup initial state
    main.work_sessions = 3
    
    app.update_checkmarks()
    
    app.check_marks.config.assert_called_once_with(text="✔✔✔")

def test_start_timer_resume_from_pause(app):
    """Test resuming timer from paused state"""
    # Setup initial state
    main.is_paused = True
    main.current_mode = "work"
    main.remaining_time = 1500  # 25 minutes
    
    app.start_timer()
    
    assert not main.is_paused
    app.text_label.config.assert_any_call(text="Restarted", fg=main.GREEN)
    app.start_button.config.assert_called_with(state=DISABLED)
    app.stop_button.config.assert_called_with(state=NORMAL)

if __name__ == "__main__":
    pytest.main(["-v"])
