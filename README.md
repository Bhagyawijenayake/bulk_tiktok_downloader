# TikTok Video Downloader
![image](https://github.com/user-attachments/assets/37d0e4fc-74ed-4e4e-b944-a45e0f3be28e)


A Python-based GUI application to download TikTok videos, organize them into categories, and reframe them to a specific resolution (e.g., 1080x1920 for vertical videos).

---

## Features
- **Download TikTok Videos**: Enter TikTok video URLs and download them in bulk.
- **Organize by Categories**: Group downloaded videos into custom categories.
- **Reframe Videos**: Automatically reframe videos to a specific resolution (e.g., 1080x1920).
- **User-Friendly GUI**: Built with `tkinter` for ease of use.

---

## Download the Application

If you don't want to install Python and dependencies, you can download the pre-built executable:

- **Windows**: [Download TikTok Downloader (ZIP)](https://github.com/Bhagyawijenayake/bulk_tiktok_downloader/raw/main/tiktok_downloader.zip)
  - Extract the `.zip` file and run `tiktok_downloader.exe`.

---

### Notes for Executable Users
- Ensure you have **FFmpeg** installed and added to your system's PATH. Download it from [ffmpeg.org](https://ffmpeg.org/).
- The application may be flagged by antivirus software (false positive). If you trust the source, you can allow it to run.

---

## Requirements (For Running the Source Code)
- Python 3.x
- Libraries: `yt-dlp`, `tkinter`, `ffmpeg`

---

## Installation (For Running the Source Code)

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Bhagyawijenayake/bulk_tiktok_downloader.git
   cd bulk_tiktok_downloader
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg**:
   - Download and install FFmpeg from [ffmpeg.org](https://ffmpeg.org/).
   - Ensure FFmpeg is added to your system's PATH.

---

## Usage

1. **Run the Application**:
   ```bash
   python tiktok_downloader.py
   ```

2. **Steps to Use**:
   - Select an output folder.
   - Add categories (e.g., "Funny", "Educational").
   - Enter TikTok video URLs for each category.
   - Click "Download All" or "Download Selected Category" to start downloading.

3. **Reframed Videos**:
   - After downloading, videos are automatically reframed to 1080x1920 resolution and saved in the output folder.

---

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the Repository**:
   - Click the "Fork" button on the top-right of this repository.

2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/Bhagyawijenayake/bulk_tiktok_downloader.git
   ```

3. **Create a New Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes and Commit**:
   ```bash
   git add .
   git commit -m "Add your feature or fix"
   ```

5. **Push Changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**:
   - Go to the original repository and click "New Pull Request".
   - Describe your changes and submit the PR.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading.
- [FFmpeg](https://ffmpeg.org/) for video reframing.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI.

---

## Contact

For questions or feedback, feel free to reach out:
- **Bhagya Wijenayake**: [bhagyasudaraka98@gmail.com](mailto:bhagyasudaraka98@gmail.com)
- **GitHub**: [Bhagyawijenayake](https://github.com/Bhagyawijenayake)

