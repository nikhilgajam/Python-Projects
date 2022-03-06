import urllib.request as url_req
import webbrowser
import json


def data():
    # Printing data about ISS
    about_iss = "The International Space Station(ISS) is a modular space station in low Earth orbit. It is a " \
                "multinational collaborative project involving five participating space agencies: NASA, Roscosmos, " \
                "JAXA, ESA, and CSA. The ownership and use of the space station is established by intergovernmental " \
                "treaties and agreements. The International Space Station is moving at close to 28,000 km/h so its " \
                "location changes really quick!."
    print("About ISS:\n" + about_iss)


def crew_data():
    # Printing ISS Crew Data
    raw_data = url_req.urlopen("http://api.open-notify.org/astros.json").read()  # ISS Members API
    json_data = json.loads(raw_data)

    iss_members = str(json_data["number"])

    print("\nThere are currently \"" + iss_members + "\" members in ISS. They are: \n")

    for i, j in enumerate(json_data["people"]):
        print(str(i+1) + ". '" + j["name"] + "' in '" + j["craft"] + "' Spacecraft")


def iss_data():
    # Getting ISS location

    raw_data = url_req.urlopen("http://api.open-notify.org/iss-now.json").read()  # ISS Location API
    json_data = json.loads(raw_data)
    latitude = str(json_data["iss_position"]["latitude"])
    longitude = str(json_data["iss_position"]["latitude"])

    # URL's to redirect to map
    gmap = "http://maps.google.com/maps?q=loc:" + latitude + "," + longitude  # http://maps.google.com/maps?q=loc:40.26577,92.54324
    oss = "https://www.openstreetmap.org/?mlat=" + latitude + "&mlon=" + longitude + "#map=4/" + latitude + "/" + longitude  # https://www.openstreetmap.org/?mlat=17.0988&mlon=74.4653#map=4/17.0988/74.4653

    inp = input("\nEnter 1 to show URL's\nEnter 2 to open map\n: ")

    print("ISS Latitude: " + latitude + ", Longitude: " + longitude + "\n")

    if inp == "1":

        print("Google Map URL: " + gmap)
        print("OpenStreetMap URL: " + oss)

    else:

        # Opens map in a browser

        print("\nOpening ISS Location In Your Browser")
        webbrowser.open_new(gmap)  # Google Map
        webbrowser.open_new(oss)   # OpenStreetMap


if __name__ == "__main__":
    # Calling

    data()
    crew_data()
    iss_data()
