veri = "voltage0=32.12,voltage1=14.64,voltage2=32.15,voltage3=32.15,voltage4=32.15,voltage5=32.15,voltage6=32.15,voltage7=32.15,voltage8=32.15,voltage9=32.15,batvolt=42,temp=30"
veri_array = veri.split(',')

f = open("/root/data.txt", "w")
f.write(veri)
f.close()
