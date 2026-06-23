from pathlib import Path

from pytest_bdd import scenarios

scenarios(str(Path(__file__).parent.parent.parent / "features" / "02_first_service.feature"))
