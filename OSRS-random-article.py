import requests
from colorama import Fore, Style, init
import textwrap

init(autoreset=True)

# Function to fetch random article
def fetch_random_osrs_article():
    api_url = "https://oldschool.runescape.wiki/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'random',
        'rnnamespace': 0,
        'rnlimit': 1
    }

    response = requests.get(api_url, params=params)
    data = response.json()

    try:
        random_title = data['query']['random'][0]['title']
        return random_title
    except KeyError:
        print(f"{Fore.RED}Error: Unable to fetch random article title from OSRS Wiki.{Style.RESET_ALL}")
        return None

# Function to fetch the content of article
def fetch_osrs_article_content(title):
    api_url = "https://oldschool.runescape.wiki/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'extracts',
        'exintro': True,
        'explaintext': True
    }

    response = requests.get(api_url, params=params)
    data = response.json()

    try:
        page = next(iter(data['query']['pages'].values()))
        article_text = page['extract']
        return article_text
    except KeyError:
        print(f"{Fore.RED}Error: Unable to fetch article content from OSRS Wiki.{Style.RESET_ALL}")
        return None

def main():
    print(f"{Fore.GREEN}\n" + "-"*60)
    print(f"{Fore.GREEN} Welcome to Your Random OSRS Wiki Article Viewer!{Style.RESET_ALL}")
    print(f"{Fore.GREEN} by Andrew Parsons")

    while True:
        print(f"{Fore.GREEN}\n" + "-"*60)
        print(f"{Fore.YELLOW} Fetching a random Old School Runescape article from OSRS Wiki...{Style.RESET_ALL}")
        random_title = fetch_random_osrs_article()

        if random_title:
            print("\n OSRS Article Title:", f"{Fore.CYAN}{random_title}{Style.RESET_ALL}")

            user_input = input("\n Do you wish to read the summary of this article? (yes/no): ").lower()

            if user_input == 'yes':
                article_text = fetch_osrs_article_content(random_title)

                if article_text is not None:
                    print("\n", "-"*60, "\n")
                    # Wrap the text to handle word wrapping
                    wrapped_text = textwrap.fill(article_text, width=80)
                    print(wrapped_text)
                    print("\n", "-"*60)
                else:
                    print(f"{Fore.RED}Failed to fetch article content. Please try again.{Style.RESET_ALL}")
            elif user_input == 'no':
                print(f"{Fore.YELLOW}Fetching another random article from OSRS Wiki...{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid input.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
