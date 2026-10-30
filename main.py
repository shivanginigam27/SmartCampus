
import tkinter as tk
from tkinter import messagebox
from database import get_events
from recommender import recommend_events

# ---------- THEME ----------
BG = "#F4F7FF"
BLUE = "#4F6DF5"
DARK = "#202B46"
MUTED = "#78839B"
WHITE = "#FFFFFF"
BORDER = "#E5EAF5"

root = tk.Tk()
root.title("SmartCampus ✨")
root.geometry("1100x740")
root.minsize(950, 680)
root.configure(bg=BG)

# ---------- INTERESTS ----------
interests = [
    ("💻", "Technology"),
    ("🤖", "AI & ML"),
    ("🏆", "Hackathons"),
    ("🎵", "Music"),
    ("💃", "Dance"),
    ("📸", "Photography"),
    ("🎨", "Arts & Design"),
    ("💼", "Business"),
    ("⚽", "Sports"),
    ("🔬", "Science"),
    ("🌱", "Environment"),
    ("🎤", "Public Speaking")
]

selected = {}

# ---------- HEADER ----------
header = tk.Frame(root, bg=BLUE, height=100)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="✨ SmartCampus",
    font=("Arial", 25, "bold"),
    bg=BLUE,
    fg=WHITE
).pack(anchor="w", padx=28, pady=(15, 0))

tk.Label(
    header,
    text="Find your people. Discover your next campus experience.",
    font=("Arial", 11),
    bg=BLUE,
    fg="#E8ECFF"
).pack(anchor="w", padx=30, pady=(3, 0))

# ---------- MAIN LAYOUT ----------
main = tk.Frame(root, bg=BG, padx=20, pady=16)
main.pack(fill="both", expand=True)

left = tk.Frame(main, bg=WHITE, padx=16, pady=14)
left.pack(side="left", fill="y", padx=(0, 16))

tk.Label(
    left,
    text="🎯 Your Interests",
    font=("Arial", 17, "bold"),
    bg=WHITE,
    fg=DARK
).pack(anchor="w")

tk.Label(
    left,
    text="Choose what excites you",
    font=("Arial", 10),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w", pady=(4, 12))

interest_grid = tk.Frame(left, bg=WHITE)
interest_grid.pack(fill="x")

for i, (emoji, name) in enumerate(interests):
    var = tk.BooleanVar()
    selected[name] = var

    item = tk.Frame(
        interest_grid,
        bg="#F7F9FF",
        highlightbackground=BORDER,
        highlightthickness=1
    )
    item.grid(
        row=i // 2,
        column=i % 2,
        sticky="ew",
        padx=3,
        pady=4
    )

    tk.Checkbutton(
        item,
        text=f"{emoji} {name}",
        variable=var,
        bg="#F7F9FF",
        activebackground="#F7F9FF",
        fg=DARK,
        selectcolor=WHITE,
        font=("Arial", 9),
        wraplength=125,
        anchor="w",
        padx=5,
        pady=5
    ).pack(fill="x")

interest_grid.grid_columnconfigure(0, weight=1)
interest_grid.grid_columnconfigure(1, weight=1)

tk.Label(
    left,
    text="💡 Personalized just for you",
    font=("Arial", 9, "italic"),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w", pady=(12, 8))

# ---------- RIGHT SIDE ----------
right = tk.Frame(main, bg=BG)
right.pack(side="left", fill="both", expand=True)

tk.Label(
    right,
    text="Discover Events ✨",
    font=("Arial", 20, "bold"),
    bg=BG,
    fg=DARK
).pack(anchor="w")

tk.Label(
    right,
    text="Click any event to explore its details",
    font=("Arial", 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(3, 10))

results = tk.Frame(right, bg=BG)
results.pack(fill="both", expand=True)


# ---------- EVENT DETAILS WINDOW ----------
def show_event_details(event_data):
    details = tk.Toplevel(root)
    details.title("Event Details ✨")
    details.geometry("480x500")
    details.configure(bg=BG)
    details.resizable(False, False)

    details.transient(root)
    details.grab_set()

    tk.Label(
        details,
        text="🎉 Event Details",
        font=("Arial", 21, "bold"),
        bg=BLUE,
        fg=WHITE,
        pady=18
    ).pack(fill="x")

    content = tk.Frame(
        details,
        bg=WHITE,
        padx=22,
        pady=18
    )
    content.pack(fill="both", expand=True, padx=15, pady=15)

    tk.Label(
        content,
        text=event_data.get("title", "Campus Event"),
        font=("Arial", 18, "bold"),
        bg=WHITE,
        fg=DARK,
        wraplength=400,
        justify="left"
    ).pack(anchor="w", pady=(0, 12))

    date_value = event_data.get("event_date", "Date TBA")
    if date_value is None:
        date_value = "Date TBA"

    fields = [
        ("🏷️ Category", event_data.get("category", "Not specified")),
        ("📅 Date", date_value),
        ("📍 Venue", event_data.get("venue", "Venue TBA")),
        ("👥 Capacity", event_data.get("capacity", "Not specified"))
    ]

    for label, value in fields:
        tk.Label(
            content,
            text=f"{label}: {value}",
            font=("Arial", 10),
            bg=WHITE,
            fg=DARK,
            wraplength=400,
            justify="left",
            anchor="w"
        ).pack(fill="x", pady=4)

    tk.Label(
        content,
        text="📝 About this event",
        font=("Arial", 12, "bold"),
        bg=WHITE,
        fg=BLUE
    ).pack(anchor="w", pady=(12, 4))

    tk.Label(
        content,
        text=event_data.get(
            "description",
            "No description available."
        ) or "No description available.",
        font=("Arial", 10),
        bg=WHITE,
        fg="#58647C",
        wraplength=400,
        justify="left",
        anchor="w"
    ).pack(fill="x")

    if "score" in event_data:
        tk.Label(
            content,
            text=f"✨ Your match: {event_data['score']:.0%}",
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg="#168454"
        ).pack(anchor="w", pady=(10, 0))

    tk.Button(
        content,
        text="Close",
        command=details.destroy,
        bg=BLUE,
        fg=WHITE,
        activebackground=BLUE,
        activeforeground=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=8
    ).pack(anchor="w", pady=(12, 0))


# ---------- CLICKABLE EVENT CARDS ----------
def clear_results():
    for widget in results.winfo_children():
        widget.destroy()


def attach_click(widget, event_data):
    # Each widget gets its own handler with the correct event captured.
    widget.configure(cursor="hand2")
    widget.bind(
        "<Button-1>",
        lambda click, data=event_data: show_event_details(data),
        add="+"
    )

    # Also make every nested label and frame clickable.
    for child in widget.winfo_children():
        attach_click(child, event_data)


def show_events(events):
    clear_results()

    if not events:
        tk.Label(
            results,
            text="No upcoming events found.",
            bg=WHITE,
            fg=MUTED,
            font=("Arial", 11),
            pady=20
        ).pack(fill="x")
        return

    for event_data in events[:5]:
        card = tk.Frame(
            results,
            bg=WHITE,
            padx=12,
            pady=8,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(fill="x", pady=4)

        category = str(event_data.get("category") or "Campus Event")

        emoji = next(
            (
                icon for icon, name in interests
                if name.lower() in category.lower()
                or category.lower() in name.lower()
            ),
            "🎉"
        )

        top = tk.Frame(card, bg=WHITE)
        top.pack(fill="x")

        tk.Label(
            top,
            text=f"{emoji}  {event_data.get('title', 'Campus Event')}",
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=DARK,
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        if "score" in event_data:
            tk.Label(
                top,
                text=f"{event_data['score']:.0%} match",
                font=("Arial", 9, "bold"),
                bg="#EAF8F0",
                fg="#168454",
                padx=6,
                pady=3
            ).pack(side="right", padx=(5, 0))

        tk.Label(
            card,
            text=(
                f"📅 {event_data.get('event_date') or 'Date TBA'}    "
                f"📍 {event_data.get('venue') or 'Venue TBA'}"
            ),
            font=("Arial", 9),
            bg=WHITE,
            fg=MUTED,
            anchor="w"
        ).pack(fill="x", pady=(4, 2))

        description = (
            event_data.get("description")
            or "Click to view event details."
        )

        short_description = (
            description[:102] + "..."
            if len(description) > 105
            else description
        )

        tk.Label(
            card,
            text=short_description,
            font=("Arial", 9),
            bg=WHITE,
            fg="#58647C",
            anchor="w",
            wraplength=480,
            justify="left"
        ).pack(fill="x")

        # Bind after ALL card contents have been created.
        attach_click(card, event_data)


# ---------- BUTTON ACTIONS ----------
def recommend():
    chosen = [
        name for name, var in selected.items()
        if var.get()
    ]

    if not chosen:
        messagebox.showinfo(
            "Choose interests",
            "Select at least one interest first! ✨",
            parent=root
        )
        return

    try:
        events = get_events()

        if not events:
            messagebox.showinfo(
                "No events",
                "No upcoming events found. Check your database.",
                parent=root
            )
            return

        ranked = recommend_events(" ".join(chosen), events)
        show_events(ranked)

    except Exception as error:
        messagebox.showerror(
            "Error",
            str(error),
            parent=root
        )


def view_all():
    try:
        show_events(get_events())
    except Exception as error:
        messagebox.showerror(
            "Database Error",
            str(error),
            parent=root
        )


def make_button(parent, text, command, color, fg):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=fg,
        activebackground=color,
        activeforeground=fg,
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=9
    )


make_button(
    left,
    "✨ Recommend for Me",
    recommend,
    BLUE,
    WHITE
).pack(fill="x", pady=(0, 7))

make_button(
    left,
    "🎉 View All Events",
    view_all,
    "#E9EEFF",
    BLUE
).pack(fill="x")


# ---------- STARTUP ----------
root.after(200, view_all)
root.mainloop()
