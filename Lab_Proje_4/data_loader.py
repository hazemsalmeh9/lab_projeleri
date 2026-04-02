import csv
from models import Futbolcu, Basketbolcu, Voleybolcu


class VeriOkuyucu:
    @staticmethod
    def sporculari_oku(dosya_adi):
        kartlar = []

        with open(dosya_adi, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                sporcu_turu = row["tur"]

                if sporcu_turu == "Futbolcu":
                    kart = Futbolcu(
                        row["id"],
                        row["ad"],
                        row["takim"],
                        int(row["ozellik1"]),
                        int(row["ozellik2"]),
                        int(row["ozellik3"]),
                        int(row["dayaniklilik"]),
                        int(row["enerji"]),
                        row["ozel_yetenek"]
                    )

                elif sporcu_turu == "Basketbolcu":
                    kart = Basketbolcu(
                        row["id"],
                        row["ad"],
                        row["takim"],
                        int(row["ozellik1"]),
                        int(row["ozellik2"]),
                        int(row["ozellik3"]),
                        int(row["dayaniklilik"]),
                        int(row["enerji"]),
                        row["ozel_yetenek"]
                    )

                elif sporcu_turu == "Voleybolcu":
                    kart = Voleybolcu(
                        row["id"],
                        row["ad"],
                        row["takim"],
                        int(row["ozellik1"]),
                        int(row["ozellik2"]),
                        int(row["ozellik3"]),
                        int(row["dayaniklilik"]),
                        int(row["enerji"]),
                        row["ozel_yetenek"]
                    )
                else:
                    raise ValueError(f"Bilinmeyen sporcu türü: {sporcu_turu}")

                kartlar.append(kart)

        return kartlar