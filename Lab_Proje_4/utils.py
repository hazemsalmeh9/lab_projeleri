import random


def kartlari_dagit(kartlar, kullanici, bilgisayar):
    futbolcular = [k for k in kartlar if k.brans == "Futbol"]
    basketbolcular = [k for k in kartlar if k.brans == "Basketbol"]
    voleybolcular = [k for k in kartlar if k.brans == "Voleybol"]

    random.shuffle(futbolcular)
    random.shuffle(basketbolcular)
    random.shuffle(voleybolcular)

    for kart in futbolcular[:4]:
        kullanici.kart_ekle(kart)
    for kart in futbolcular[4:]:
        bilgisayar.kart_ekle(kart)

    for kart in basketbolcular[:4]:
        kullanici.kart_ekle(kart)
    for kart in basketbolcular[4:]:
        bilgisayar.kart_ekle(kart)

    for kart in voleybolcular[:4]:
        kullanici.kart_ekle(kart)
    for kart in voleybolcular[4:]:
        bilgisayar.kart_ekle(kart)


        