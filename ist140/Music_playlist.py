# 1. Initialize a playlist array with just song titles
playlist = ["Blinding Lights", "Levitating", "Sunflower"]

# 2. Add 3 new songs to the original list
for i in range(3):
    new_songs = input("Enter a new song to add: ")
    playlist.append(new_songs)

# 3. Use the insert function to Insert another song at the beginning of the list
# playlist.
first_song = input("Enter a song to insert at the beginning: ")
playlist.insert(0, first_song)

# 4. Check if the list has more than 2 songs in it. If it does 
#remove the second song in the list. (about 3 lines of code here)
if len(playlist) > 2:
    removed_song = playlist.pop(1)
    print(f"Removed the second song: {removed_song}")

# 5. View the final version of the playlist & also print out the number of songs
print("My playlist:", playlist)
print("# of songs:", len(playlist))

# 6. Sort the playlist and print again
# playlist.
playlist.sort()
print("Sorted playlist:", playlist)
