import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os, zipfile

TARGET_SIZE_KB = 200

def compress_image(input_path, output_path):
    img = Image.open(input_path)
    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    else:
        img = img.convert("RGB")

    quality = 95
    while quality > 10:
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        if os.path.getsize(output_path) <= TARGET_SIZE_KB * 1024:
            break
        quality -= 5
    return output_path

def choose_files():
    files = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.webp")])
    if not files:
        return

    output_zip = "compressed_images.zip"
    with zipfile.ZipFile(output_zip, "w") as zipf:
        for f in files:
            output_file = os.path.splitext(os.path.basename(f))[0] + "_compressed.jpg"
            compressed_path = compress_image(f, output_file)
            zipf.write(compressed_path)
            os.remove(compressed_path)

    messagebox.showinfo("完成", f"已壓縮並打包 {len(files)} 張圖片\n輸出檔案：{output_zip}")

root = tk.Tk()
root.title("圖片壓縮工具")
root.geometry("300x150")

btn = tk.Button(root, text="選擇圖片並批次壓縮", command=choose_files)
btn.pack(expand=True)

root.mainloop()
