import os
from modules.MusicDatabase import MusicDatabase
from modules.Music import Music
from modules.MusicPlayer import Player

# TODO: remove below. Test purposes for now

def run(filepath=None):
    db = MusicDatabase(filepath)

    while True:
        print("\nWhat would you like to do?")
        print("1. View database")
        print("2. Add song")
        print("3. Search song")
        print("4. Play song")
        print("5. Quit")

        choice = input("Enter choice as 1, 2, 3, 4, or 5: ").strip()

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
            if db.data.empty:
                print("Database is empty.")
            else:
                while True:
                    song_index = input("Enter song index to play (or 'done' to stop): ").strip()
                    if song_index.lower() == "done":
                        break
                    try:
                        song_index = int(song_index)
                        player = Player(db)
                        player.load(song_index)

                        song_skip = input("Do you want to start at a specific point in the song (format : m:s, enter to skip): ").strip().lower()
                        offset_seconds = 0
                        if song_skip != "" :
                            try:
                                minutes_str, seconds_str = song_skip.split(":")

                                minutes = int(minutes_str)
                                seconds = int(seconds_str)

                                offset_seconds = (minutes * 60) + seconds

                                print(f"Music will start at {minutes}m and {seconds}s (Total: {offset_seconds} seconds).")
                            except ValueError:
                                print("Invalid format, song will start at the beggining.")
                                offset_seconds = 0
                        player.seek(offset_seconds)
                        player.play()

                        while True:
                            print("p for pause")
                            print("r for resume")
                            print("s for stop")
                            print("f for skip forward 10s")
                            print("b for skip backward 10s")
                            print("n for next song")
                            print("q for quit")
                            print("a for amplify")

                            action = input("Enter your action: ").strip().lower()

                            if action == "p":
                                player.pause()
                            elif action == "r":
                                player.resume()
                            elif action == "s":
                                player.seek(0)
                                player.pause()
                            elif action == "f":
                                player.skip_forward()
                            elif action == "b":
                                player.skip_backward()
                            elif action == "n":
                                player.next_song()
                            elif action == "a":
                                factor = float(input("Enter amplification factor (between 0.0 and 1.0): "))
                                player.amplify(factor)
                            elif action == "q":
                                player.pause()
                                if os.path.exists("temp_amplified.wav"):
                                    os.remove("temp_amplified.wav")
                                break
                            else:
                                print("Invalid action, try again.")
                    except (ValueError, IndexError) as e:
                        print(f"Error: {e}")

        elif choice == "5":
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    filepath = input("Enter database filepath (or press Enter to start fresh): ").strip()
    run(filepath if filepath else None)

