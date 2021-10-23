import sys

import pkg_resources
from pathlib import Path

from mylogger import logger
class TestRequirements:
    """Test availability of required packages."""

    def __init__(self, requirement_path):
        self.requirement_path = Path(requirement_path)

    def test_requirements(self):
        """Test that each required package is available."""
        # Ref: https://stackoverflow.com/a/45474387/
        requirements = pkg_resources.parse_requirements(self.requirement_path.open())
        missing_requirement = False
        for requirement in requirements:
            requirement = str(requirement)
            try:
                pkg_resources.require(requirement)
            except pkg_resources.VersionConflict:
                logger.error("You need to install or update some dependencies: pip install -U %s", requirement)
                missing_requirement=True
        if missing_requirement:
            sys.exit(10)