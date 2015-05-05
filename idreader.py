from subprocess import call

def get_id_file():
    call("adb pull /sdcard/ids.txt", shell=True)
