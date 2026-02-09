from neo4j import GraphDatabase 
import json

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "12345678"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

# film arama fonksiyonu

def search_movie():
    keyword = input("\nFilmin İsmini Giriniz: ").strip()

    if len(keyword) < 3:
        print("\nLütfen en az 3 karakter giriniz")
        return None

# "With" Acma kapatma islemini kolaylastirir.
    with driver.session() as session:
        result = session.run(
            """
            MATCH (m:Movie)
            WHERE tolower(m.title) CONTAINS tolower($keyword)
            RETURN elementId(m) AS id, m.title AS title
            """, keyword = keyword
        )
        movies = [(record["id"], record["title"]) for record in result]
        if not movies :
            print("Film Bulunamadı") 
            return None
        
        print("\nFilmler Bulundu:")
        for i , movie in enumerate(movies):
            print(f"{i} - {movie[1]}")

        try:
            choice = int(input("\nFilm Numarası Seçiniz: "))
        except ValueError:
            print("\nLütfen Sayı Giriniz.")
            return None

        if choice < 0 or choice >= len(movies):
            print("\nGeçersiz Film Numarası.")
            return None

        return movies[choice]


# filmin detaylarini yazan fonksiyon
def show_movie_details(movie_id):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (m:Movie)
            WHERE elementId(m) = $id

            OPTIONAL MATCH (d:Director)-[:DIRECTED]->(m)
            OPTIONAL MATCH (a:Actor)-[:ACTED_IN]->(m)

            RETURN 
                m.title AS title,
                m.released AS year,
                collect(DISTINCT d.name) AS directors,
                collect(DISTINCT a.name)[0..5] AS actors
            """,
            id=movie_id
        )

        record = result.single()

        if record:
            print("\n--- Film Detayları ---")
            print("İsim:", record["title"])
            print("Yıl:", record["year"])

            print("Yönetmen(ler):")
            for d in record["directors"]:
                print("-", d)

            print("Oyuncular:")
            for a in record["actors"]:
                print("-", a)


# JSON dosyaysi yapan fonksiyon
def export_graph(movie_id):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (m:Movie)
            WHERE elementId(m) = $id

            OPTIONAL MATCH (d:Director)-[:DIRECTED]->(m)
            OPTIONAL MATCH (a:Actor)-[:ACTED_IN]->(m)

            RETURN 
                m.title AS title,
                m.released AS year,
                collect(DISTINCT d.name) AS directors,
                collect(DISTINCT a.name)[0..5] AS actors
            """,
            id=movie_id
        )

        record = result.single()

        graph_data = {
            "movie": {
                "title": record["title"],
                "year": record["year"],
                "directors": record["directors"],
                "actors": record["actors"]
            }
        }

        with open("exports/graph.json", "w", encoding="utf-8") as f:
            json.dump(graph_data, f, indent=4, ensure_ascii=False)

        print("exports/graph.json oluşturuldu.")

# Ana Fonksiyon #
def main_menu():
    while True:
        print("\n--- Film Menüsü ---")
        print("1. Film Ara")
        print("2. Çıkış")

        choice = input("Seç: ")

        if choice == "1":

            selected = search_movie()

            if selected:
                movie_id = selected[0]
                show_movie_details(movie_id)
                export_graph(movie_id)


        elif choice == "2":

            confirm = input("Çıkmak İstediğinizden Emin misiniz? (e/h): ").lower()
            if confirm == "e":

                print("Bye 👋")
                break

            elif confirm == "h" :
                print("Çıkış İptal Edildi")

            else :
                print("Geçersiz Seçim")

        else:
            print("Geçersiz Seçim")

main_menu()























