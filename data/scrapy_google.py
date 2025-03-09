import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_paper_details(paper_url, headers):
    """Get the detailed paper URL from the paper's specific page"""
    try:
        response = requests.get(paper_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the title link in the detailed view
        title_wrapper = soup.find('div', id='gsc_oci_title_wrapper')
        if title_wrapper:
            title_link = title_wrapper.find('a', class_='gsc_oci_title_link')
            if title_link:
                return {
                    'title': title_link.text.strip(),
                    'url': title_link.get('href', '')
                }
    except Exception as e:
        print(f"Error getting paper details: {str(e)}")
    return None

def scrape_google_scholar(scholar_id):
    # URL of the Google Scholar page
    base_url = "https://scholar.google.com"
    profile_url = f"{base_url}/citations?hl=en&user={scholar_id}&hl=en&scioq=oteri+f.&cstart=0&pagesize=80&sortby=pubdate
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Make the request to the main profile page
        response = requests.get(profile_url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Lists to store paper information
        papers = []

        # Find all paper entries in the main profile page
        paper_entries = soup.find_all('tr', class_='gsc_a_tr')

        for entry in paper_entries:
            # Find the paper title link
            title_link = entry.find('a', class_='gsc_a_at')
            if title_link:
                paper_url = base_url + title_link.get('href')

                # Add delay between requests
                time.sleep(2)

                # Get paper details from the paper's page
                paper_details = get_paper_details(paper_url, headers)

                if paper_details:
                    papers.append(paper_details)

        # Create a DataFrame
        df = pd.DataFrame(papers)

        # Save to CSV
        output_file = 'google_scholar_papers.csv'
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Data has been saved to {output_file}")

        return df

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage with the scholar ID
    scholar_id = "Ebgxuk4AAAAJ"
    papers_df = scrape_google_scholar(scholar_id)

    if papers_df is not None:
        print("\nFirst few entries:")
        print(papers_df.head())

# Created/Modified files during execution:
# google_scholar_papers.csv