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

# def max_rainfall()

def rainiest_cloudy(forecasts: list[Forecast]) -> bool:
    reports = forecasts_to_reports(forecasts)