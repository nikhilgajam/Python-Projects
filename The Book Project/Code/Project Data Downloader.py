import os
import time
import TheBhagavadGitaAPI

# Automated data download program. Keep this program in a place where Data directory doesn't exist.

chp_ver_nos = {0:0, 1:47, 2:72, 3:43, 4:42, 5:29, 6:47, 7:30, 8:28, 9:34, 10:42, 11:55, 12:20, 13:35, 14:27, 15:20, 16:24, 17:28, 18:78}

api = TheBhagavadGitaAPI.TheBhagavadGita()

try:
    
    start = time.time()
    os.mkdir("Bhagavad_Gita")

    total_count = 720*3
    count = 0

    # English
    os.mkdir("Bhagavad_Gita/English")

    for i, j in chp_ver_nos.items():
        chp = str(i)
        os.mkdir("Bhagavad_Gita/English/Chapter_" + chp)
        for k in range(j+1):
            ver = str(k)
            data = api.getData(i, k)
            while "WinError" in data:
                data = api.getData(i, k)
                with open("a.txt", "w", encoding="utf-8") as p:
                    p.write(data)
            path = "Bhagavad_Gita/English/Chapter_" + chp + "/Verse_" + ver + ".txt"
            with open(path, "w", encoding="utf-8") as p:
                p.write(data)
            count += 1
            print("English Chapter " + chp + " Verse " + ver + " Writing Completed (" + str(count) + "/" + str(total_count) + ")")

    # Hindi
    os.mkdir("Bhagavad_Gita/Hindi")

    for i, j in chp_ver_nos.items():
        chp = str(i)
        os.mkdir("Bhagavad_Gita/Hindi/Chapter_" + chp)
        for k in range(j+1):
            ver = str(k)
            data = api.getData(i, k, "hi")
            while "WinError" in data:
                data = api.getData(i, k, "hi")
            path = "Bhagavad_Gita/Hindi/Chapter_" + chp + "/Verse_" + ver + ".txt"
            with open(path, "w", encoding="utf-8") as p:
                p.write(data)
            count += 1
            print("Hindi Chapter " + chp + " Verse " + ver + " Writing Completed (" + str(count) + "/" + str(total_count) + ")")

    # Telugu
    os.mkdir("Bhagavad_Gita/Telugu")

    for i, j in chp_ver_nos.items():
        chp = str(i)
        os.mkdir("Bhagavad_Gita/Telugu/Chapter_" + chp)
        for k in range(j+1):
            ver = str(k)
            data = api.getData(i, k, "te")
            while "WinError" in data:
                data = api.getData(i, k, "te")
            path = "Bhagavad_Gita/Telugu/Chapter_" + chp + "/Verse_" + ver + ".txt"
            with open(path, "w", encoding="utf-8") as p:
                p.write(data)
            count += 1
            print("Telugu Chapter " + chp + " Verse " + ver + " Writing Completed (" + str(count) + "/" + str(total_count) + ")")


    end = time.time()
    total_time = round((end-start)/60, 2)  # Converting To Minutes
    print("\n\nTotal Time Taken:", total_time, "Minutes")

except Exception as e:
    print(str(e))
