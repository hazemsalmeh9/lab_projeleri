import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QTextEdit, QListWidget
)
from data_loader import VeriOkuyucu
from models import Kullanici, Bilgisayar
from game_manager import OyunYonetici
from utils import kartlari_dagit
from strategy import OrtaStrateji


class OyunArayuzu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Akilli Sporcu Kart Ligi")
        self.setGeometry(200, 200, 700, 500)

        self.kullanici = None
        self.bilgisayar = None
        self.oyun = None
        self.toplam_tur = 12
        self.oynanan_tur = 0
        self.show_pc = False

        self.layout = QVBoxLayout()

        self.baslik = QLabel("Akilli Sporcu Kart Ligi")
        self.layout.addWidget(self.baslik)

        self.skor_label = QLabel("Skor -> Kullanici: 0 | Bilgisayar: 0")
        self.layout.addWidget(self.skor_label)

        self.moral_label = QLabel("Moral -> Kullanici: 70 | Bilgisayar: 70")
        self.layout.addWidget(self.moral_label)

        self.tur_label = QLabel("Tur: Hazir")
        self.layout.addWidget(self.tur_label)

        self.sonuc_alani = QTextEdit()
        self.sonuc_alani.setReadOnly(True)
        self.layout.addWidget(self.sonuc_alani)

        self.kart_listesi_widget = QListWidget()
        self.layout.addWidget(self.kart_listesi_widget)

        self.baslat_btn = QPushButton("Oyunu Baslat")
        self.baslat_btn.clicked.connect(self.oyunu_baslat)
        self.layout.addWidget(self.baslat_btn)

        self.tur_btn = QPushButton("Sonraki Turu Oyna")
        self.tur_btn.clicked.connect(self.tur_oyna)
        self.tur_btn.setEnabled(False)
        self.layout.addWidget(self.tur_btn)

        self.toggle_btn = QPushButton("Show PC Cards")
        self.toggle_btn.clicked.connect(self.toggle_pc)
        self.layout.addWidget(self.toggle_btn)

        self.setLayout(self.layout)

    def kart_listesini_guncelle(self):
        self.kart_listesi_widget.clear()

        if not self.oyun:
            return

        brans = self.oyun.mevcut_brans()
        uygun_kartlar = self.kullanici.bransa_gore_kartlar(brans)

        for kart in uygun_kartlar:
            self.kart_listesi_widget.addItem(f"{kart.sporcu_adi} ({kart.brans})")

    def oyunu_baslat(self):
        kartlar = VeriOkuyucu.sporculari_oku("sporcular.csv")

        self.kullanici = Kullanici("U1", "Aboudi")
        self.bilgisayar = Bilgisayar("B1", "PC", OrtaStrateji())

        kartlari_dagit(kartlar, self.kullanici, self.bilgisayar)
        self.oyun = OyunYonetici(self.kullanici, self.bilgisayar)

        self.oynanan_tur = 0
        self.sonuc_alani.clear()
        self.sonuc_alani.append("Oyun basladi!")
        self.kart_listesini_guncelle()

        self.tur_btn.setEnabled(True)

    def guncelle_ekran(self):
        self.skor_label.setText(
            f"Skor -> Kullanici: {self.kullanici.skor} | Bilgisayar: {self.bilgisayar.skor}"
        )
        self.moral_label.setText(
            f"Moral -> Kullanici: {self.kullanici.moral} | Bilgisayar: {self.bilgisayar.moral}"
        )

    def tur_oyna(self):
        selected_item = self.kart_listesi_widget.currentItem()

        if not selected_item:
            self.sonuc_alani.append("Lutfen bir kart sec!")
            return

        kart_adi = selected_item.text().split(" (")[0]

        if self.oynanan_tur >= self.toplam_tur:
            self.sonuc_alani.append("\nOyun bitti!")
            self.tur_btn.setEnabled(False)
            return

        brans = self.oyun.mevcut_brans()
        self.tur_label.setText(f"Tur: {self.oynanan_tur + 1} - {brans}")

        sonuc_text = self.oyun.tur_oyna_arayuzlu(kart_adi)
        self.sonuc_alani.append(sonuc_text)
        self.sonuc_alani.append("-" * 50)

        self.oynanan_tur += 1
        self.guncelle_ekran()
        self.kart_listesini_guncelle()

        if self.oynanan_tur >= self.toplam_tur:
            final_text = self.oyun.kazanan_belirle_metin()
            self.sonuc_alani.append("\n" + final_text)
            self.tur_btn.setEnabled(False)

    def toggle_pc(self):
        if self.bilgisayar is None:
            self.sonuc_alani.append("Once oyunu baslatin!")
            return

        self.show_pc = not self.show_pc

        if self.show_pc:
            self.toggle_btn.setText("Hide PC Cards")
            self.sonuc_alani.append("\n--- PC Kartlari ---")

            for kart in self.bilgisayar.kart_listesi:
                self.sonuc_alani.append(kart.kart_bilgisi_yazdir())

        else:
            self.toggle_btn.setText("Show PC Cards")
            self.sonuc_alani.append("\nPC kartlari gizlendi.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = OyunArayuzu()
    pencere.show()
    sys.exit(app.exec())