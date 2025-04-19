import gdown

def convert_drive_link(drive_url: str) -> str:
    try:
        file_id = drive_url.split("/d/")[1].split("/")[0]
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    except IndexError:
        return None

def fetch_image(url: str) -> str:
    url = convert_drive_link(url)

    if url is None:
        raise ValueError("Invalid URL provided.")

    # Download the image
    output_path = "reference.png"
    gdown.download(url, output_path, quiet=False)
    return output_path

