from faker import Faker
import uuid
import string

fake = Faker()

def faker_customer():
    import random
    LOCATIONS = [
    ("Tokyo",         "Tokyo",           "Japan",                "Asia Pacific"),
    ("London",        "England",         "United Kingdom",       "Europe"),
    ("New York City", "New York",        "United States",        "North America"),
    ("Paris",         "Île-de-France",   "France",               "Europe"),
    ("Mumbai",        "Maharashtra",     "India",                "Asia Pacific"),
    ("Sydney",        "New South Wales", "Australia",            "Asia Pacific"),
    ("Cairo",         "Cairo",           "Egypt",                "Middle East & Africa"),
    ("São Paulo",     "São Paulo",       "Brazil",               "Latin America"),
    ("Toronto",       "Ontario",         "Canada",               "North America"),
    ("Singapore",     "Singapore",       "Singapore",            "Asia Pacific"),
    ("Rome",          "Lazio",           "Italy",                "Europe"),
    ("Los Angeles",   "California",      "United States",        "North America"),
    ("Berlin",        "Berlin",          "Germany",              "Europe"),
    ("Seoul",         "Seoul",           "South Korea",          "Asia Pacific"),
    ("Bangkok",       "Bangkok",         "Thailand",             "Asia Pacific"),
    ("Mexico City",   "Mexico City",     "Mexico",               "Latin America"),
    ("Buenos Aires",  "Buenos Aires",    "Argentina",            "Latin America"),
    ("Amsterdam",     "Noord-Holland",   "Netherlands",          "Europe"),
    ("Cape Town",     "Western Cape",    "South Africa",         "Middle East & Africa"),
]
    customer_segments = ["Economy / Budget","Standard / Core","Premium / Pro","Enterprise / VIP / Elite","Freemium / Trialist"]
    event = ["Dedit","credit"]

    customer = {
    "event_id" : str(uuid.uuid4()),
    "customer_id" : str(uuid.uuid4()),
    "first_name" : fake.name(),
    "last_name": fake.name(),
    "email": fake.email(),
    "phone_number": fake.phone_number(),
    "city": random.choice([location[0] for location in LOCATIONS]),
    "state": random.choice([location[1] for location in LOCATIONS]),
    "country": random.choice([location[2] for location in LOCATIONS]),
    "customer_segment": random.choice(customer_segments),
    "event_type": random.choice(event),
    "event_timestamp": fake.date_time_this_year(),
    "ingested_at": fake.date_time_this_year()
    }

    return customer
