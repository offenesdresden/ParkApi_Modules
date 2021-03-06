import feedparser
from park_api.geodata import GeoData


# Falls das hier jemals einer von den Menschen
# hinter OpenDataZürich lesen sollte: Ihr seid so toll <3
geodata = GeoData(__file__)


def parse_html(xml_data):
    feed = feedparser.parse(xml_data)

    last_updated = feed["entries"][0]["updated"]
    data = {
        "lots": [],
        # remove trailing timezone for consensistency
        "last_updated": last_updated.replace("Z", "")
    }

    for entry in feed["entries"]:
        summary = parse_summary(entry["summary"])
        title_elements = parse_title(entry["title"])

        lot_identifier = (title_elements[2] + " " + title_elements[0]).strip()
        lot = geodata.lot(lot_identifier)

        data["lots"].append({
            "name": title_elements[0],
            "address": title_elements[1],
            "id": lot.id,
            "state": summary[0],
            "free": summary[1],
            "total": lot.total,
            "coords": lot.coords,
            "forecast": False,
            "lot_type": title_elements[2]
        })

    return data


def parse_summary(summary):
    """Parse a string from the format 'open /   41' into both its params"""
    summary = summary.split("/")

    summary[0] = summary[0].strip()
    if "?" in summary[0]:
        summary[0] = "nodata"

    try:
        summary[1] = int(summary[1])
    except ValueError:
        summary[1] = 0
    return summary


def parse_title(title):
    """
    Parse a string from the format 'Parkgarage am Central / Seilergraben'
    into both its params
    """
    types = ["Parkhaus", "Parkplatz"]

    name = title.split(" / ")[0]
    address = title.split(" / ")[1]
    type = ""
    if name.split(" ")[0] in types:
        type = name.split(" ")[0]
        name = " ".join(name.split(" ")[1:])

    return name, address, type
