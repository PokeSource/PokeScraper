# *--/ PokeScraper, by Mindset. \--*
import os
import json
import requests
from colorama             import Fore, Style, init

# ---------------------------------------------------- #
init(autoreset=True)

BASE_URL = "https://pokeapi.co/api/v2/"

CATEGORIES = [
    "pokemon",
    "region",
    "move",
    "location",
    "wild-area",
    "type"
]

SCRAPER_VERSION = "1.072"
MAX_404_ERRORS = 3

def make_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def fetch_data(endpoint, item_id):
    url = f"{BASE_URL}{endpoint}/{item_id}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        print(f"Failed to fetch {endpoint}/{item_id}. Status: {response.status_code}")
        return None

def save_json_data(category, data, base_folder):
    if data:
        folder_english = os.path.join(base_folder, category, "English")
        folder_japanese = os.path.join(base_folder, category, "Japanese")
        make_directory(folder_english)
        make_directory(folder_japanese)

        for lang_folder, lang_key in [(folder_english, "en"), (folder_japanese, "ja")]:
            file_path = os.path.join(lang_folder, f"{data['id']}.json")
            header = {
                "Made by": "mindset",
                "Scraper Version": SCRAPER_VERSION
            }
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump({"header": header, "data": data}, file, indent=8, ensure_ascii=False)

def save_sprites(pokemon_data, base_folder):
    sprites = pokemon_data.get("sprites", {})
    pokemon_name = pokemon_data.get("name", f"pokemon_{pokemon_data['id']}")
    folder = os.path.join(base_folder, "sprites", pokemon_name)
    make_directory(folder)

    sprite_urls = {
        "front_default": sprites.get("front_default"),
        "back_default": sprites.get("back_default"),
        "front_shiny": sprites.get("front_shiny"),
        "back_shiny": sprites.get("back_shiny")
    }

    for sprite_name, url in sprite_urls.items():
        if url:
            response = requests.get(url)
            if response.status_code == 200:
                sprite_path = os.path.join(folder, f"{sprite_name}.png")
                with open(sprite_path, "wb") as img_file:
                    img_file.write(response.content)

def show_menu():
    print(Fore.YELLOW + Style.BRIGHT + "=" * 40)
    print(" " * 15 + "PokeScraper")
    print(" " * 20 + f"By Mindsetpro")
    print(Fore.CYAN + Style.BRIGHT + "-" * 40)
    print("[1.] Scrape Sprites")
    print("[2.] Scrape JSON")
    print("[3.] Scrape Both")
    print("[4.] Credits/API Status")
    print(Fore.YELLOW + Style.BRIGHT + "=" * 40)
    return input("Enter your choice: ").strip()

def main():
    base_folder = "PokeScraper_Data"
    make_directory(base_folder)

    choice = show_menu()
    if choice == "4":
        print(Fore.GREEN + """
Made by PokéSource (owner: mindset)

Copyright (c) 2024 PokéSource

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Made with Python 3.12, and PokéAPI.

Version: 1.072
PokéAPI Status: Online
        """)
        return

    scrape_json = scrape_sprites = False
    if choice == "1":
        scrape_sprites = True
    elif choice == "2":
        scrape_json = True
    elif choice == "3":
        scrape_json = scrape_sprites = True
    else:
        print(Fore.RED + "Invalid option!")
        return

    for category in CATEGORIES:
        print(Fore.CYAN + f"Processing {category}...")
        folder = os.path.join(base_folder, category)
        make_directory(folder)

        consecutive_404s = 0
        for item_id in range(1, 11000):
            if consecutive_404s >= MAX_404_ERRORS:
                print(Fore.YELLOW + f"Stopped scraping {category} after {MAX_404_ERRORS} consecutive 404 errors.")
                break

            data = fetch_data(category, item_id)
            if not data:
                consecutive_404s += 1
                continue

            consecutive_404s = 0
            if scrape_json:
                save_json_data(category, data, base_folder)
            if scrape_sprites and category == "pokemon":
                save_sprites(data, base_folder)

if __name__ == "__main__":
    main()
