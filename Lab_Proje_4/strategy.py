from abc import ABC, abstractmethod
import random


class KartSecmeStratejisi(ABC):
    @abstractmethod
    def kart_sec(self, kartlar, ozellik, moral):
        pass


class KolayStrateji(KartSecmeStratejisi):
    def kart_sec(self, kartlar, ozellik, moral):
        return random.choice(kartlar)


class OrtaStrateji(KartSecmeStratejisi):
    def kart_sec(self, kartlar, ozellik, moral):
        en_iyi = None
        en_yuksek = -1

        for kart in kartlar:
            puan = kart.performans_hesapla(ozellik, moral)
            if puan > en_yuksek:
                en_yuksek = puan
                en_iyi = kart

        return en_iyi