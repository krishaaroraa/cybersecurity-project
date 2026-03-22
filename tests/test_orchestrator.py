import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add agents/ directory to path so we can import orchestrator_agent
agents_dir = Path(__file__).resolve().parent.parent / "agents"
sys.path.append(str(agents_dir))

import orchestrator_agent

class TestOrchestrator(unittest.TestCase):

    @patch("subprocess.run")
    @patch("builtins.print")
    @patch("pathlib.Path.exists")
    def test_run_agent_success(self, mock_exists, mock_print, mock_run):
        # Setup mock to return success
        mock_exists.return_value = True
        mock_run.return_value.returncode = 0
        
        # Test success case
        code, duration = orchestrator_agent.run_agent("test_agent.py")
        
        self.assertEqual(code, 0)
        self.assertGreaterEqual(duration, 0)
        mock_run.assert_called_once()
        # The print message now includes duration
        last_print = mock_print.call_args_list[-1][0][0]
        self.assertIn("=== Finished test_agent.py", last_print)
        self.assertIn("with code 0 ===", last_print)

    @patch("subprocess.run")
    @patch("builtins.print")
    @patch("pathlib.Path.exists")
    def test_run_agent_failure(self, mock_exists, mock_print, mock_run):
        # Setup mock to return failure
        mock_exists.return_value = True
        mock_run.return_value.returncode = 1
        
        # Test failure case
        code, duration = orchestrator_agent.run_agent("test_agent.py")
        
        self.assertEqual(code, 1)
        self.assertGreaterEqual(duration, 0)
        mock_run.assert_called_once()
        last_print = mock_print.call_args_list[-1][0][0]
        self.assertIn("=== Finished test_agent.py", last_print)
        self.assertIn("with code 1 ===", last_print)

    @patch("orchestrator_agent.run_agent")
    @patch("builtins.print")
    @patch("sys.exit")
    def test_main_all_success(self, mock_exit, mock_print, mock_run_agent):
        # Mock run_agent to always return success (0, duration)
        mock_run_agent.return_value = (0, 0.5)
        
        # Call main
        orchestrator_agent.main()
        
        # Check that sys.exit was NOT called for failure
        mock_exit.assert_not_called()
        
        # Verify summary was printed (checking for table headers)
        any_summary = any("Agent" in str(call[0][0]) and "Status" in str(call[0][0]) for call in mock_print.call_args_list)
        self.assertTrue(any_summary)

    @patch("orchestrator_agent.run_agent")
    @patch("builtins.print")
    @patch("sys.exit")
    def test_main_with_failure(self, mock_exit, mock_print, mock_run_agent):
        # Mock run_agent to return failure (1, duration) for one of the agents
        # We now have 5 agents in the list
        mock_run_agent.side_effect = [
            (0, 0.1), (0, 0.1), (1, 0.1), (0, 0.1), (0, 0.1)
        ] # Third agent fails
        
        # Call main
        orchestrator_agent.main()
        
        # Verify sys.exit(1) was called for flow failure
        mock_exit.assert_called_once_with(1)
        
        # Verify failure is in the summary
        any_failed = any("FAILED" in str(call[0][0]) for call in mock_print.call_args_list)
        self.assertTrue(any_failed)

if __name__ == "__main__":
    unittest.main()
