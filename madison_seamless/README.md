# Charlies Print Helper

A simple plug-in for **GIMP 3.x** that turns any image into a **seamless repeating pattern** and tiles it across a **large poster-sized canvas** at the print resolution you choose. It is designed for people who are not confident with GIMP: open an image, fill in one small dialog, click OK, then export.

Typical use: take a PNG, make it seamless, and prepare a 3 metre wide poster for a large-format printer.

---

## What it does

1. Takes the image you have open in GIMP (your original is never changed).
2. Optionally blends the edges so the image repeats with no visible seams.
3. Scales one copy of the image to the physical size you want it to appear on the print.
4. Repeats it across a new canvas the size of your poster, at your chosen DPI.
5. Opens the finished poster as a new image, ready to export.

Repeating a small seamless image is usually better than stretching one image to 3 metres, which would look blurry.

---

## Features and settings

The plug-in appears in GIMP under **Filters > Charlies Print Helper...** (an image must be open). Each setting has help text in the dialog.

| Setting | What it does | Default |
|---|---|---|
| **Make edges seamless** | Blends the image edges so the repeats join with no visible line. Leave ticked unless your image is already seamless. | On |
| **One repeat size (cm)** | How wide ONE copy of your image will look on the finished print. Smaller gives more repeats and a finer pattern; larger gives fewer, bigger repeats. Height follows the image's proportions. | 30 cm |
| **Poster width (cm)** | Width of the finished print in centimetres (300 = 3 metres). | 300 cm |
| **Poster height (cm)** | Height of the finished print in centimetres. | 100 cm |
| **Print resolution (DPI)** | Print sharpness. 100 is fine for large posters seen from a distance. Higher looks sharper up close but makes a much bigger, slower file. | 100 |

Other behaviour:
- Works on a flattened copy, so the original image and its layers are untouched.
- Shows a progress bar while building.
- Sets the output image's resolution to the DPI you chose.
- Refuses to run if the settings would create more than 600 repeats (to stop GIMP running out of memory). If you see "Too many repeats", make the repeat size larger.

---

## How to use it

1. Open your image in GIMP (**File > Open**).
2. Go to **Filters > Charlies Print Helper...**
3. Set the options:
   - Leave **Make edges seamless** ticked.
   - Set **One repeat size** (how big one copy of the image appears).
   - Set the **Poster width** and **Poster height** in cm.
   - Set the **DPI** (100 is a good starting point).
4. Click **OK**. Wait for the progress bar to finish.
5. A new image opens with the finished poster.
6. Go to **File > Export As...** and save as PNG, TIFF or PDF, depending on what your printer software needs.

**Size guide:** pixel size = centimetres / 2.54 x DPI. A 300 cm wide poster at 100 DPI is about 11,800 pixels wide. At 150 DPI it is about 17,700 pixels wide and needs a lot of memory.

---

## Installation

Requires **GIMP 3.0 or newer** (tested on GIMP 3.2, Windows). It does **not** work with GIMP 2.10.

The plug-in must sit in its **own folder with the same name as the file**:

```
plug-ins/
  madison_seamless/
    madison_seamless.py
```

### Windows

1. Open File Explorer and go to:
   `C:\Users\<your name>\AppData\Roaming\GIMP\3.2\plug-ins`
   (AppData is hidden: type it into the address bar, or turn on View > Show > Hidden items. Use `3.0` instead of `3.2` if that is your version.)
2. Create a folder called `madison_seamless`.
3. Put `madison_seamless.py` inside that folder.
4. Fully close and restart GIMP.

### Linux

1. Copy the `madison_seamless` folder to `~/.config/GIMP/3.0/plug-ins/`
2. Make the file executable: `chmod +x ~/.config/GIMP/3.0/plug-ins/madison_seamless/madison_seamless.py`
3. Restart GIMP.

### macOS

1. Copy the `madison_seamless` folder to `~/Library/Application Support/GIMP/3.0/plug-ins/`
2. Make the file executable: `chmod +x` on the `.py` file.
3. Restart GIMP.

You can confirm the correct folder in GIMP under **Edit > Preferences > Folders > Plug-ins**.

---

## Troubleshooting

- **The menu item doesn't appear:** check the folder layout above. A loose `.py` file directly in `plug-ins` is ignored. Make sure the file is not named `madison_seamless.py.txt` (turn on file name extensions in Windows Explorer). Open an image first, as the item only shows when one is open. It is at the bottom of the **Filters** menu.
- **Still not showing:** open **Windows > Dockable Dialogs > Error Console** in GIMP and look for red messages mentioning `madison_seamless`.
- **"Too many repeats":** increase **One repeat size** or reduce the poster size.
- **GIMP is slow or runs out of memory:** lower the DPI or use bigger repeats.
- **Visible seams or smearing:** the plug-in uses GIMP's built-in Tile Seamless filter, which blends the edges and can look soft on very detailed images. Try a simpler source image or fix the edges by hand in GIMP.

---

## Known limitations

- Built for GIMP 3.x only.
- The seamless effect is the standard GIMP edge blend, not a smart content-aware one.
- Very large posters at high DPI can use a lot of memory.

---

## License

Add your chosen license here (for example MIT) and include a `LICENSE` file in the repository.

Copyright (c) 2026 <your name>
