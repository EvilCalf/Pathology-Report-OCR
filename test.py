import os
for root, dirs, files in os.walk("sckxcout/"):
    for file in files:
        print(root+file)
