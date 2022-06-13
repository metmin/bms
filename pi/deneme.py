from os.path import exists
from time import sleep

def control(counter = 1):
    if not (exists('/dev/ttyACM0')):
        sleep(0.1)
        if(counter < 60):
            print('motor sürücüsünün bağlı olduğu port bulunamadı yeniden deneniyor')
            return control(counter + 1)
        return False        
    return True

def deneme():
    if control() == False:
        return
    print('sa')

deneme()