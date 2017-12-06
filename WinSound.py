import winsound
from playsound import playsound

import subprocess
import os
cwd = os.getcwd()
AudioPath = '\\Assets\\Audio\\'
Audio = cwd + AudioPath + 'Jarvis.wav'
print Audio
winsound.Beep(700, 950)
#playsound(AudioPath+'Jarvis.wav')



# Play Windows exit sound.
winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

# Probably play Windows default sound, if any is registered (because
# "*" probably isn't the registered name of any sound).
#winsound.PlaySound("*", winsound.SND_ALIAS)
winsound.PlaySound(Audio, winsound.SND_FILENAME)
