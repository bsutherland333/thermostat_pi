from datetime import datetime
import yaml


class Schedule:
    def __init__(self, schedule_filepath: str):
        self._schedule_filepath = schedule_filepath

    def get_setpoint(self) -> tuple[float, float, str]:
        # Open the schedule file
        with open(self._schedule_filepath, "r") as file:
            schedule = yaml.safe_load(file)
        self._check_schedule_valid(schedule)

        # Get the curren time of day, formatted as hhmm
        curr_time = int(datetime.now().strftime("%H%M"))

        # Iterate through the schedule and find the current and previous entry,
        # wrapping if necessary
        entries = list(schedule.keys())
        prev_entry = entries[-2] if len(entries) > 1 else None
        curr_entry = entries[-1]
        for i in reversed(range(len(entries))):
            if curr_time >= entries[i]:
                prev_entry = entries[i - 1] if len(entries) > 1 else None
                curr_entry = entries[i]
                break

        # Wrap the current time if necessary
        if curr_entry > curr_time:
            curr_time += 2400

        # Get the setpoint for the current entry, interpolating if necessary
        curr_time_in_minutes = (curr_time // 100) * 60 + curr_time % 100
        curr_entry_in_minutes = (curr_entry // 100) * 60 + curr_entry % 100
        delta_time = curr_time_in_minutes - curr_entry_in_minutes
        if (
            prev_entry is not None
            and "transition_period" in schedule[curr_entry]
            and delta_time < schedule[curr_entry]["transition_period"]
        ):
            setpoint = (
                schedule[prev_entry]["setpoint"]
                + (schedule[curr_entry]["setpoint"] - schedule[prev_entry]["setpoint"])
                * delta_time
                / schedule[curr_entry]["transition_period"]
            )
        else:  # No interpolation needed
            setpoint = schedule[curr_entry]["setpoint"]

        # Get final values to return
        min = setpoint - schedule[curr_entry]["tolerance"]
        max = setpoint + schedule[curr_entry]["tolerance"]
        mode = (
            schedule[curr_entry]["mode"] if "mode" in schedule[curr_entry] else "auto"
        )

        return min, max, mode

    def _check_schedule_valid(self, schedule: dict):
        # Check that the schedule has entries
        if not schedule:
            raise ValueError("Schedule is empty")

        for key, value in schedule.items():
            # Check that each key is a valid integer time
            if not isinstance(key, int) or not 0 <= key <= 2400:
                raise ValueError(f"Entry {key} is not a valid time")
            # Check that the minutes are valid
            if key % 100 >= 60:
                raise ValueError(f"Entry {key} has invalid minutes")
            # Check that there is not a 0000 and 2400
            if 0 in schedule and 2400 in schedule:
                raise ValueError("Cannot have both 0000 and 2400 entries")
            # Check that each entry is a dictionary
            if not isinstance(value, dict):
                raise ValueError(f"Entry {key} is not a dictionary")
            # Check that each entry has the 'setpoint' key
            if "setpoint" not in value:
                raise ValueError(f"Entry {key} is missing 'setpoint'")
            # Check that the setpoint is a float
            if not isinstance(value["setpoint"], float):
                raise ValueError(f"Entry {key} 'setpoint' is not a float")
            # Check that each entry has the 'tolerance' key
            if "tolerance" not in value:
                raise ValueError(f"Entry {key} is missing 'tolerance'")
            # Check that the tolerance is a positive float
            if not isinstance(value["tolerance"], float) or value["tolerance"] < 0:
                raise ValueError(f"Entry {key} 'tolerance' is not a positive float")
            # Check that transition_period is a positive integer, if it exists
            if "transition_period" in value:
                if (
                    not isinstance(value["transition_period"], int)
                    or value["transition_period"] < 0
                ):
                    raise ValueError(
                        f"Entry {key} 'transition_period' is not a positive integer"
                    )
            # Check that mode is 'auto', 'cool', or 'heat' if it exists
            if "mode" in value:
                if value["mode"] not in ["auto", "cool", "heat"]:
                    raise ValueError(
                        f"Entry {key} 'mode' is not 'auto', 'cool', or 'heat'"
                    )

        # Check that the schedule is in chronological order
        if list(schedule.keys()) != sorted(schedule.keys()):
            raise ValueError("Schedule is not in chronological order")
