import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np

# --- Nastavení ---
st.set_page_config(layout="wide")
FONT_PATH = "fonts/Inter-Bold.ttf"  # Nahraj Inter Bold font
TEXT_SIZE = 100
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720
YELLOW = (255, 204, 0)
WHITE = (255, 255, 255)

# --- Databáze hostů ---
HOSTS = {
    "Tomáš Roud": "hosts/tomas_roud.png",
    "Dominik Hais": "hosts/dominik_hais.png"
}

# --- Sidebar ---
st.sidebar.header("🎛️ Nastavení postu")
white_text = st.sidebar.text_input("Bílý text", "Co vláda pokazila")
yellow_text = st.sidebar.text_input("Žlutý text", "a co ne?")
selected_hosts = st.sidebar.multiselect("Vyber hosty", list(HOSTS.keys()), default=list(HOSTS.keys()))
uploaded_bg = st.sidebar.file_uploader("Pozadí (16:9)", type=["jpg", "png"])

# --- Canvas ---
canvas = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0))

# --- Pozadí ---
if uploaded_bg:
    bg = Image.open(uploaded_bg).convert("RGB")
    # Ořízni na střed 16:9
    bg_ratio = 16 / 9
    img_ratio = bg.width / bg.height

    if img_ratio > bg_ratio:
        new_width = int(bg.height * bg_ratio)
        left = (bg.width - new_width) // 2
        bg = bg.crop((left, 0, left + new_width, bg.height))
    else:
        new_height = int(bg.width / bg_ratio)
        top = (bg.height - new_height) // 2
        bg = bg.crop((0, top, bg.width, top + new_height))

    bg = bg.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
    canvas.paste(bg)

# --- Překryvný efekt ---
overlay = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0, 180))
canvas.paste(overlay, (0, 0), overlay)

# --- Text ---
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype(FONT_PATH, TEXT_SIZE)

draw.text((80, 100), white_text, font=font, fill=WHITE)
draw.text((80, 220), yellow_text, font=font, fill=YELLOW)

# --- Hosté ---
x_offset = 700
for host in selected_hosts:
    host_path = HOSTS[host]
    host_img = Image.open(host_path).convert("RGBA").resize((400, 400))
    canvas.paste(host_img, (x_offset, 300), host_img)
    x_offset += 420

# --- Žlutý pruh dole ---
draw.rectangle([0, IMAGE_HEIGHT - 60, IMAGE_WIDTH, IMAGE_HEIGHT], fill=YELLOW)
draw.text((20, IMAGE_HEIGHT - 52), "voluntia.cz", font=ImageFont.truetype(FONT_PATH, 30), fill=(0, 0, 0))
logo = Image.open("logo/voluntia_logo.png").convert("RGBA").resize((300, 60))
canvas.paste(logo, (IMAGE_WIDTH - 320, IMAGE_HEIGHT - 65), logo)

# --- Zobrazení výsledku ---
st.image(canvas, caption="📸 Náhled postu", use_column_width=True)

# --- Export ---
buf = io.BytesIO()
canvas.save(buf, format="PNG")
st.download_button("📥 Stáhnout jako PNG", buf.getvalue(), "voluntia_post.png", "image/png")
