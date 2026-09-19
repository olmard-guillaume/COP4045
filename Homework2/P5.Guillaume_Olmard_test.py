"""Unit tests for the weather station analyzer."""

import importlib.util
import tempfile
import unittest
from datetime import datetime
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("P5.Guillaume_Olmard.py")
SPEC = importlib.util.spec_from_file_location("weather_analyzer", MODULE_PATH)
weather_analyzer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(weather_analyzer)


class WeatherStationTests(unittest.TestCase):
    """Test observation parsing and reporting."""

    def make_input(self, content):
        file_object = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", delete=False
        )
        file_object.write(content)
        file_object.close()
        self.addCleanup(Path(file_object.name).unlink, missing_ok=True)
        return file_object.name

    def test_several_stations_and_negative_temperatures(self):
        filename = self.make_input(
            "North,09:28:09 AM 04/20/2026,-4.5\n"
            "South,09:28:09 AM 04/20/2026,12.0\n"
        )
        observations, errors = weather_analyzer.read_observations(filename)
        self.assertEqual(errors, [])
        self.assertEqual(observations["North"][0][1], -4.5)
        self.assertIn("South", observations)

    def test_duplicate_observation_is_rejected(self):
        filename = self.make_input(
            "North,09:28:09 AM 04/20/2026,4.5\n"
            "North,09:28:09 AM 04/20/2026,5.5\n"
        )
        observations, errors = weather_analyzer.read_observations(filename)
        self.assertEqual(len(observations["North"]), 1)
        self.assertEqual(errors[0][0], 2)

    def test_invalid_temperature_range_is_rejected(self):
        filename = self.make_input(
            "North,09:28:09 AM 04/20/2026,150.1\n"
            "South,09:28:09 AM 04/20/2026,-100.1\n"
        )
        observations, errors = weather_analyzer.read_observations(filename)
        self.assertEqual(observations, {})
        self.assertEqual(len(errors), 2)

    def test_statistics_are_calculated(self):
        observations = {
            "North": [
                (datetime(2026, 4, 20, 9, 28, 9), -4.0),
                (datetime(2026, 4, 21, 9, 28, 9), 8.0),
            ]
        }
        self.assertEqual(
            weather_analyzer.station_statistics(observations)["North"],
            (-4.0, 8.0, 2.0),
        )

    def test_observations_and_output_are_sorted(self):
        filename = self.make_input(
            "South,09:28:09 AM 04/21/2026,5.0\n"
            "North,09:28:09 AM 04/20/2026,1.0\n"
            "South,09:28:09 AM 04/20/2026,3.0\n"
        )
        observations, _ = weather_analyzer.read_observations(filename)
        self.assertLess(observations["South"][0][0], observations["South"][1][0])

        output = tempfile.NamedTemporaryFile(delete=False)
        output.close()
        self.addCleanup(Path(output.name).unlink, missing_ok=True)
        weather_analyzer.write_statistics(
            output.name,
            {"South": (3.0, 5.0, 4.0), "North": (1.0, 1.0, 1.0)},
        )
        self.assertEqual(
            Path(output.name).read_text(encoding="utf-8").splitlines(),
            ["North,1.0,1.0,1.0", "South,3.0,5.0,4.0"],
        )

    def test_missing_file_raises_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            weather_analyzer.read_observations("missing-observations.csv")


if __name__ == "__main__":
    unittest.main()