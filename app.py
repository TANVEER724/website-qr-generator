import streamlit as st
import qrcode
from io import BytesIO
from urllib.parse import urlparse
import os

# ==============================
# Page Configuration
# ==============================
st.set_page_config(
    page_title="Website QR Code Generator",
    page_icon="🌐",
    layout="centered"
)

# ==============================
# Create Folder for QR Codes
# ==============================
SAVE_FOLDER = "generated_qr"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# ==============================
# Title
# ==============================
st.title("🌐 Website QR Code Generator")
st.write("Generate a QR Code for any website URL.")

# ==============================
# Website Input
# ==============================
website = st.text_input(
    "Enter Website URL",
    placeholder="https://www.google.com"
)

# ==============================
# Generate QR Code
# ==============================
if st.button("Generate QR Code"):

    if not website.strip():
        st.warning("⚠ Please enter a website URL.")

    else:

        # Automatically add https:// if missing
        if not website.startswith(("http://", "https://")):
            website = "https://" + website

        parsed = urlparse(website)

        if not parsed.scheme or not parsed.netloc:
            st.error("❌ Invalid website URL.")

        else:
            # Create QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4
            )

            qr.add_data(website)
            qr.make(fit=True)

            img = qr.make_image(
                fill_color="black",
                back_color="white"
            ).get_image()

            # Create filename
            filename = (
                parsed.netloc.replace(".", "_")
                + ".png"
            )

            filepath = os.path.join(SAVE_FOLDER, filename)

            # Save locally
            img.save(filepath)

            # Convert to bytes
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            # Show QR Code
            st.success("✅ Website QR Code Generated Successfully!")

            st.image(
                img,
                caption="Website QR Code",
                width=300
            )

            # Show URL
            st.write("### 🔗 Website")
            st.code(website)

            # Download Button
            st.download_button(
                label="⬇ Download QR Code",
                data=buffer,
                file_name=filename,
                mime="image/png"
            )

            st.info(f"📁 Saved to: {filepath}")