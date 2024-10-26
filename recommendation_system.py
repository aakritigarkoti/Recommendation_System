import sys
import pandas as pd
import tkinter as tk
from tkinter import scrolledtext, font, ttk
from tkinter import messagebox
import random

# Function to ensure unique column names
def make_unique(columns):
    seen = set()
    result = []
    for column in columns:
        new_column = column
        counter = 1
        while new_column in seen:
            new_column = f"{column}_{counter}"
            counter += 1
        seen.add(new_column)
        result.append(new_column)
    return result

# Load data
try:
    movies = pd.read_csv("C:\\Users\\hp\\PycharmProjects\\pythonProject2\\HollywoodMovies.csv")
    movies.columns = make_unique(movies.columns)
    if 'movieid' not in movies.columns:
        movies['movieid'] = range(1, len(movies) + 1)
        movies.to_csv("C:\\Users\\hp\\PycharmProjects\\pythonProject2\\HollywoodMovies_with_movieId.csv", index=False)
    hindi_movies = pd.read_csv("C:\\Users\\hp\\PycharmProjects\\pythonProject2\\IMDB-Movie-Dataset(2023-1951).csv", encoding='ISO-8859-1')
except Exception as e:
    print(f"Error loading data: {e}")
    sys.exit()

movies.columns = movies.columns.str.strip().str.lower()
hindi_movies.columns = hindi_movies.columns.str.strip().str.lower()
hindi_movies['language'] = 'Hindi'
movies['language'] = 'English'
common_columns = ['title', 'genre', 'year', 'language']
hindi_movies = hindi_movies[common_columns]
movies = movies[common_columns]
hindi_movies.reset_index(drop=True, inplace=True)
movies.reset_index(drop=True, inplace=True)

try:
    combined_movies = pd.concat([movies, hindi_movies], ignore_index=True)
except Exception as e:
    print(f"Error combining datasets: {e}")
    sys.exit()

# Assign mood based on genre
def assign_mood_for_non_hindi(genres):
    mood_map = {
        'Action': 'Excited',
        'Comedy': 'Happy',
        'Drama': 'Calm',
        'Horror': 'Scared',
        'Romance': 'Romantic',
        'Thriller': 'Adventurous'
    }
    for genre in mood_map:
        if genre in genres:
            return mood_map[genre]
    return "Neutral"

# Recommend movies based on mood and genre
def recommend_movies_by_mood(language, genre, mood=None):
    if language == "Hindi":
        filtered_movies = combined_movies[(combined_movies['genre'].str.contains(genre, case=False, na=False)) &
                                          (combined_movies['language'] == "Hindi")]
        if filtered_movies.empty:
            messagebox.showerror("No Movies Found", "No Hindi movies found with the selected genre.")
            return
    elif language == "English":
        filtered_movies = combined_movies[(combined_movies['genre'].str.contains(genre, case=False, na=False)) &
                                          (combined_movies['language'] != "Hindi")]
        if mood:
            filtered_movies = filtered_movies.copy()
            filtered_movies['moods'] = filtered_movies['genre'].apply(assign_mood_for_non_hindi)
            filtered_movies = filtered_movies[filtered_movies['moods'].str.contains(mood, case=False, na=False)]
        if filtered_movies.empty:
            messagebox.showerror("No Movies Found", "No English movies found with the selected genre and mood.")
            return
    else:
        messagebox.showerror("Error", "Please select a valid language.")
        return

    mood_comments = {
        'Excited': ["Get ready for some action!", "You're in for a thrilling experience!"],
        'Happy': ["Enjoy some light-hearted fun!", "Time to laugh and relax!"],
        'Calm': ["Relax with these calm stories.", "Find your peace with these movies."],
        'Scared': ["Get ready for a scare!", "These movies will keep you on the edge of your seat!"],
        'Romantic': ["Love is in the air!", "These romantic tales will warm your heart."],
        'Adventurous': ["Prepare for an adventure!", "These movies will take you on a wild ride!"]
    }
    comment = random.choice(mood_comments.get(mood, ["Here are some great movies for you!"]))

    recommendations = filtered_movies['title'].head(5) if 'title' in filtered_movies.columns else []

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: Language - {language}, Genre - {genre}, Mood - {mood}\n", "user_input")
    chat_display.insert(tk.END, f"System: {comment}\n", "output_blue")
    chat_display.insert(tk.END, "System: Recommended Movies based on your input:\n", "output_blue")
    for index, movie in enumerate(recommendations):
        color_tag = "output_green" if index % 2 == 0 else "output_purple"
        chat_display.insert(tk.END, movie + "\n", color_tag)
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

# Theme selection function
def on_theme_select(event):
    selected_theme = theme_combobox.get()
    if selected_theme == "Dark":
        root.tk_setPalette(background='#2E2E2E', foreground='#FFFFFF')
        chat_display.config(bg='#2E2E2E', fg='#FFFFFF')
    else:
        root.tk_setPalette(background='#FFFFFF', foreground='#000000')
        chat_display.config(bg='#FFFFFF', fg='#000000')

# Create the GUI application
root = tk.Tk()
root.title("Movie Recommendation System")

# Fullscreen setup
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
chat_display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

# Set color tags
chat_display.tag_config("user_input", foreground="blue", font=("Helvetica", 12, "bold"))
chat_display.tag_config("output_blue", foreground="cyan", font=("Helvetica", 12))
chat_display.tag_config("output_green", foreground="green", font=("Helvetica", 12))
chat_display.tag_config("output_purple", foreground="purple", font=("Helvetica", 12))

# Add Language and Genre dropdowns
language_label = tk.Label(root, text="Select Language:")
language_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
language_combobox = ttk.Combobox(root, values=["English", "Hindi"])
language_combobox.grid(row=1, column=1, padx=10, pady=5)

genre_label = tk.Label(root, text="Select Genre:")
genre_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
genre_combobox = ttk.Combobox(root, values=["Action", "Comedy", "Drama", "Horror", "Romance", "Thriller"])
genre_combobox.grid(row=2, column=1, padx=10, pady=5)

mood_label = tk.Label(root, text="Select Mood:")
mood_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
mood_combobox = ttk.Combobox(root, values=["Excited", "Happy", "Calm", "Scared", "Romantic", "Adventurous"])
mood_combobox.grid(row=3, column=1, padx=10, pady=5)

# Button for Recommendations
recommend_button = tk.Button(root, text="Get Recommendations", command=lambda: recommend_movies_by_mood(
    language_combobox.get(), genre_combobox.get(), mood_combobox.get()))
recommend_button.grid(row=4, column=0, columnspan=2, pady=10)

# Theme Selector
theme_label = tk.Label(root, text="Select Theme:")
theme_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
theme_combobox = ttk.Combobox(root, values=["Light", "Dark"])
theme_combobox.grid(row=5, column=1, padx=10, pady=5)
theme_combobox.bind("<<ComboboxSelected>>", on_theme_select)

# Run the application
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.mainloop()
