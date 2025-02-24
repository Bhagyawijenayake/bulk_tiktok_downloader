import os
import subprocess
import yt_dlp
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from tkinter.ttk import Progressbar
import threading

# Function to sanitize filenames
def sanitize_filename(filename, max_length=100):
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return filename[:max_length].strip()

# Function to reframe videos
def reframe_video(input_video, output_video, width=1080, height=1920):
    command = [
        "ffmpeg", 
        "-i", input_video,  # Input file
        "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",  # Scale and pad video
        "-c:a", "copy",  # Copy audio stream without re-encoding
        output_video  # Output file
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Video successfully reframed: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"Error reframing video: {e}")

# Function to download TikTok videos
def download_tiktok_videos(urls, output_dir, category, progress_callback=None):
    category_dir = os.path.join(output_dir, category)
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)

    ydl_opts = {
        'outtmpl': os.path.join(category_dir, '%(id)s.%(ext)s'),  # Save videos with ID to prevent long names
        'quiet': False,  # Show download progress
        'restrictfilenames': True,  # Restrict filenames to only valid characters
        'progress_hooks': [progress_callback] if progress_callback else [],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for i, url in enumerate(urls):
            try:
                print(f"Downloading video {i+1} of {len(urls)} ({category}): {url}")
                ydl.download([url])  # Download the video
            except Exception as e:
                print(f"Failed to download {url}: {e}")

# Function to reframe all videos in a folder
def reframe_all_videos_in_folder(folder_path, width=1080, height=1920):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".mp4"):  # Ensure we're only processing MP4 files
                input_video = os.path.join(root, filename)
                output_video = os.path.join(root, f"reframed_{filename}")
                reframe_video(input_video, output_video, width, height)

# GUI Application
class TikTokDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Video Downloader")
        self.root.geometry("800x600")

        # Variables
        self.output_dir = tk.StringVar()
        self.categories = []  # List to store categories
        self.category_urls = {}  # Dictionary to store URLs by category
        self.selected_category = tk.StringVar()  # Currently selected category

        # GUI Elements
        tk.Label(root, text="Output Folder:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.output_dir, width=40).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_folder).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=10)
        self.category_entry = tk.Entry(root, width=20)
        self.category_entry.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(root, text="Add Category", command=self.add_category).grid(row=1, column=2, padx=10, pady=10)

        tk.Label(root, text="Select Category:").grid(row=2, column=0, padx=10, pady=10)
        self.category_dropdown = ttk.Combobox(root, textvariable=self.selected_category, state="readonly")
        self.category_dropdown.grid(row=2, column=1, padx=10, pady=10)
        self.category_dropdown.bind("<<ComboboxSelected>>", self.update_url_list)

        tk.Label(root, text="URLs (one per line):").grid(row=3, column=0, padx=10, pady=10)
        self.urls_text = scrolledtext.ScrolledText(root, width=50, height=10)
        self.urls_text.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

        tk.Button(root, text="Add URLs", command=self.add_urls).grid(row=4, column=1, padx=10, pady=10)

        # Treeview to display URLs for the selected category
        self.tree = ttk.Treeview(root, columns=("No.", "URLs", "Delete"), show="headings")
        self.tree.heading("No.", text="No.")
        self.tree.heading("URLs", text="URLs")
        self.tree.heading("Delete", text="Delete")
        self.tree.column("No.", width=50)
        self.tree.column("URLs", width=400)
        self.tree.column("Delete", width=100)
        self.tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Bind the delete function to the Treeview
        self.tree.bind("<Button-1>", self.on_treeview_click)

        # Progress Bar
        self.progress = Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=6, column=1, padx=10, pady=10)

        # Label to show current progress
        self.progress_label = tk.Label(root, text="")
        self.progress_label.grid(row=7, column=1, padx=10, pady=10)

        # Buttons for downloading
        tk.Button(root, text="Download All", command=self.start_download_all).grid(row=8, column=1, padx=10, pady=10)
        tk.Button(root, text="Download Selected Category", command=self.start_download_selected_category).grid(row=8, column=2, padx=10, pady=10)

    # Function to browse for output folder
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir.set(folder)

    # Function to add a category
    def add_category(self):
        category = self.category_entry.get().strip()
        if category:
            if category not in self.categories:
                self.categories.append(category)
                self.category_urls[category] = []
                self.category_dropdown["values"] = self.categories
                self.category_entry.delete(0, tk.END)
                messagebox.showinfo("Success", f"Category '{category}' added.")
            else:
                messagebox.showwarning("Error", f"Category '{category}' already exists.")
        else:
            messagebox.showwarning("Error", "Please enter a category name.")

    # Function to add URLs to the selected category
    def add_urls(self):
        category = self.selected_category.get()
        if not category:
            messagebox.showwarning("Error", "Please select a category.")
            return

        urls = self.urls_text.get("1.0", tk.END).strip().splitlines()
        if urls:
            self.category_urls[category].extend(urls)
            self.update_url_list()
            self.urls_text.delete("1.0", tk.END)
            messagebox.showinfo("Success", f"Added {len(urls)} URLs to category '{category}'.")
        else:
            messagebox.showwarning("Error", "Please enter at least one URL.")

    # Function to update the URL list for the selected category
    def update_url_list(self, event=None):
        category = self.selected_category.get()
        self.tree.delete(*self.tree.get_children())
        if category:
            for i, url in enumerate(self.category_urls.get(category, [])):
                self.tree.insert("", "end", values=(i+1, url, "Delete"))

    # Function to handle Treeview click events
    def on_treeview_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == "#3":  # Check if the "Delete" column was clicked
                item = self.tree.identify_row(event.y)
                url = self.tree.item(item, "values")[1]
                self.delete_url(url)

    # Function to delete a URL
    def delete_url(self, url):
        category = self.selected_category.get()
        if category in self.category_urls:
            self.category_urls[category].remove(url)
            self.update_url_list()
            messagebox.showinfo("Success", f"URL '{url}' deleted from category '{category}'.")

    # Function to start downloading all categories in a separate thread
    def start_download_all(self):
        output_dir = self.output_dir.get()
        if not output_dir:
            messagebox.showwarning("Error", "Please select an output folder.")
            return

        total_urls = sum(len(urls) for urls in self.category_urls.values())
        self.progress["value"] = 0
        self.progress["maximum"] = total_urls

        # Start the download process in a separate thread
        threading.Thread(target=self.download_all, args=(output_dir,), daemon=True).start()

    # Function to download all categories
    def download_all(self, output_dir):
        def update_progress(d):
            if d["status"] == "finished":
                self.progress["value"] += 1
                percentage = (self.progress["value"] / self.progress["maximum"]) * 100
                self.progress_label.config(text=f"Downloading {d['filename']} - {percentage:.2f}%")
                self.root.update_idletasks()

        for category, urls in self.category_urls.items():
            if urls:
                download_tiktok_videos(urls, output_dir, category, update_progress)
                reframe_all_videos_in_folder(os.path.join(output_dir, category))
        messagebox.showinfo("Success", "All videos downloaded and reframed!")

    # Function to start downloading the selected category in a separate thread
    def start_download_selected_category(self):
        output_dir = self.output_dir.get()
        if not output_dir:
            messagebox.showwarning("Error", "Please select an output folder.")
            return

        category = self.selected_category.get()
        if not category:
            messagebox.showwarning("Error", "Please select a category.")
            return

        urls = self.category_urls.get(category, [])
        if urls:
            self.progress["value"] = 0
            self.progress["maximum"] = len(urls)

            # Start the download process in a separate thread
            threading.Thread(target=self.download_selected_category, args=(output_dir, category), daemon=True).start()
        else:
            messagebox.showwarning("Error", f"No URLs found for category '{category}'.")

    # Function to download the selected category
    def download_selected_category(self, output_dir, category):
        def update_progress(d):
            if d["status"] == "finished":
                self.progress["value"] += 1
                percentage = (self.progress["value"] / self.progress["maximum"]) * 100
                self.progress_label.config(text=f"Downloading {d['filename']} - {percentage:.2f}%")
                self.root.update_idletasks()

        download_tiktok_videos(self.category_urls[category], output_dir, category, update_progress)
        reframe_all_videos_in_folder(os.path.join(output_dir, category))
        messagebox.showinfo("Success", f"Videos for category '{category}' downloaded and reframed!")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TikTokDownloaderApp(root)
    root.mainloop()