from lead import de_school_lead_samples
from dataclasses import dataclass
from bakery import assert_equal
# ppb = parts per billion; unit to measure lead concentration in water

SAMPLE1 = '0002ppb| Appoquinimink|               Alfred G Waters Middle School|Kitchen Faucet'
SAMPLE2 = '0003ppb|    Woodbridge|                    Woodbridge Middle School|Water Fountain'
SAMPLE3 = '0002ppb|    Brandywine|                      Brandywine High School|Second Floor Right Water Fountain w/Cooler in Hallway by Room 213'
SAMPLE4 = "0002ppb| Appoquinimink|               Alfred G Waters Middle School|Water Fountain w/Cooler by Room E119"
SAMPLE5 = "0002ppb| Appoquinimink|               Alfred G Waters Middle School|Water Fountain w/Cooler by Room F119"
SAMPLE6 = "0003ppb| Appoquinimink|                   Appoquinimink High School|Kitchen Faucet"
SAMPLE7 = "0002ppb|    Brandywine|                         Concord High School|Basement Bottle Filler by Room T100"

SAMPLES = [SAMPLE1, SAMPLE2, SAMPLE3, SAMPLE4, SAMPLE5, SAMPLE6, SAMPLE7]

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
assert_equal(convert_line(SAMPLE2), Sample(3, "Woodbridge", "Woodbridge Middle School", "Water Fountain"))
assert_equal(convert_line(SAMPLE3), Sample(2, "Brandywine", "Brandywine High School", "Second Floor Right Water Fountain w/Cooler in Hallway by Room 213"))

def convert_lines(lines: list[str]) -> list[Sample]:
    result = []
    for line in lines:
        result.append(convert_line(line))
    return result

def count_samples(samples: list[Sample]) -> int:
    return len(samples)

assert_equal(count_samples(convert_lines(SAMPLES)), 7)
assert_equal(count_samples([convert_line(SAMPLE1), convert_line(SAMPLE2)]), 2)
assert_equal(count_samples([convert_line(SAMPLE3), convert_line(SAMPLE1), convert_line(SAMPLE2)]), 3)

def total_lead(samples: list[Sample]) -> int:
    total = 0
    for sample in samples:
        total += sample.lead_level
    return total

assert_equal(total_lead([convert_line(SAMPLE1), convert_line(SAMPLE2)]), 5)
assert_equal(total_lead([convert_line(SAMPLE3), convert_line(SAMPLE1), convert_line(SAMPLE2)]), 7)
assert_equal(total_lead([convert_line(SAMPLE1)]), 2)

def average_lead(samples: list[Sample]) -> float:
    if not samples:
        return 0.0
    return total_lead(samples) / len(samples)

assert_equal(average_lead([convert_line(SAMPLE1), convert_line(SAMPLE2)]), 2.5)
assert_equal(average_lead([convert_line(SAMPLE3), convert_line(SAMPLE1), convert_line(SAMPLE2)]), 7/3)
assert_equal(average_lead([convert_line(SAMPLE1)]), 2.0)

def average_lead_per_district(samples: list[Sample], district: str) -> float:
    filtered = [sample for sample in samples if sample.district == district]
    if not filtered:
        return 0.0
    return average_lead(filtered)

assert_equal(average_lead_per_district([convert_line(SAMPLE1), convert_line(SAMPLE2)], "Appoquinimink"), 2.0)
assert_equal(average_lead_per_district([convert_line(SAMPLE1), convert_line(SAMPLE2)], "Woodbridge"), 3.0)
assert_equal(average_lead_per_district([convert_line(SAMPLE1), convert_line(SAMPLE3)], "Brandywine"), 2.0)

# additional questions

def average_lead_per_school(samples: list[Sample], school: str) -> float:
    filtered = [sample for sample in samples if sample.school == school]
    if not filtered:
        return 0.0
    return average_lead(filtered)

assert_equal(average_lead_per_school(convert_lines(SAMPLES), "Alfred G Waters Middle School"), 2.0)
assert_equal(average_lead_per_school(convert_lines(SAMPLES), "Appoquinimink High School"), 3.0)

def total_in_district(samples: list[Sample], district: str) -> int:
    return total_lead(sample for sample in samples if sample.district == district)

assert_equal(total_in_district(convert_lines(SAMPLES), "Appoquinimink"), 9)
assert_equal(total_in_district(convert_lines(SAMPLES), "Brandywine"), 4)