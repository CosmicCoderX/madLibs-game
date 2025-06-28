import textwrap
import tkinter as tk
from tkinter import messagebox, ttk
import pyttsx3
import emoji
import random
from playsound import playsound
import os
import time
import threading
import json
import re
from datetime import datetime

# === TTS Setup ===
engine = pyttsx3.init()
engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id if len(voices) > 1 else voices[0].id)

# === Global Variables ===
story_count = 0
saved_stories = []
current_theme = "Funny"

def speak(text):
    try:
        engine.stop()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Voice error:", e)

def clean_text_for_speech(text):
    """Remove emojis, excessive formatting, and clean text for better TTS"""
    # Remove emojis
    text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)
    
    # Remove excessive formatting like multiple dashes or equals
    text = re.sub(r'[=\-]{3,}', '', text)
    
    # Remove titles in all caps with special formatting
    text = re.sub(r'🎪.*?🎪|🤪.*?🤪|🌙.*?🌙|🕷️.*?🕷️|🚀.*?🚀|🛸.*?🛸|💖.*?💖|🌹.*?🌹', '', text)
    
    # Clean up multiple spaces and newlines
    text = re.sub(r'\n+', '. ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Remove hashtags and social media references that don't sound good when spoken
    text = re.sub(r'#\w+', '', text)
    
    # Replace some text-speak with speakable versions
    text = text.replace('WiFi', 'Wi-Fi')
    text = text.replace('TikTok', 'Tick Tock')
    text = text.replace('Netflix', 'Netflix')
    
    return text.strip()

# Sound file paths
SOUND_PATHS = {
    "general": {
        "drumroll": "sounds/general/drumroll.mp3",
        "tada": "sounds/general/tada.mp3", 
        "bye": "sounds/general/bye.mp3",
        "startup": "sounds/general/startup.mp3",
        "button_click": "sounds/general/button_click.mp3",
        "error": "sounds/general/error.mp3"
    },
    "themes": {
        "Funny": [
            "sounds/themes/funny/laugh.mp3",
            "sounds/themes/funny/comedy.mp3",
            "sounds/themes/funny/giggle.mp3",
        ],
        "Spooky": [
            "sounds/themes/spooky/spooky.mp3",
            "sounds/themes/spooky/creepy.mp3",
            "sounds/themes/spooky/thunder.mp3"
        ],
        "Sci-Fi": [
            "sounds/themes/scifi/computer.mp3",
            "sounds/themes/scifi/teleport.mp3"
        ],
        "Romantic": [
            "sounds/themes/romantic/whistle.mp3",
            "sounds/themes/romantic/soft_music.mp3",
        ]
    },
    "actions": {
        "surprise_me": "sounds/actions/surprise_me.mp3",
        "generate_story": "sounds/actions/generate_story.mp3",
        "theme_change": "sounds/actions/theme_change.mp3"
    }
}

def play_sound(sound_key, category="general"):
    """Enhanced sound playing function with organized structure"""
    try:
        if category == "themes":
            # For themes, pick a random sound from the list
            theme = current_theme
            if theme in SOUND_PATHS["themes"]:
                sound_file = random.choice(SOUND_PATHS["themes"][theme])
            else:
                return
        else:
            # For general and action sounds
            if sound_key in SOUND_PATHS[category]:
                sound_file = SOUND_PATHS[category][sound_key]
            else:
                return
        
        if os.path.exists(sound_file):
            playsound(sound_file)
        else:
            print(f"⚠️ Sound file not found: {sound_file}")
    except Exception as e:
        print(f"⚠️ Sound error: {e}")

def play_theme_sound():
    """Play a random sound for the current theme"""
    play_sound("", "themes")

def play_action_sound(action):
    """Play sound for specific actions"""
    play_sound(action, "actions")

# === Theme Configurations ===
THEMES = {
    "Funny": {
        "bg": "#fff5b7",
        "accent": "#ffeb3b",
        "button": "#ff9800",
        "text": "#333333",
        "emoji": "😂",
        "font": ("Comic Sans MS", 12),
        "sounds": ["laugh.mp3", "comedy.mp3", "giggle.mp3"]
    },
    "Spooky": {
        "bg": "#2a1810",
        "accent": "#8b0000",
        "button": "#ff4444",
        "text": "#ffffff",
        "emoji": "👻",
        "font": ("Chiller", 12),
        "sounds": ["spooky.mp3", "creepy.mp3", "thunder.mp3"]
    },
    "Sci-Fi": {
        "bg": "#0d1b2a",
        "accent": "#00ffff",
        "button": "#7209b7",
        "text": "#00ff00",
        "emoji": "🛸",
        "font": ("Courier New", 12),
        "sounds": ["computer.mp3", "teleport.mp3"]
    },
    "Romantic": {
        "bg": "#fce4ec",
        "accent": "#e91e63",
        "button": "#ff69b4",
        "text": "#880e4f",
        "emoji": "💕",
        "font": ("Brush Script MT", 12),
        "sounds": ["whistle.mp3", "soft_music.mp3"]
    }
}

# === Silly Word Suggestions ===
SILLY_SUGGESTIONS = {
    "place": ["Timbuktu", "Your Bathroom", "McDonald's", "Mars", "Under Your Bed", "Netflix Headquarters"],
    "adjective": ["Wiggly", "Stinky", "Magnificent", "Ridiculous", "Sneaky", "Legendary"],
    "noun": ["Pickle", "Unicorn", "Toothbrush", "Dinosaur", "Pizza Slice", "Rubber Duck"],
    "verb": ["Danced", "Burped", "Teleported", "Giggled", "Snorted", "Wobbled"],
    "adverb": ["Awkwardly", "Majestically", "Suspiciously", "Dramatically", "Frantically", "Sleepily"],
    "name": ["Captain Cheese", "Sir Snuggles", "Princess Pickles", "Doctor Giggles", "Master Muffin"]
}

# === Enhanced Story Templates ===
def generate_story(inputs, theme):
    funny_templates = [
        textwrap.dedent(f"""
            🎪 THE GREAT {inputs['place'].upper()} ADVENTURE! 🎪
            
            Once upon a time in {inputs['place']}, there lived a {inputs['adjective']} {inputs['noun']} named Kevin.
            Kevin {inputs['verb']} {inputs['adverb']} every morning at 6 AM sharp, much to the horror of local pigeons.
            
            One day, {inputs['name']} witnessed this spectacle and thought, "This is either genius or I need glasses."
            The {inputs['noun']} then started a YouTube channel called "Kevin's {inputs['adjective']} Adventures" 
            and became an overnight sensation with 50 million subscribers!
            
            The moral of the story: Never underestimate a {inputs['adjective']} {inputs['noun']} with WiFi access! 📱✨
        """),
        
        textwrap.dedent(f"""
            🤪 BREAKING NEWS FROM {inputs['place'].upper()}! 🤪
            
            Local resident {inputs['name']} reported seeing a {inputs['adjective']} {inputs['noun']} that could {inputs['verb']} {inputs['adverb']}.
            "I was just minding my own business," said {inputs['name']}, "when this thing started performing better than TikTok dancers!"
            
            The {inputs['noun']} has since been offered a Bollywood contract, a Netflix series, and its own brand of energy drinks.
            Scientists are baffled, tourists are flocking, and the {inputs['noun']} is trending on Twitter with #RelateableMood.
            
            In other news, local chai vendors report a 500% increase in sales. Coincidence? We think not! ☕️🎬
        """),
    ]

    spooky_templates = [
        textwrap.dedent(f"""
            🌙 THE HAUNTING OF {inputs['place'].upper()} 🌙
            
            It was a dark and stormy night in {inputs['place']}... (Yes, we're starting with that cliché!)
            The wind howled as a {inputs['adjective']} {inputs['noun']} began to {inputs['verb']} {inputs['adverb']} near the old cemetery.
            
            {inputs['name']} was walking home from late-night pizza delivery when they spotted the creature.
            "Well, this is either a ghost or I've been working too many night shifts," muttered {inputs['name']}.
            
            The {inputs['noun']} turned around, looked {inputs['name']} dead in the eye, and said:
            "Do you have WiFi password? Even spirits need internet these days!" 👻📱
            
            And that's how {inputs['name']} became the first person to give WiFi access to a supernatural being.
        """),
        
        textwrap.dedent(f"""
            🕷️ THE CURSE OF THE {inputs['adjective'].upper()} {inputs['noun'].upper()} 🕷️
            
            Legend says that anyone who visits {inputs['place']} will encounter the mysterious {inputs['adjective']} {inputs['noun']}.
            It appears at midnight, {inputs['verb']}s {inputs['adverb']}, and grants three wishes... but with a twist!
            
            When {inputs['name']} met the creature, they wished for:
            1. Unlimited pizza 🍕
            2. The ability to sleep through Monday mornings 😴
            3. For their WiFi to never lag during Netflix 📺
            
            The {inputs['noun']} granted all wishes but now {inputs['name']} can only eat pizza, 
            sleeps for 20 hours a day, and binge-watches shows forever!
            
            Be careful what you wish for... especially from {inputs['adjective']} {inputs['noun']}s! 🎭
        """),
    ]

    scifi_templates = [
        textwrap.dedent(f"""
            🚀 GALACTIC REPORT: YEAR 3025 🚀
            
            Commander {inputs['name']} was patrolling the space sector near {inputs['place']} when sensors detected
            an unidentified {inputs['adjective']} {inputs['noun']} that could {inputs['verb']} {inputs['adverb']} through hyperspace!
            
            "This is either first contact or my coffee machine is malfunctioning again," reported {inputs['name']}.
            
            The alien {inputs['noun']} communicated using memes and offered to trade advanced technology 
            for Earth's supply of pizza and cat videos. 
            
            Peace negotiations are ongoing. Humanity's greatest diplomats (pizza delivery drivers) 
            have been dispatched to finalize the treaty! 🍕👽
            
            UPDATE: The {inputs['noun']} has opened an intergalactic food truck. Reviews are stellar! ⭐⭐⭐⭐⭐
        """),
        
        textwrap.dedent(f"""
            🛸 SPACE STATION {inputs['place'].upper()}: MISSION LOG 🛸
            
            Day 347: Our AI assistant has evolved into a {inputs['adjective']} {inputs['noun']} that insists on 
            {inputs['verb']}ing {inputs['adverb']} through the corridors while playing 80s music.
            
            Chief Engineer {inputs['name']} tried to reprogram it, but the {inputs['noun']} just laughed and 
            started streaming cooking shows to every screen on the station.
            
            The crew has given up fighting it. We now have the most entertaining AI in the galaxy!
            It tells jokes, orders supplies, and somehow makes the best digital pancakes we've ever tasted.
            
            Mission Status: Successfully weird. Morale: Surprisingly high! 🥞🤖
        """),
    ]

    romantic_templates = [
        textwrap.dedent(f"""
            💖 LOVE STORY: {inputs['place'].upper()} EDITION 💖
            
            In the charming streets of {inputs['place']}, {inputs['name']} was having another ordinary day
            until they spotted a {inputs['adjective']} {inputs['noun']} that could {inputs['verb']} {inputs['adverb']}.
            
            "Is this love at first sight or did I forget my glasses again?" wondered {inputs['name']}.
            
            The {inputs['noun']} approached with a bouquet of... wait for it... French fries! 🍟
            They shared deep conversations about life, dreams, and whether pineapple belongs on pizza.
            
            Six months later, they're still together, running a food blog called 
            "{inputs['adjective']} Love and {inputs['noun']} Recipes" with 2 million followers!
            
            True love finds a way... especially when it involves food! 💕🍽️
        """),
        
        textwrap.dedent(f"""
            🌹 THE {inputs['place'].upper()} ROMANCE 🌹
            
            {inputs['name']} was scrolling through dating apps when a {inputs['adjective']} {inputs['noun']} 
            literally {inputs['verb']}ed {inputs['adverb']} into their life!
            
            "Well, this is either destiny or the universe has a weird sense of humor," thought {inputs['name']}.
            
            Their first date was at a café where the {inputs['noun']} ordered everything on the menu
            and somehow managed to pay with interpretive dance.
            
            Now they live together in {inputs['place']}, host a podcast called "Love is {inputs['adjective']}",
            and their relationship advice has helped thousands of couples worldwide!
            
            Sometimes the best love stories are the ones you never see coming! 💝📻
        """),
    ]

    all_templates = {
        "Funny": funny_templates,
        "Spooky": spooky_templates,
        "Sci-Fi": scifi_templates,
        "Romantic": romantic_templates,
    }

    return random.choice(all_templates[theme]).strip()

# === New Features ===
def get_random_suggestion(field):
    return random.choice(SILLY_SUGGESTIONS[field])

def surprise_me():
    """Fill all fields with random silly words"""
    place_var.set(get_random_suggestion("place"))
    adj_var.set(get_random_suggestion("adjective"))
    noun_var.set(get_random_suggestion("noun"))
    verb_var.set(get_random_suggestion("verb"))
    adv_var.set(get_random_suggestion("adverb"))
    name_var.set(get_random_suggestion("name"))
    
    play_action_sound("surprise_me")
    messagebox.showinfo("Surprise!", "🎲 Random words loaded! Prepare for chaos! 🎲")
    speak("Surprise! I've filled everything with wonderfully ridiculous words!")

def save_story():
    """Save the current story"""
    global story_count, saved_stories
    current_story = story_output.get("1.0", tk.END).strip()
    if current_story:
        story_count += 1
        story_data = {
            "id": story_count,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "theme": current_theme,
            "story": current_story
        }
        saved_stories.append(story_data)
        
        # Save to file
        try:
            with open("saved_stories.json", "w") as f:
                json.dump(saved_stories, f, indent=2)
            play_action_sound("save_story")
            messagebox.showinfo("Saved!", f"📚 Story #{story_count} saved successfully!")
            speak(f"Story number {story_count} has been saved to your collection!")
        except Exception as e:
            play_sound("error")
            messagebox.showerror("Error", f"Could not save story: {e}")

def view_saved_stories():
    """View all saved stories"""
    if not saved_stories:
        messagebox.showinfo("No Stories", "📭 No saved stories yet! Create some masterpieces first!")
        return
    
    play_action_sound("load_story")
    
    # Create a new window to display saved stories
    stories_window = tk.Toplevel(root)
    stories_window.title("📚 Saved Stories")
    stories_window.geometry("700x500")
    stories_window.config(bg=THEMES[current_theme]["bg"])
    
    # Create scrollable text widget
    stories_text = tk.Text(stories_window, font=("Arial", 10), wrap="word")
    scrollbar = tk.Scrollbar(stories_window, orient="vertical", command=stories_text.yview)
    stories_text.configure(yscrollcommand=scrollbar.set)
    
    # Display all stories
    for story in saved_stories:
        stories_text.insert(tk.END, f"📖 Story #{story['id']} - {story['theme']} ({story['timestamp']})\n")
        stories_text.insert(tk.END, "="*50 + "\n")
        stories_text.insert(tk.END, story['story'] + "\n\n")
    
    stories_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")
    stories_text.config(state="disabled")

def apply_theme():
    """Apply the selected theme to the entire GUI"""
    global current_theme
    current_theme = theme_var.get()
    theme_config = THEMES[current_theme]
    
    # Update root window
    root.config(bg=theme_config["bg"])
    
    # Update all frames
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.config(bg=theme_config["bg"])
            for child in widget.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(bg=theme_config["bg"])
                elif isinstance(child, tk.Label):
                    child.config(bg=theme_config["bg"], fg=theme_config["text"], font=theme_config["font"])
                elif isinstance(child, tk.Button):
                    child.config(bg=theme_config["button"], fg="white", font=theme_config["font"])
        elif isinstance(widget, tk.Label):
            widget.config(bg=theme_config["bg"], fg=theme_config["text"], font=theme_config["font"])
        elif isinstance(widget, tk.Button):
            widget.config(bg=theme_config["button"], fg="white", font=theme_config["font"])
    
    # Update the title with theme emoji
    title_label.config(text=f"{theme_config['emoji']} Mad Libs Story Generator {theme_config['emoji']}")
    
    play_action_sound("theme_change")
    speak(f"Theme changed to {current_theme}! Looking {get_random_suggestion('adjective')}!")

# === Story Execution ===
def run_story_thread(inputs, theme, output_widget):
    global story_count
    story = generate_story(inputs, theme)
    output_widget.config(state="normal")
    output_widget.delete("1.0", tk.END)
    output_widget.insert(tk.END, story)
    output_widget.config(state="disabled")

    play_sound("drumroll")
    speak(f"Here comes your {theme} story! Get ready to laugh, cry, or question reality!")
    time.sleep(0.4)
    
    # Clean the story for TTS - remove emojis and excessive formatting
    clean_story = clean_text_for_speech(story)
    speak(clean_story)
    
    # Play theme-appropriate sound
    play_theme_sound()
    
    time.sleep(0.4)
    play_sound("tada")
    
    # Ask if user wants to play again
    user_response = messagebox.askyesno("Play Again?", "🔁 Want to play another story?")
    if not user_response:
        speak(emoji.emojize("👋 ", language="alias") + "Okay! See you next time!")
        play_sound("bye")
        root.quit()

def start_story():
    inputs = {
        "place": place_var.get(),
        "adjective": adj_var.get(),
        "noun": noun_var.get(),
        "verb": verb_var.get(),
        "adverb": adv_var.get(),
        "name": name_var.get(),
    }

    if not all(inputs.values()):
        messagebox.showwarning("Missing Info", "Please fill all the fields! Or use 'Surprise Me!' for instant chaos! 🎲")
        speak("Oops! You forgot to fill some fields. Use the surprise me button if you're feeling adventurous!")
        return

    theme = theme_var.get()
    threading.Thread(target=run_story_thread, args=(inputs, theme, story_output)).start()

# === GUI Setup ===
root = tk.Tk()
root.title("🎭 Mad Libs Story Generator")
root.geometry("750x700")
root.config(bg="#fffbe6")

# Title
title_label = tk.Label(root, text="🎭 Mad Libs Story Generator 🎭", font=("Arial", 18, "bold"), bg="#fffbe6")
title_label.pack(pady=10)

# Input frame
input_frame = tk.Frame(root, bg="#fffbe6")
input_frame.pack(pady=5)

def add_input(label, var, field_name):
    row = tk.Frame(input_frame, bg="#fffbe6")
    tk.Label(row, text=label, width=12, anchor="w", font=("Arial", 12), bg="#fffbe6").pack(side=tk.LEFT)
    entry = tk.Entry(row, textvariable=var, font=("Arial", 12), width=25)
    entry.pack(side=tk.LEFT, padx=5)
    
    # Add suggestion button for each field
    suggestion_btn = tk.Button(row, text="💡", command=lambda: var.set(get_random_suggestion(field_name)), 
                             font=("Arial", 10), width=3, bg="#ffeb3b")
    suggestion_btn.pack(side=tk.LEFT, padx=2)
    row.pack(pady=3)

place_var = tk.StringVar()
adj_var = tk.StringVar()
noun_var = tk.StringVar()
verb_var = tk.StringVar()
adv_var = tk.StringVar()
name_var = tk.StringVar()
theme_var = tk.StringVar(value="Funny")

add_input("Place:", place_var, "place")
add_input("Adjective:", adj_var, "adjective")
add_input("Noun:", noun_var, "noun")
add_input("Verb:", verb_var, "verb")
add_input("Adverb:", adv_var, "adverb")
add_input("Name:", name_var, "name")

# Theme selection and controls
control_frame = tk.Frame(root, bg="#fffbe6")
control_frame.pack(pady=10)

tk.Label(control_frame, text="Select Theme:", font=("Arial", 12), bg="#fffbe6").pack(side=tk.LEFT, padx=5)
theme_menu = tk.OptionMenu(control_frame, theme_var, "Funny", "Spooky", "Sci-Fi", "Romantic", command=lambda x: apply_theme())
theme_menu.pack(side=tk.LEFT, padx=5)

# Fun buttons
button_frame = tk.Frame(root, bg="#fffbe6")
button_frame.pack(pady=10)

tk.Button(button_frame, text="🎲 Surprise Me!", command=surprise_me, font=("Arial", 12, "bold"), 
          bg="#ff9800", fg="white", padx=10).pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="📝 Generate Story", command=start_story, font=("Arial", 14, "bold"), 
          bg="#4caf50", fg="white", padx=15).pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="💾 Save Story", command=save_story, font=("Arial", 12), 
          bg="#2196f3", fg="white", padx=10).pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="📚 View Saved", command=view_saved_stories, font=("Arial", 12), 
          bg="#9c27b0", fg="white", padx=10).pack(side=tk.LEFT, padx=5)

# Output section
tk.Label(root, text="📖 Your Hilarious Story", font=("Arial", 14, "bold"), bg="#fffbe6").pack(pady=(20,5))

story_output = tk.Text(root, font=("Arial", 11), height=12, wrap="word", state="disabled", 
                      bg="#ffffff", relief="sunken", borderwidth=2)
story_output.pack(padx=20, pady=10, fill="both", expand=True)

# Status bar
status_frame = tk.Frame(root, bg="#fffbe6")
status_frame.pack(fill="x", side="bottom")
status_label = tk.Label(status_frame, text="🎭 Ready to create some comedy gold! Click 'Surprise Me!' for instant fun!", 
                       font=("Arial", 10), bg="#fffbe6", fg="#666666")
status_label.pack(pady=5)

# Load saved stories on startup
try:
    with open("saved_stories.json", "r") as f:
        saved_stories = json.load(f)
        story_count = len(saved_stories)
except FileNotFoundError:
    saved_stories = []
    story_count = 0

# Apply initial theme
apply_theme()

# Welcome message
speak("Welcome to the most ridiculously fun Mad Libs generator! Fill in the words or click surprise me for instant chaos!")

root.mainloop()