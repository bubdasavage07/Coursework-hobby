import random


playlist = [
    {"title": "Blinding Lights", "artist": "The Weeknd", "minutes": 3, "seconds": 20},
    {"title": "Levitating", "artist": "Dua Lipa", "minutes": 3, "seconds": 23},
    {"title": "Sunflower", "artist": "Post Malone and Swae Lee", "minutes": 2, "seconds": 38},
]


def show_menu():
    print("\nMusic Playlist")
    print("1. View playlist")
    print("2. Add song")
    print("3. Remove song")
    print("4. Search playlist")
    print("5. Shuffle playlist")
    print("6. Show total play time")
    print("7. Quit")


def format_song(song, number):
    return (
        f"{number}. {song['title']} by {song['artist']} "
        f"({song['minutes']}:{song['seconds']:02d})"
    )


def view_playlist():
    if len(playlist) == 0:
        print("Your playlist is empty.")
        return

    print("\nCurrent Playlist:")
    for index, song in enumerate(playlist, start=1):
        print(format_song(song, index))


def get_positive_int(prompt):
    while True:
        try:
            number = int(input(prompt))
            if number >= 0:
                return number
            print("Please enter a number that is 0 or greater.")
        except ValueError:
            print("Please enter a whole number.")


def get_seconds():
    while True:
        seconds = get_positive_int("Enter song seconds: ")
        if seconds <= 59:
            return seconds
        print("Seconds must be between 0 and 59.")


def add_song():
    title = input("Enter the song title: ").strip()
    artist = input("Enter the artist: ").strip()
    minutes = get_positive_int("Enter song minutes: ")
    seconds = get_seconds()

    if title == "" or artist == "":
        print("Song title and artist cannot be blank.")
        return

    if minutes == 0 and seconds == 0:
        print("Song length cannot be 0:00.")
        return

    playlist.append(
        {"title": title, "artist": artist, "minutes": minutes, "seconds": seconds}
    )
    print(f'"{title}" was added to the playlist.')


def remove_song():
    view_playlist()

    if len(playlist) == 0:
        return

    while True:
        song_number = get_positive_int("Enter the number of the song to remove: ")
        if 1 <= song_number <= len(playlist):
            removed_song = playlist.pop(song_number - 1)
            print(f'"{removed_song["title"]}" was removed from the playlist.')
            return
        print("That song number is not in the playlist.")


def search_playlist():
    search_term = input("Enter a song title or artist to search for: ").strip().lower()

    if search_term == "":
        print("Search cannot be blank.")
        return

    matches = []
    for song in playlist:
        title = song["title"].lower()
        artist = song["artist"].lower()
        if search_term in title or search_term in artist:
            matches.append(song)

    if len(matches) == 0:
        print("No matching songs were found.")
        return

    print("\nSearch Results:")
    for index, song in enumerate(matches, start=1):
        print(format_song(song, index))


def shuffle_playlist():
    if len(playlist) < 2:
        print("Add at least two songs before shuffling.")
        return

    random.shuffle(playlist)
    print("Playlist shuffled.")
    view_playlist()


def show_total_time():
    total_seconds = 0

    for song in playlist:
        total_seconds += song["minutes"] * 60 + song["seconds"]

    minutes = total_seconds // 60
    seconds = total_seconds % 60
    print(f"Total play time: {minutes}:{seconds:02d}")


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_playlist()
        elif choice == "2":
            add_song()
        elif choice == "3":
            remove_song()
        elif choice == "4":
            search_playlist()
        elif choice == "5":
            shuffle_playlist()
        elif choice == "6":
            show_total_time()
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Please choose a valid menu option.")


if __name__ == "__main__":
    main()
