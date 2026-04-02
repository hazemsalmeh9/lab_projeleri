from data_loader import VeriOkuyucu
from models import Kullanici, Bilgisayar
from game_manager import OyunYonetici
from utils import kartlari_dagit
from strategy import KolayStrateji, OrtaStrateji

kartlar = VeriOkuyucu.sporculari_oku("sporcular.csv")

kullanici = Kullanici("U1", "Abdulrahman")
bilgisayar = Bilgisayar("B1", "PC", KolayStrateji()) 
# bilgisayar = Bilgisayar("B1", "PC", OrtaStrateji())


kartlari_dagit(kartlar, kullanici, bilgisayar)

print("Kullanici kart sayisi:", len(kullanici.kart_listesi))
print("Bilgisayar kart sayisi:", len(bilgisayar.kart_listesi))

print("Kullanici Futbol:", len(kullanici.bransa_gore_kartlar("Futbol")))
print("Kullanici Basketbol:", len(kullanici.bransa_gore_kartlar("Basketbol")))
print("Kullanici Voleybol:", len(kullanici.bransa_gore_kartlar("Voleybol")))

print("Bilgisayar Futbol:", len(bilgisayar.bransa_gore_kartlar("Futbol")))
print("Bilgisayar Basketbol:", len(bilgisayar.bransa_gore_kartlar("Basketbol")))
print("Bilgisayar Voleybol:", len(bilgisayar.bransa_gore_kartlar("Voleybol")))

oyun = OyunYonetici(kullanici, bilgisayar)

for _ in range(12):
    oyun.tur_oyna()

oyun.kazanan_belirle()
