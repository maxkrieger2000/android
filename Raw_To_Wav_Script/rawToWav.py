import os

#run script in an4_clstk or an4test_clstk folder
def main():
    os.system("mkdir wav_files")
    for directory in os.listdir():
        if(os.path.isdir(directory)):
            directory_name = directory + "/"
            for file in os.listdir(directory_name):
                if(file.endswith(".raw")):                
                    new_name = file.replace(".raw", ".wav")
                    os.system(
                        "sox -B -b 16 -c 1 -e signed -r 16k " + directory + "/" + file + " wav_files/" + new_name)


if __name__ == "__main__":
    main()

