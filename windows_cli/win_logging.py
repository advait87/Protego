import os
import datetime
import logging
from typing import Optional

class Logging:
    def __init__(self, log_dir: Optional[str] = None):
        """Initialize the logging system for Protego.
        
        Args:
            log_dir (str, optional): Directory to store log files. Defaults to 'logs' in current directory.
        """
        # Set up log directory
        self.log_dir = log_dir or os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(self.log_dir, exist_ok=True)

        # Use a single log file
        self.log_file = os.path.join(self.log_dir, 'protego.log')

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, mode='a'),  # 'a' for append mode
                logging.StreamHandler()  # Also print to console
            ]
        )
        self.logger = logging.getLogger('Protego')
        
        # Log application startup
        separator = '-' * 50
        self.logger.info(f"\n{separator}")
        self.logger.info("Protego Application Started")

    def log_action(self, action: str, status: bool, details: Optional[str] = None):
        """Log an action with its status and optional details.
        
        Args:
            action (str): The action being performed
            status (bool): True if successful, False if failed
            details (str, optional): Additional details about the action
        """
        status_str = "SUCCESS" if status else "FAILED"
        message = f"{action}: {status_str}"
        if details:
            message += f" - {details}"

        if status:
            self.logger.info(message)
        else:
            self.logger.error(message)

    def log_check(self, parameter: str, current_value: str, target_value: str, compliant: bool):
        """Log a compliance check result.
        
        Args:
            parameter (str): The parameter being checked
            current_value (str): Current value of the parameter
            target_value (str): Target value for the parameter
            compliant (bool): Whether the current value is compliant
        """
        status = "COMPLIANT" if compliant else "NON-COMPLIANT"
        message = f"Check {parameter}: {status} (Current: {current_value}, Target: {target_value})"
        if compliant:
            self.logger.info(message)
        else:
            self.logger.warning(message)

    def log_backup(self, backup_path: str, success: bool):
        """Log backup operation status.
        
        Args:
            backup_path (str): Path where backup is stored
            success (bool): Whether backup was successful
        """
        if success:
            self.logger.info(f"System state backup created successfully at: {backup_path}")
        else:
            self.logger.error(f"Failed to create system state backup at: {backup_path}")

    def log_rollback(self, backup_path: str, success: bool):
        """Log rollback operation status.
        
        Args:
            backup_path (str): Path of backup being restored
            success (bool): Whether rollback was successful
        """
        if success:
            self.logger.info(f"System state restored successfully from: {backup_path}")
        else:
            self.logger.error(f"Failed to restore system state from: {backup_path}")

    def log_error(self, error_message: str, exception: Optional[Exception] = None):
        """Log an error with optional exception details.
        
        Args:
            error_message (str): Description of the error
            exception (Exception, optional): The exception that was caught
        """
        if exception:
            self.logger.error(f"{error_message}: {str(exception)}")
        else:
            self.logger.error(error_message)
            
    def log_shutdown(self):
        """Log application shutdown."""
        separator = '-' * 50
        self.logger.info("Protego Application Shutting Down")
        self.logger.info(f"{separator}\n")