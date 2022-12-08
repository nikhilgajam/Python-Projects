import os
from urllib.request import Request, urlopen
import time

# Automated picture download program. Keep this program in a place where Picture directory doesn't exist.

try:
    start = time.time()
    os.mkdir("Pictures")
    for i in range(1, 19):
        num = str(i)
        url="https://www.holy-bhagavad-gita.org/public/images/bg/" + num + ".jpg"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})  # To access the websites which show errors
        data = urlopen(req).read()
        
        with open("Pictures/Chapter " + num + ".jpg", "wb") as p:
            p.write(data)

    end = time.time()
    total_time = (end-start)/60  # Converting To Minutes
    print("Total Time Taken:", total_time, "Minutes")

except Exception as e:
    print(str(e))

