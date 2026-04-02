
import random

class OyunYonetici:
    def __init__(self, kullanici, bilgisayar):
        self.kullanici = kullanici
        self.bilgisayar = bilgisayar
        self.tur_sirasi = ["Futbol", "Basketbol", "Voleybol"]
        self.tur_index = 0

    def tur_oyna_arayuzlu(self, secilen_kart_adi=None):
        metinler = []

        brans = self.mevcut_brans()
        metinler.append(f"--- TUR: {brans} ---")

        ozellik = self.ozellik_sec(brans)
        kullanici_kartlar = self.kullanici.kart_sec(brans)

        if not kullanici_kartlar:
            self.tur_index += 1
            return "Kullanicida uygun kart yok."

        kullanici_kart = None

        if secilen_kart_adi is not None:
            for kart in kullanici_kartlar:
                if kart.sporcu_adi == secilen_kart_adi:
                    kullanici_kart = kart
                    break

        if kullanici_kart is None:
            return f"Lutfen {brans} bransina uygun bir kart sec!"
        bilgisayar_kart = self.bilgisayar.kart_sec(brans, ozellik)

        if not bilgisayar_kart:
            self.tur_index += 1
            return "Bilgisayarda uygun kart yok."

        metinler.append(f"Kullanici kart: {kullanici_kart.kart_bilgisi_yazdir()}")
        metinler.append(f"Bilgisayar kart: {bilgisayar_kart.kart_bilgisi_yazdir()}")
        metinler.append(f"Karsilastirilan ozellik: {ozellik}")

        kullanici_puan = kullanici_kart.performans_hesapla(ozellik, self.kullanici.moral)
        bilgisayar_puan = bilgisayar_kart.performans_hesapla(ozellik, self.bilgisayar.moral)

        metinler.append(f"Kullanici puan: {kullanici_puan}")
        metinler.append(f"Bilgisayar puan: {bilgisayar_puan}")

        if kullanici_puan > bilgisayar_puan:
            metinler.append("Kullanici kazandi!")
            self.kullanici.skor_guncelle(10)
            self.kullanici.kazanilan_tur += 1

            self.kullanici.moral_guncelle("galibiyet")
            self.bilgisayar.moral_guncelle("maglubiyet")

            kullanici_kart.enerji_guncelle("galibiyet")
            bilgisayar_kart.enerji_guncelle("maglubiyet")

            kullanici_kart.deneyim_guncelle("galibiyet")
            bilgisayar_kart.deneyim_guncelle("maglubiyet")

        elif kullanici_puan < bilgisayar_puan:
            metinler.append("Bilgisayar kazandi!")
            self.bilgisayar.skor_guncelle(10)
            self.bilgisayar.kazanilan_tur += 1

            self.kullanici.moral_guncelle("maglubiyet")
            self.bilgisayar.moral_guncelle("galibiyet")

            kullanici_kart.enerji_guncelle("maglubiyet")
            bilgisayar_kart.enerji_guncelle("galibiyet")

            kullanici_kart.deneyim_guncelle("maglubiyet")
            bilgisayar_kart.deneyim_guncelle("galibiyet")

        else:
            metinler.append("Ilk esitlik, tie-break basliyor...")

            kullanici_stats = kullanici_kart.sporcu_puani_goster()
            bilgisayar_stats = bilgisayar_kart.sporcu_puani_goster()

            toplam_kullanici = sum(kullanici_stats.values())
            toplam_bilgisayar = sum(bilgisayar_stats.values())

            if toplam_kullanici > toplam_bilgisayar:
                metinler.append("Kullanici kazandi (tie-break: toplam ozellik)")
                self.kullanici.skor_guncelle(10)
                self.kullanici.kazanilan_tur += 1
                self.kullanici.moral_guncelle("galibiyet")
                self.bilgisayar.moral_guncelle("maglubiyet")
                kullanici_kart.enerji_guncelle("galibiyet")
                bilgisayar_kart.enerji_guncelle("maglubiyet")
                kullanici_kart.deneyim_guncelle("galibiyet")
                bilgisayar_kart.deneyim_guncelle("maglubiyet")

            elif toplam_kullanici < toplam_bilgisayar:
                metinler.append("Bilgisayar kazandi (tie-break: toplam ozellik)")
                self.bilgisayar.skor_guncelle(10)
                self.bilgisayar.kazanilan_tur += 1
                self.kullanici.moral_guncelle("maglubiyet")
                self.bilgisayar.moral_guncelle("galibiyet")
                kullanici_kart.enerji_guncelle("maglubiyet")
                bilgisayar_kart.enerji_guncelle("galibiyet")
                kullanici_kart.deneyim_guncelle("maglubiyet")
                bilgisayar_kart.deneyim_guncelle("galibiyet")

            else:
                if kullanici_kart.dayaniklilik > bilgisayar_kart.dayaniklilik:
                    metinler.append("Kullanici kazandi (dayaniklilik)")
                    self.kullanici.skor_guncelle(10)
                    self.kullanici.kazanilan_tur += 1
                elif kullanici_kart.dayaniklilik < bilgisayar_kart.dayaniklilik:
                    metinler.append("Bilgisayar kazandi (dayaniklilik)")
                    self.bilgisayar.skor_guncelle(10)
                    self.bilgisayar.kazanilan_tur += 1
                else:
                    metinler.append("Gercek Berabere!")
                    self.kullanici.beraberlik_sayisi += 1
                    self.bilgisayar.beraberlik_sayisi += 1
                    self.kullanici.moral_guncelle("beraberlik")
                    self.bilgisayar.moral_guncelle("beraberlik")
                    kullanici_kart.enerji_guncelle("beraberlik")
                    bilgisayar_kart.enerji_guncelle("beraberlik")
                    kullanici_kart.deneyim_guncelle("beraberlik")
                    bilgisayar_kart.deneyim_guncelle("beraberlik")

        kullanici_kart.seviye_atla_kontrol()
        bilgisayar_kart.seviye_atla_kontrol()

        metinler.append(f"Skor -> Kullanici: {self.kullanici.skor} | Bilgisayar: {self.bilgisayar.skor}")
        metinler.append(f"Moral -> Kullanici: {self.kullanici.moral} | Bilgisayar: {self.bilgisayar.moral}")
        metinler.append(f"{kullanici_kart.sporcu_adi} seviye: {kullanici_kart.seviye}")
        metinler.append(f"{bilgisayar_kart.sporcu_adi} seviye: {bilgisayar_kart.seviye}")

        self.tur_index += 1
        return "\n".join(metinler)

    def mevcut_brans(self):
        return self.tur_sirasi[self.tur_index % 3]
    
    def kazanan_belirle(self):
        print("\n--- OYUN SONU ---")
        print(f"Kullanici skor: {self.kullanici.skor}")
        print(f"Bilgisayar skor: {self.bilgisayar.skor}")

        if self.kullanici.skor > self.bilgisayar.skor:
            print("Genel kazanan: Kullanici")
            return

        elif self.kullanici.skor < self.bilgisayar.skor:
            print("Genel kazanan: Bilgisayar")
            return

        print("Skor esit! Tie-break basliyor...")

        if self.kullanici.kazanilan_tur > self.bilgisayar.kazanilan_tur:
            print("Genel kazanan: Kullanici (kazanilan tur sayisi)")
            return
        elif self.kullanici.kazanilan_tur < self.bilgisayar.kazanilan_tur:
            print("Genel kazanan: Bilgisayar (kazanilan tur sayisi)")
            return

        kullanici_enerji = sum(k.enerji for k in self.kullanici.kart_listesi)
        bilgisayar_enerji = sum(k.enerji for k in self.bilgisayar.kart_listesi)

        if kullanici_enerji > bilgisayar_enerji:
            print("Genel kazanan: Kullanici (kalan enerji)")
            return
        elif kullanici_enerji < bilgisayar_enerji:
            print("Genel kazanan: Bilgisayar (kalan enerji)")
            return

        kullanici_yuksek_seviye = sum(1 for k in self.kullanici.kart_listesi if k.seviye == 3)
        bilgisayar_yuksek_seviye = sum(1 for k in self.bilgisayar.kart_listesi if k.seviye == 3)

        if kullanici_yuksek_seviye > bilgisayar_yuksek_seviye:
            print("Genel kazanan: Kullanici (en yuksek seviyeli kart sayisi)")
            return
        elif kullanici_yuksek_seviye < bilgisayar_yuksek_seviye:
            print("Genel kazanan: Bilgisayar (en yuksek seviyeli kart sayisi)")
            return

        if self.kullanici.beraberlik_sayisi < self.bilgisayar.beraberlik_sayisi:
            print("Genel kazanan: Kullanici (daha az beraberlik)")
            return
        elif self.kullanici.beraberlik_sayisi > self.bilgisayar.beraberlik_sayisi:
            print("Genel kazanan: Bilgisayar (daha az beraberlik)")
            return

        print("Oyun tamamen berabere bitti!")
    
    def kazanan_belirle_metin(self):
        satirlar = []
        satirlar.append("--- OYUN SONU ---")
        satirlar.append(f"Kullanici skor: {self.kullanici.skor}")
        satirlar.append(f"Bilgisayar skor: {self.bilgisayar.skor}")

        if self.kullanici.skor > self.bilgisayar.skor:
            satirlar.append("Genel kazanan: Kullanici")
            return "\n".join(satirlar)

        elif self.kullanici.skor < self.bilgisayar.skor:
            satirlar.append("Genel kazanan: Bilgisayar")
            return "\n".join(satirlar)

        satirlar.append("Skor esit! Tie-break basliyor...")

        if self.kullanici.kazanilan_tur > self.bilgisayar.kazanilan_tur:
            satirlar.append("Genel kazanan: Kullanici (kazanilan tur sayisi)")
            return "\n".join(satirlar)
        elif self.kullanici.kazanilan_tur < self.bilgisayar.kazanilan_tur:
            satirlar.append("Genel kazanan: Bilgisayar (kazanilan tur sayisi)")
            return "\n".join(satirlar)

        kullanici_enerji = sum(k.enerji for k in self.kullanici.kart_listesi)
        bilgisayar_enerji = sum(k.enerji for k in self.bilgisayar.kart_listesi)

        if kullanici_enerji > bilgisayar_enerji:
            satirlar.append("Genel kazanan: Kullanici (kalan enerji)")
            return "\n".join(satirlar)
        elif kullanici_enerji < bilgisayar_enerji:
            satirlar.append("Genel kazanan: Bilgisayar (kalan enerji)")
            return "\n".join(satirlar)

        kullanici_yuksek_seviye = sum(1 for k in self.kullanici.kart_listesi if k.seviye == 3)
        bilgisayar_yuksek_seviye = sum(1 for k in self.bilgisayar.kart_listesi if k.seviye == 3)

        if kullanici_yuksek_seviye > bilgisayar_yuksek_seviye:
            satirlar.append("Genel kazanan: Kullanici (en yuksek seviyeli kart sayisi)")
            return "\n".join(satirlar)
        elif kullanici_yuksek_seviye < bilgisayar_yuksek_seviye:
            satirlar.append("Genel kazanan: Bilgisayar (en yuksek seviyeli kart sayisi)")
            return "\n".join(satirlar)

        if self.kullanici.beraberlik_sayisi < self.bilgisayar.beraberlik_sayisi:
            satirlar.append("Genel kazanan: Kullanici (daha az beraberlik)")
            return "\n".join(satirlar)
        elif self.kullanici.beraberlik_sayisi > self.bilgisayar.beraberlik_sayisi:
            satirlar.append("Genel kazanan: Bilgisayar (daha az beraberlik)")
            return "\n".join(satirlar)

        satirlar.append("Oyun tamamen berabere bitti!")
        return "\n".join(satirlar)

    def ozellik_sec(self, brans):
        if brans == "Futbol":
            return random.choice(["penalti", "serbest_vurus", "kaleci_karsi_karsiya"])
        elif brans == "Basketbol":
            return random.choice(["ikilik", "ucluk", "serbest_atis"])
        elif brans == "Voleybol":
            return random.choice(["servis", "blok", "smac"])

    def tur_oyna(self):
        brans = self.mevcut_brans()
        print(f"\n--- TUR: {brans} ---")

        kullanici_kartlar = self.kullanici.kart_sec(brans)

        if not kullanici_kartlar:
            print("Kullanicida uygun kart yok.")
            self.tur_index += 1
            return

        # مؤقتًا نختار أول كرت
        brans = self.mevcut_brans()
        print(f"\n--- TUR: {brans} ---")

        # أول شي نحدد الخاصية
        ozellik = self.ozellik_sec(brans)

        # بعدين نجيب الكروت
        kullanici_kartlar = self.kullanici.kart_sec(brans)

        if not kullanici_kartlar:
            print("Kullanicida uygun kart yok.")
            self.tur_index += 1
            return

        kullanici_kart = kullanici_kartlar[0]

        # هلّق الكمبيوتر يختار بناءً على الخاصية
        bilgisayar_kart = self.bilgisayar.kart_sec(brans, ozellik)

        if not bilgisayar_kart:
            print("Bilgisayarda uygun kart yok.")
            self.tur_index += 1
            return

        print("Kullanici kart:", kullanici_kart.kart_bilgisi_yazdir())
        print("Bilgisayar kart:", bilgisayar_kart.kart_bilgisi_yazdir())

        ozellik = self.ozellik_sec(brans)
        print("Karsilastirilan ozellik:", ozellik)

        kullanici_puan = kullanici_kart.performans_hesapla(ozellik, self.kullanici.moral)
        bilgisayar_puan = bilgisayar_kart.performans_hesapla(ozellik, self.bilgisayar.moral)

        print(f"Kullanici puan: {kullanici_puan}")
        print(f"Bilgisayar puan: {bilgisayar_puan}")




        if kullanici_puan > bilgisayar_puan:
            print("Kullanici kazandi!")
            self.kullanici.skor_guncelle(10)
            self.kullanici.kazanilan_tur += 1

            self.kullanici.moral_guncelle("galibiyet")
            self.bilgisayar.moral_guncelle("maglubiyet")

            kullanici_kart.enerji_guncelle("galibiyet")
            bilgisayar_kart.enerji_guncelle("maglubiyet")

            kullanici_kart.deneyim_guncelle("galibiyet")
            bilgisayar_kart.deneyim_guncelle("maglubiyet")

        elif kullanici_puan < bilgisayar_puan:
            print("Bilgisayar kazandi!")
            self.bilgisayar.skor_guncelle(10)
            self.bilgisayar.kazanilan_tur += 1

            self.kullanici.moral_guncelle("maglubiyet")
            self.bilgisayar.moral_guncelle("galibiyet")

            kullanici_kart.enerji_guncelle("maglubiyet")
            bilgisayar_kart.enerji_guncelle("galibiyet")

            kullanici_kart.deneyim_guncelle("maglubiyet")
            bilgisayar_kart.deneyim_guncelle("galibiyet")

        else:

            print("Ilk esitlik, tie-break basliyor...")

            # باقي الخصائص
            kullanici_stats = kullanici_kart.sporcu_puani_goster()
            bilgisayar_stats = bilgisayar_kart.sporcu_puani_goster()

            toplam_kullanici = sum(kullanici_stats.values())
            toplam_bilgisayar = sum(bilgisayar_stats.values())

            if toplam_kullanici > toplam_bilgisayar:
                print("Kullanici kazandi (tie-break: toplam ozellik)")
                self.kullanici.skor_guncelle(10)

            elif toplam_kullanici < toplam_bilgisayar:
                print("Bilgisayar kazandi (tie-break: toplam ozellik)")
                self.bilgisayar.skor_guncelle(10)

            else:
                # dayanıklılık
                if kullanici_kart.dayaniklilik > bilgisayar_kart.dayaniklilik:
                    print("Kullanici kazandi (dayaniklilik)")
                    self.kullanici.skor_guncelle(10)

                elif kullanici_kart.dayaniklilik < bilgisayar_kart.dayaniklilik:
                    print("Bilgisayar kazandi (dayaniklilik)")
                    self.bilgisayar.skor_guncelle(10)

                else:
                    self.kullanici.beraberlik_sayisi += 1
                    self.bilgisayar.beraberlik_sayisi += 1
                    print("Gercek Berabere!")


        kullanici_kart.seviye_atla_kontrol()
        bilgisayar_kart.seviye_atla_kontrol()
        self.kullanici.moral_guncelle("beraberlik")
        self.bilgisayar.moral_guncelle("beraberlik")

        print(f"Skor -> Kullanici: {self.kullanici.skor} | Bilgisayar: {self.bilgisayar.skor}")
        print(f"Moral -> Kullanici: {self.kullanici.moral} | Bilgisayar: {self.bilgisayar.moral}")
        print(f"{kullanici_kart.sporcu_adi} seviye: {kullanici_kart.seviye}")
        print(f"{bilgisayar_kart.sporcu_adi} seviye: {bilgisayar_kart.seviye}")

        self.tur_index += 1




