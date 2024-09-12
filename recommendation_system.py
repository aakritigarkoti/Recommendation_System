import pandas as pd
import tkinter as tk
from tkinter import scrolledtext, font, ttk
from tkinter import messagebox
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load the data
try:
    # Load the movies dataset
    movies = pd.read_csv("C:/Users/hp/PycharmProjects/pythonProject2/HollywoodMovies.csv")

    # Add the movieId column if it doesn't exist
    if 'movieId' not in movies.columns:
        movies['movieId'] = range(1, len(movies) + 1)
        # Save the updated DataFrame back to the CSV file
        movies.to_csv("C:/Users/hp/PycharmProjects/pythonProject2/HollywoodMovies.csv", index=False)

    # Load the Hindi movies dataset
    hindi_movies = pd.read_csv("C:/Users/hp/PycharmProjects/pythonProject2/IMDB-Movie-Dataset(2023-1951).csv",
                               encoding='ISO-8859-1')

except Exception as e:
    print(f"Error loading data: {e}")
    exit()

# Ensure the hindi_movies dataset has the 'language' column
hindi_movies['language'] = 'Hindi'

# Append Hindi movies to the existing movies dataset
movies = pd.concat([movies, hindi_movies], ignore_index=True)

# Ensure the 'language' column exists in the combined dataset
if 'language' not in movies.columns:
    movies['language'] = 'English'  # Assign default value if column is missing

# For demonstration purposes, just printing the columns of the movies DataFrame
print("Columns in the movies dataset:", movies.columns)


# Uncomment and define 'ratings' DataFrame if available
# For demonstration, assuming 'ratings' DataFrame is defined elsewhere
# ratings = pd.read_csv('path_to_ratings_csv')  # Update path as needed
# data = pd.merge(ratings, movies, on='movieId')

# Uncomment and define 'user_movie_matrix' if 'ratings' DataFrame is defined
# user_movie_matrix = data.pivot_table(index='userId', columns='title', values='rating').fillna(0)
# user_similarity = cosine_similarity(user_movie_matrix)
# user_similarity_df = pd.DataFrame(user_similarity, index=user_movie_matrix.index, columns=user_movie_matrix.index)

# Define functions for recommendations and GUI setup
def recommend_movies_by_mood(language, genre, mood=None):
    print(f"Language: {language}, Genre: {genre}, Mood: {mood}")  # Debugging

    if language == "Hindi":
        # Filter Hindi movies
        filtered_movies = movies[
            (movies['Genre'].str.contains(genre, case=False, na=False)) &
            (movies['language'] == "Hindi")
            ]
        print(f"Filtered Movies (Hindi): {filtered_movies.shape[0]} found")  # Debugging

        if filtered_movies.empty:
            messagebox.showerror("No Movies Found", "No Hindi movies found with the selected genre.")
            return

    elif language == "English":
        # Filter English movies
        filtered_movies = movies[
            (movies['Genre'].str.contains(genre, case=False, na=False)) &
            (movies['language'] != "Hindi")
            ]
        print(f"Filtered Movies (English): {filtered_movies.shape[0]} found")  # Debugging

        if mood:
            # Apply mood filter using the mood mapping
            filtered_movies['moods'] = filtered_movies['Genre'].apply(assign_mood_for_non_hindi)
            filtered_movies = filtered_movies[filtered_movies['moods'].str.contains(mood, case=False, na=False)]
            print(f"Filtered Movies after Mood (English): {filtered_movies.shape[0]} found")  # Debugging

        if filtered_movies.empty:
            messagebox.showerror("No Movies Found", "No English movies found with the selected genre and mood.")
            return

    else:
        messagebox.showerror("Error", "Please select a valid language.")
        return

    recommendations = filtered_movies['title'].head(5)

    # Insert user's query into chat
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: Language - {language}, Genre - {genre}, Mood - {mood}\n", "user_input")

    # Insert system's response in different colors for each line
    chat_display.insert(tk.END, "System: Recommended Movies based on your input:\n", "output_blue")
    for index, movie in enumerate(recommendations):
        color_tag = "output_green" if index % 2 == 0 else "output_purple"
        chat_display.insert(tk.END, movie + "\n", color_tag)

    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)


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
    return "Neutral"  # Default mood if no genre matches


def on_theme_select(event):
    selected_theme = theme_combobox.get()
    if selected_theme == "Dark":
        root.tk_setPalette(background='#2E2E2E', foreground='#FFFFFF')
        chat_display.config(bg='#2E2E2E', fg='#FFFFFF', font=chat_font)
        genre_label.config(bg='#2E2E2E', fg='#FFFFFF', font=label_font)
        mood_label.config(bg='#2E2E2E', fg='#FFFFFF', font=label_font)
        language_label.config(bg='#2E2E2E', fg='#FFFFFF', font=label_font)
        genre_combobox.config(font=entry_font, foreground='black', background='#4E4E4E')
        mood_combobox.config(font=entry_font, foreground='black', background='#4E4E4E')
        language_combobox.config(font=entry_font, foreground='black', background='#4E4E4E')
        submit_button.config(bg='#555555', fg='#FFFFFF', font=button_font)
        close_button.config(bg='#FF0000', fg='#FFFFFF')
        minimize_button.config(bg='#DDDDDD', fg='#000000')
    else:
        root.tk_setPalette(background='#FFFFFF', foreground='#000000')
        chat_display.config(bg='#FFFFFF', fg='#000000', font=chat_font)
        genre_label.config(bg='#FFFFFF', fg='#000000', font=label_font)
        mood_label.config(bg='#FFFFFF', fg='#000000', font=label_font)
        language_label.config(bg='#FFFFFF', fg='#000000', font=label_font)
        genre_combobox.config(font=entry_font, foreground='black', background='#FFFFFF')
        mood_combobox.config(font=entry_font, foreground='black', background='#FFFFFF')
        language_combobox.config(font=entry_font, foreground='black', background='#FFFFFF')
        submit_button.config(bg='#FFFFFF', fg='#000000', font=button_font)
        close_button.config(bg='#FFFFFF', fg='#000000')
        minimize_button.config(bg='#FFFFFF', fg='#000000')


# Create the GUI application
root = tk.Tk()
root.title("Movie Recommendation System")

# Configure fonts
chat_font = font.Font(family="Helvetica", size=12)
label_font = font.Font(family="Helvetica", size=10, weight="bold")
entry_font = font.Font(family="Helvetica", size=10)
button_font = font.Font(family="Helvetica", size=10, weight="bold")

# Set up chat display
chat_display = scrolledtext.ScrolledText(root, height=20, width=60, wrap=tk.WORD, state=tk.DISABLED)
chat_display.tag_configure("user_input", foreground="blue", font=chat_font)
chat_display.tag_configure("output_blue", foreground="black", font=chat_font)
chat_display.tag_configure("output_green", foreground="green", font=chat_font)
chat_display.tag_configure("output_purple", foreground="purple", font=chat_font)
chat_display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Set up genre selection
genre_label = tk.Label(root, text="Genre:", font=label_font)
genre_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
genre_combobox = ttk.Combobox(root, values=['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Thriller'],
                              font=entry_font)
genre_combobox.grid(row=1, column=1, padx=5, pady=5)

# Set up mood selection
mood_label = tk.Label(root, text="Mood:", font=label_font)
mood_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
mood_combobox = ttk.Combobox(root, values=['Excited', 'Happy', 'Calm', 'Scared', 'Romantic', 'Adventurous'],
                             font=entry_font)
mood_combobox.grid(row=2, column=1, padx=5, pady=5)

# Set up language selection
language_label = tk.Label(root, text="Language:", font=label_font)
language_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
language_combobox = ttk.Combobox(root, values=['Hindi', 'English'], font=entry_font)
language_combobox.grid(row=3, column=1, padx=5, pady=5)

# Set up submit button
submit_button = tk.Button(root, text="Submit",
                          command=lambda: recommend_movies_by_mood(language_combobox.get(), genre_combobox.get(),
                                                                   mood_combobox.get()), font=button_font)
submit_button.grid(row=4, column=1, padx=5, pady=10)

# Set up close and minimize buttons
close_button = tk.Button(root, text="Close", command=root.quit, bg='#FF0000', fg='#FFFFFF', font=button_font)
close_button.grid(row=5, column=0, padx=5, pady=10)

minimize_button = tk.Button(root, text="Minimize", command=root.iconify, bg='#DDDDDD', fg='#000000', font=button_font)
minimize_button.grid(row=5, column=2, padx=5, pady=10)

# Add theme selection
theme_combobox = ttk.Combobox(root, values=["Light", "Dark"], font=entry_font)
theme_combobox.grid(row=6, column=1, padx=5, pady=5)
theme_combobox.bind("<<ComboboxSelected>>", on_theme_select)

root.mainloop()
