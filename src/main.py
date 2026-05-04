from modules.MusicDatabase import MusicDatabase
from modules.Music import Music

# TODO: remove below. Test purposes for now

def run(filepath=None):
    db = MusicDatabase(filepath)

    while True:
        print("\nWhat would you like to do?")
        print("1. View database")
        print("2. Add song")
        print("3. Search song")
        print("4. Quit")

        choice = input("Enter choice as 1, 2, 3, or 4: ").strip()

        if choice == "1":
            if db.data.empty:
                print("Database is empty.")
            else:
                print(db.data)


        elif choice == "2":
            while True:
                path = input("Enter file path (or 'done' to stop): ").strip()
                if path.lower() == "done":
                    break
                try:
                    title = input("Enter title (or press Enter to skip): ").strip() or None
                    artist = input("Enter artist (or press Enter to skip): ").strip() or None
                    genre = input("Enter genre (or press Enter to skip): ").strip() or None
                    year = input("Enter year (or press Enter to skip): ").strip()
                    year = int(year) if year else None
                    song = Music(path, title=title, artist=artist, genre=genre, year=year)
                    db.add_song(vars(song))
                    print(f"Added: {song.title}")
                except FileNotFoundError:
                    print(f"Error: file not found at '{path}'. Please check the path and try again.")
                except ValueError as e:
                    print(f"Error: {e}")
            save_path = input("Enter filepath to save database: ").strip()
            db.save(save_path)


        elif choice == "3":
            query = input("Enter search query: ").strip()
            field = input("Search by (title/genre/artist/all): ").strip().lower()
            try:
                results = db.search(query, field)
                if results.empty:
                    print("No matching songs found.")
                else:
                    print(results)
            except ValueError as e:
                print(f"Error: {e}")

                
        elif choice == "4":
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    filepath = input("Enter database filepath (or press Enter to start fresh): ").strip()
    run(filepath if filepath else None)

