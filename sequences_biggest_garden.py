from bakery import assert_equal

def take_until_trees(beds: list[str]) -> list[str]:
    taking = True
    result = []
    for bed in beds:
        if '🌳' in bed:
            taking = False
        elif taking:
            result.append(bed)
    return result

assert_equal(take_until_trees(["🌹🌹","🌷🌷","🌻🌻🌻"]), ["🌹🌹","🌷🌷","🌻🌻🌻"])
assert_equal(take_until_trees(["🌹🌹","🌷🌷","🌳", "🌻🌻🌻"]), ["🌹🌹","🌷🌷"])
assert_equal(take_until_trees(["🌳","🌸","🌺🌺🌺🌺"]), [])
assert_equal(take_until_trees([]), [])
assert_equal(take_until_trees(["🌳🌳🌳"]), [])

def remove_seedlings(beds: list[str]) -> list[str]:
    result = []
    for bed in beds:
        if '🌱' not in bed:
            result.append(bed)
    return result

assert_equal(remove_seedlings(["🌹", "🌱🌱", "🌷","🌼🌼","🌱🌱🌱","🌳","🌻🌻🌻"]), ["🌹", "🌷","🌼🌼","🌳","🌻🌻🌻"])
assert_equal(remove_seedlings(["🌱🌱,🌱🌱🌱","🌳","🌸","🌺🌺🌺🌺"]), ["🌳","🌸","🌺🌺🌺🌺"])
assert_equal(remove_seedlings([]), [])
assert_equal(remove_seedlings(["🌱🌱"]), [])

def max_bed(beds: list[str]) -> str:
    most_popular = beds[0]
    for bed in beds:
        if len(bed) > len(most_popular):
            most_popular = bed
    return most_popular

assert_equal(max_bed(["🌹🌹","🌷🌷","🌻🌻🌻","🌸"]), "🌻🌻🌻")
assert_equal(max_bed(["🌹🌹","🌷🌷","🌼🌼🌼","🌸","🌺🌺🌺🌺","🌻🌻🌻"]), "🌺🌺🌺🌺")
assert_equal(max_bed(["🌹🌹","🌷🌷","🌼🌼🌼","🌱🌱🌱🌱🌱","🌳","🌸","🌺🌺🌺🌺","🌻🌻🌻"]), "🌱🌱🌱🌱🌱")
assert_equal(max_bed(["🌺🌺🌺🌺", "🌱🌱","🌱🌱🌱","🌳","🌸"]), "🌺🌺🌺🌺")
assert_equal(max_bed(["🌱🌱"]), "🌱🌱")

def biggest_bed(garden: str) -> str:
    if not garden:
        return "no flowers"
    flower_beds = garden.split(',')
    flower_beds = take_until_trees(flower_beds)
    flower_beds = remove_seedlings(flower_beds)
    if not flower_beds:
        return 'no flowers'
    return max_bed(flower_beds)

assert_equal(biggest_bed("🌹🌹,🌷🌷,🌻🌻🌻,🌸"), "🌻🌻🌻")
assert_equal(biggest_bed("🌹🌹,🌷🌷,🌼🌼🌼,🌸,🌺🌺🌺🌺,🌻🌻🌻"), "🌺🌺🌺🌺")
assert_equal(biggest_bed("🌹🌹,🌷🌷,🌼🌼🌼,🌱🌱🌱🌱🌱,🌳,🌸,🌺🌺🌺🌺,🌻🌻🌻"), "🌼🌼🌼")
assert_equal(biggest_bed("🌹🌹,🌷🌷,🌼🌼🌼,🌳,🌸,🌺🌺🌺🌺,🌻🌻🌻"), "🌼🌼🌼")
assert_equal(biggest_bed("🌹🌹,🌷🌷,🌼🌼🌼,🌱🌱🌱🌱🌱,🌸,🌺🌺🌺🌺,🌻🌻🌻"), "🌺🌺🌺🌺")
assert_equal(biggest_bed("🌱🌱,🌱🌱🌱,🌳,🌸,🌺🌺🌺🌺"), "no flowers")
assert_equal(biggest_bed("🌳,🌸,🌺🌺🌺🌺"), "no flowers")
assert_equal(biggest_bed(""), "no flowers")
assert_equal(biggest_bed("🌳🌳🌳"), "no flowers")
assert_equal(biggest_bed("🌱🌱"), "no flowers")