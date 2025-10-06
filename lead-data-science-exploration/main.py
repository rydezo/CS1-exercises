from lead import de_school_lead_samples
from dataclasses import dataclass
from bakery import assert_equal

SAMPLE1 = '0002ppb| Appoquinimink|               Alfred G Waters Middle School|Kitchen Faucet'
SAMPLE2 = '0003ppb|    Woodbridge|                    Woodbridge Middle School|Water Fountain'
SAMPLE3 = '0002ppb|    Brandywine|                      Brandywine High School|Second Floor Right Water Fountain w/Cooler in Hallway by Room 213'

SAMPLES = [SAMPLE1, SAMPLE2, SAMPLE3]

@dataclass(frozen=True)
class Sample:
    lead_level: int # ppb
    district: str
    school: str
    location: str

def convert_line(line: str) -> Sample:
    return Sample(
        lead_level=int(line[:4]),
        district=line[8:22].strip(),
        school=line[23:67].strip(),
        location=line[68:].strip(),
    )

assert_equal(convert_line(SAMPLE1), Sample(2, "Appoquinimink", "Alfred G Waters Middle School", "Kitchen Faucet"))

def convert_lines(lines: list[str]) -> list[Sample]:
    result = []
    for line in lines:
        result.append(convert_line(line))
    return result

def total_lead(samples: list[Sample]) -> int:
    total = 0
    for sample in samples:
        total += sample.lead_level
    return total

def average_lead(samples: list[Sample]) -> float:
    if not samples:
        return 0.0
    return total_lead(samples) / len(samples)

def average_lead_per_district(samples: list[Sample], district: str) -> float:
    if not samples:
        return 0.0
    return average_lead(sample for sample in samples if sample.district == district)