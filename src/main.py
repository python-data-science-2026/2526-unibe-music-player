from modules.MusicDatabase import MusicDatabase
from modules.Music import Music

# TODO: remove below. Test purposes for now

def run(filepath=None):
    db = MusicDatabase(filepath)

    while True:
        print("\nWhat would you like to do?")
        print("1. View database")
        print("2. Add song")
        print("3. Quit")

        choice = input("Enter choice as 1, 2, or 3: ").strip()

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
                    song = Music(path)
                    db.add_song(vars(song))
                    print(f"Added: {song.title}")
                except ValueError as e:
                    print(f"Error: {e}")

            save_path = input("Enter filepath to save database: ").strip()
            db.save(save_path)

        elif choice == "3":
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    run("my_database.pkl")


