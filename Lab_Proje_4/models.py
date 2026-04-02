from abc import ABC, abstractmethod
import random

class Sporcu(ABC):
    def __init__(self, sporcu_id, sporcu_adi, sporcu_takim, brans,
                 dayaniklilik, enerji, ozel_yetenek):
        self.sporcu_id = sporcu_id
        self.sporcu_adi = sporcu_adi
        self.sporcu_takim = sporcu_takim
        self.brans = brans
        self.dayaniklilik = dayaniklilik
        self.enerji = enerji
        self.max_enerji = enerji
        self.seviye = 1
        self.deneyim_puani = 0
        self.kart_kullanildi_mi = False
        self.ozel_yetenek = ozel_yetenek
        self.kullanim_sayisi = 0
        self.kazanma_sayisi = 0
        self.kaybetme_sayisi = 0

    @abstractmethod
    def sporcu_puani_goster(self):
        pass

    @abstractmethod
    def kart_bilgisi_yazdir(self):
        pass

    def moral_bonusu_hesapla(self, moral):
        if moral >= 90:
            return 10
        elif moral >= 80:
            return 5
        elif moral < 50:
            return -5
        return 0

    def enerji_cezasi_hesapla(self, temel_ozellik):
        if self.enerji > 70:
            return 0
        elif 40 <= self.enerji <= 70:
            return temel_ozellik * 0.10
        elif 0 < self.enerji < 40:
            return temel_ozellik * 0.20
        return temel_ozellik

    def seviye_bonusu_hesapla(self):
        if self.seviye == 2:
            return 5
        elif self.seviye == 3:
            return 10
        return 0

    def ozel_yetenek_bonusu(self):
        if self.ozel_yetenek == "Legend":
            return 10

        elif self.ozel_yetenek == "Finisher":
            if self.enerji < 40:
                return 15

        elif self.ozel_yetenek == "Clutch Player":
            return 5  # مؤقت

        elif self.ozel_yetenek == "Captain":
            return 3

        elif self.ozel_yetenek == "Defender":
            return 4

        elif self.ozel_yetenek == "Veteran":
            return 6

        return 0

    def performans_hesapla(self, ozellik_adi, moral):
        temel_ozellik = getattr(self, ozellik_adi)
        moral_bonusu = self.moral_bonusu_hesapla(moral)
        enerji_cezasi = self.enerji_cezasi_hesapla(temel_ozellik)
        seviye_bonusu = self.seviye_bonusu_hesapla()
        ozel_bonus = self.ozel_yetenek_bonusu()

        guncel_puan = temel_ozellik + moral_bonusu + ozel_bonus - enerji_cezasi + seviye_bonusu
        return round(guncel_puan, 2)

    def enerji_guncelle(self, sonuc):
        if sonuc == "galibiyet":
            self.enerji = max(0, self.enerji - 5)
            self.kazanma_sayisi += 1
        elif sonuc == "maglubiyet":
            self.enerji = max(0, self.enerji - 10)
            self.kaybetme_sayisi += 1
        elif sonuc == "beraberlik":
            self.enerji = max(0, self.enerji - 3)

    def deneyim_guncelle(self, sonuc):
        if sonuc == "galibiyet":
            self.deneyim_puani += 2
        elif sonuc == "beraberlik":
            self.deneyim_puani += 1

    def seviye_atla_kontrol(self):
        if self.seviye == 1 and (self.kazanma_sayisi >= 2 or self.deneyim_puani >= 4):
            self.seviye = 2
            self.max_enerji += 10
            self.dayaniklilik += 5
            self.ozellikleri_arttir()
        elif self.seviye == 2 and (self.kazanma_sayisi >= 4 or self.deneyim_puani >= 8):
            self.seviye = 3
            self.max_enerji += 10
            self.dayaniklilik += 5
            self.ozellikleri_arttir()

    @abstractmethod
    def ozellikleri_arttir(self):
        pass


class Futbolcu(Sporcu):
    def __init__(self, sporcu_id, sporcu_adi, sporcu_takim,
                 penalti, serbest_vurus, kaleci_karsi_karsiya,
                 dayaniklilik, enerji, ozel_yetenek):
        super().__init__(sporcu_id, sporcu_adi, sporcu_takim, "Futbol",
                         dayaniklilik, enerji, ozel_yetenek)
        self.penalti = penalti
        self.serbest_vurus = serbest_vurus
        self.kaleci_karsi_karsiya = kaleci_karsi_karsiya

    def sporcu_puani_goster(self):
        return {
            "penalti": self.penalti,
            "serbest_vurus": self.serbest_vurus,
            "kaleci_karsi_karsiya": self.kaleci_karsi_karsiya
        }

    def kart_bilgisi_yazdir(self):
        return f"{self.sporcu_adi} | {self.brans} | {self.sporcu_takim}"

    def ozellikleri_arttir(self):
        self.penalti += 5
        self.serbest_vurus += 5
        self.kaleci_karsi_karsiya += 5


class Basketbolcu(Sporcu):
    def __init__(self, sporcu_id, sporcu_adi, sporcu_takim,
                 ikilik, ucluk, serbest_atis,
                 dayaniklilik, enerji, ozel_yetenek):
        super().__init__(sporcu_id, sporcu_adi, sporcu_takim, "Basketbol",
                         dayaniklilik, enerji, ozel_yetenek)
        self.ikilik = ikilik
        self.ucluk = ucluk
        self.serbest_atis = serbest_atis

    def sporcu_puani_goster(self):
        return {
            "ikilik": self.ikilik,
            "ucluk": self.ucluk,
            "serbest_atis": self.serbest_atis
        }

    def kart_bilgisi_yazdir(self):
        return f"{self.sporcu_adi} | {self.brans} | {self.sporcu_takim}"

    def ozellikleri_arttir(self):
        self.ikilik += 5
        self.ucluk += 5
        self.serbest_atis += 5


class Voleybolcu(Sporcu):
    def __init__(self, sporcu_id, sporcu_adi, sporcu_takim,
                 servis, blok, smac,
                 dayaniklilik, enerji, ozel_yetenek):
        super().__init__(sporcu_id, sporcu_adi, sporcu_takim, "Voleybol",
                         dayaniklilik, enerji, ozel_yetenek)
        self.servis = servis
        self.blok = blok
        self.smac = smac

    def sporcu_puani_goster(self):
        return {
            "servis": self.servis,
            "blok": self.blok,
            "smac": self.smac
        }

    def kart_bilgisi_yazdir(self):
        return f"{self.sporcu_adi} | {self.brans} | {self.sporcu_takim}"

    def ozellikleri_arttir(self):
        self.servis += 5
        self.blok += 5
        self.smac += 5






class Oyuncu(ABC):
    def __init__(self, oyuncu_id, oyuncu_adi):
        self.oyuncu_id = oyuncu_id
        self.oyuncu_adi = oyuncu_adi
        self.skor = 0
        self.moral = 70
        self.kart_listesi = []
        self.galibiyet_serisi = 0
        self.kaybetme_serisi = 0
        self.kazanilan_tur = 0
        self.beraberlik_sayisi = 0

    def kart_ekle(self, kart):
        self.kart_listesi.append(kart)

    def bransa_gore_kartlar(self, brans):
        return [
            kart for kart in self.kart_listesi 
            if kart.brans == brans 
            and kart.enerji > 0
        ]

    def skor_guncelle(self, puan):
        self.skor += puan

    def moral_guncelle(self, sonuc):
        if sonuc == "galibiyet":
            self.galibiyet_serisi += 1
            self.kaybetme_serisi = 0

            if self.galibiyet_serisi == 2:
                self.moral = min(100, self.moral + 10)
            elif self.galibiyet_serisi >= 3:
                self.moral = min(100, self.moral + 15)

        elif sonuc == "maglubiyet":
            self.kaybetme_serisi += 1
            self.galibiyet_serisi = 0

            if self.kaybetme_serisi >= 2:
                self.moral = max(0, self.moral - 10)

    @abstractmethod
    def kart_sec(self, brans):
        pass


class Kullanici(Oyuncu):
    def kart_sec(self, brans):
        uygun_kartlar = self.bransa_gore_kartlar(brans)
        return uygun_kartlar


class Bilgisayar(Oyuncu):
    def __init__(self, oyuncu_id, oyuncu_adi, strateji):
        super().__init__(oyuncu_id, oyuncu_adi)
        self.strateji = strateji

    def kart_sec(self, brans, ozellik):
        uygun_kartlar = self.bransa_gore_kartlar(brans)

        if not uygun_kartlar:
            return None

        return self.strateji.kart_sec(
            uygun_kartlar,
            ozellik,
            self.moral
        )