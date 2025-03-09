import requests
from bs4 import BeautifulSoup
import yaml
import time
import re

def get_paper_details(paper_url, headers):
    """Get the detailed paper information from the paper's specific page"""
    try:
        response = requests.get(paper_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        paper_info = {}

        # Get title and URL
        title_wrapper = soup.find('div', id='gsc_oci_title_wrapper')
        if title_wrapper:
            title_link = title_wrapper.find('a', class_='gsc_oci_title_link')
            if title_link:
                paper_info['title'] = title_link.text.strip()
                paper_info['url'] = title_link.get('href', '')

        # Get authors
        authors_div = soup.find('div', class_='gsc_oci_value', recursive=True)
        if authors_div:
            authors = [author.strip() for author in authors_div.text.split(',')]
            if len(authors) > 6:  # If more than 6 authors, use et al.
                authors = authors[:6] + ['et al.']
            paper_info['authors'] = authors

        # Get journal and year
        journal_div = soup.find_all('div', class_='gsc_oci_value')
        if len(journal_div) > 1:
            journal_text = journal_div[1].text.strip()
            # Try to extract year using regex
            year_match = re.search(r'\b20\d{2}\b', journal_text)
            year = year_match.group(0) if year_match else ''
            journal = re.sub(r'\b20\d{2}\b', '', journal_text).strip().split(',')[0]
            paper_info['journal'] = f"{journal}, {year}"

        # Get abstract if available
        abstract_div = soup.find('div', class_='gsc_oci_value', id='gsc_oci_descr')
        if abstract_div:
            paper_info['abstract'] = abstract_div.text.strip()

        return paper_info

    except Exception as e:
        print(f"Error getting paper details: {str(e)}")
        return None

def create_yaml_output(scholar_id, papers):
    yaml_dict = {
        'enable': True,
        'title': 'Publications',
        'description': 'Selected publications in computational biology, bioinformatics, and machine learning',
        'footertext': f'View all publications on <a href="https://scholar.google.com/citations?hl=en&user={scholar_id}" target="_blank">Google Scholar</a>',
        'papers': papers
    }
    return yaml_dict

def scrape_google_scholar(scholar_id):
    base_url = "https://scholar.google.com"
    profile_url = f"{base_url}/citations?hl=en&user={scholar_id}&hl=en&scioq=oteri+f.&cstart=0&pagesize=80&sortby=pubdate"
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(profile_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        papers = []

        paper_entries = soup.find_all('tr', class_='gsc_a_tr')

        for entry in paper_entries:
            title_link = entry.find('a', class_='gsc_a_at')
            if title_link:
                paper_url = base_url + title_link.get('href')
                time.sleep(1)  # Delay between requests

                paper_details = get_paper_details(paper_url, headers)
                if paper_details:
                    # Add placeholder for thumbnail
                    paper_details['thumbnail'] = f"/images/papers/{slugify(paper_details['title'])}.jpg"
                    papers.append(paper_details)

        # Create YAML structure
        yaml_output = create_yaml_output(scholar_id, papers)

        # Save to YAML file
        output_file = 'themes\hugo-elate-theme\data\papers.yaml'
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_output, f, allow_unicode=True, sort_keys=False)

        print(f"Data has been saved to {output_file}")
        return yaml_output

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

if __name__ == "__main__":
    scholar_id = "Ebgxuk4AAAAJ"
    yaml_data = scrape_google_scholar(scholar_id)

    if yaml_data:
        print("\nExample of the YAML output:")
        print(yaml.dump(yaml_data, allow_unicode=True, sort_keys=False))

# Created/Modified files during execution:
# publications.yml