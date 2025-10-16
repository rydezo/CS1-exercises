from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Measurement:
    amount: int
    automatic: bool
    
@dataclass
class WeatherOptions:
    raining: bool
    cloudy: bool
    snowing: bool

@dataclass
class Report:
    temperature: int
    rainfall: list[Measurement]
    weather: WeatherOptions
    
@dataclass
class Forecast:
    when: str
    where: str
    reports: list[Report]
    
def forecasts_to_reports(forecasts: list[Forecast]) -> list[Report]:
    reports: list[Report] = []
    for forecast in forecasts:
        for report in forecast.reports:
            reports.append(report)
    return reports

def rainiest_cloudy(forecasts: list[Forecast]) -> bool:
    reports = forecasts_to_reports(forecasts)
    if not reports:
        return False

    day_most_rainfall: Report = reports[0]
    max_rainfall: int = day_most_rainfall.rainfall[0].amount

    for report in reports:
        report_total = 0
        for rain in report.rainfall:
            report_total += rain.amount
        if report_total > max_rainfall:
            max_rainfall = report_total
            day_most_rainfall = report
    
    return day_most_rainfall.weather.cloudy

rainfall1 = [Measurement(2, True), Measurement(5, False)]
rainfall2 = [Measurement(8, True), Measurement(6, False)]
report1 = Report(32, rainfall1, WeatherOptions(True, False, True))
report2 = Report(44, rainfall2, WeatherOptions(True, True, True))
report3 = Report(50, rainfall1, WeatherOptions(True, True, True))
forecasts1 = [Forecast("w","w", [report1, report2]), Forecast("h","h", [report2, report1])]
forecasts2 = [Forecast("h","h", [report3, report2]), Forecast("w","w", [report2, report2])]
forecasts3 = [Forecast("h","h", []), Forecast("w","w", [])]

assert_equal(rainiest_cloudy(forecasts1), True)
assert_equal(rainiest_cloudy(forecasts2), True)
assert_equal(rainiest_cloudy(forecasts3), False)