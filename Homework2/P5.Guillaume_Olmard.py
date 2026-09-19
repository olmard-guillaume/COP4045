"""Weather station observation analyzer."""

import csv
import math
import sys
from datetime import datetime


DATE_FORMAT = "%I:%M:%S %p %m/%d/%Y"
MIN_TEMPERATURE = -100.0
MAX_TEMPERATURE = 150.0


def _parse_date(date_text: str) -> datetime:
	"""Convert an observation date to a datetime object."""
	return datetime.strptime(date_text.strip(), DATE_FORMAT)


def read_observations(filename):
	"""Read observations and return ``(observations, errors)``."""
	observations = {}
	errors = []
	seen = set()

	with open(filename, "r", newline="", encoding="utf-8") as file_object:
		reader = csv.reader(file_object)

		for line_number, row in enumerate(reader, start=1):
			if len(row) != 3:
				errors.append((line_number, "malformed observation"))
				continue

			station = row[0].strip()
			date_text = row[1].strip()
			temperature_text = row[2].strip()

			if not station or not date_text or not temperature_text:
				errors.append((line_number, "malformed observation"))
				continue

			try:
				date = _parse_date(date_text)
			except ValueError:
				errors.append((line_number, "invalid date"))
				continue

			try:
				temperature = float(temperature_text)
			except ValueError:
				errors.append((line_number, "invalid temperature"))
				continue

			if (not math.isfinite(temperature)
					or not MIN_TEMPERATURE <= temperature <= MAX_TEMPERATURE):
				errors.append((line_number, "temperature out of range"))
				continue

			observation_key = (station, date)
			if observation_key in seen:
				errors.append((line_number, "duplicate station/date"))
				continue

			seen.add(observation_key)
			observations.setdefault(station, []).append((date, temperature))

	for station in observations:
		observations[station].sort(key=lambda observation: observation[0])

	return observations, errors


def station_statistics(observations):
	"""Return minimum, maximum, and mean temperature for each station."""
	return {
		station: (
			min(temperature for _, temperature in station_observations),
			max(temperature for _, temperature in station_observations),
			sum(temperature for _, temperature in station_observations)
			/ len(station_observations),
		)
		for station, station_observations in observations.items()
	}


def station_outliers(observations):
	"""Return stations whose latest temperature exceeds their mean."""
	statistics = station_statistics(observations)
	return {
		station: (latest_date, latest_temperature, statistics[station][2])
		for station, station_observations in observations.items()
		for latest_date, latest_temperature in [station_observations[-1]]
		if latest_temperature > statistics[station][2]
	}


def write_statistics(filename, statistics):
	"""Write station statistics as sorted, comma-separated rows."""
	with open(filename, "w", newline="", encoding="utf-8") as file_object:
		writer = csv.writer(file_object, lineterminator="\n")
		for station in sorted(statistics):
			minimum, maximum, mean = statistics[station]
			writer.writerow(
				[station, f"{minimum:.1f}", f"{maximum:.1f}", f"{mean:.1f}"]
			)


def _print_statistics(statistics):
	"""Print station statistics in lexicographic order."""
	for station in sorted(statistics):
		minimum, maximum, mean = statistics[station]
		print(
			f"{station}: min={minimum:.1f}, "
			f"max={maximum:.1f}, mean={mean:.1f}"
		)


def main():
	"""Read the command-line input file and write its statistics."""
	if len(sys.argv) != 3:
		print("Usage: P5.Guillaume_Olmard.py input_file output_file")
		return

	try:
		observations, errors = read_observations(sys.argv[1])
		statistics = station_statistics(observations)

		_print_statistics(statistics)
		print("Outliers:")
		outliers = station_outliers(observations)
		for station in sorted(outliers):
			date, temperature, mean = outliers[station]
			print(f"{station}: {date.strftime(DATE_FORMAT)}, "
				  f"temperature={temperature:.1f}, mean={mean:.1f}")

		if errors:
			print("Errors:")
			for line_number, message in errors:
				print(f"line {line_number}: {message}")

		write_statistics(sys.argv[2], statistics)
	except OSError as error:
		print(f"File access error: {error}")
	except (csv.Error, ValueError) as error:
		print(f"Unable to process observations: {error}")


if __name__ == "__main__":
	main()
