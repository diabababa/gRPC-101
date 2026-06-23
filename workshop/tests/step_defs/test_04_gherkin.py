"""Exercise 04 — loads the participant's feature file from exercises/04_gherkin/."""
from pathlib import Path

from pytest_bdd import scenarios

scenarios(
    str(
        Path(__file__).parent.parent.parent
        / "exercises"
        / "04_gherkin"
        / "chat_starter.feature"
    )
)
