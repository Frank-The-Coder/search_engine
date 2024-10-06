'''
The script writes the path of a local HTML file (test.html) to a test_urls.txt file,
which serves as the input for the crawler. It then initializes the crawler, performs
a crawl with a depth of 1, and checks if the crawler correctly builds the expected 
inverted index for the test HTML file. After the test, it cleans up by deleting the 
test_urls.txt file.
'''
import sys
import os

# Add the parent directory (../custom_lib) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'custom_lib')))

# Now you can import crawler
import crawler

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    html_file = os.path.join(script_dir, 'test.html')
    html_file = "file://" + html_file

    # Path for the test_urls.txt file
    test_urls_file = os.path.join(script_dir, 'test_urls.txt')

    # Write the file_url to test_urls.txt
    with open(test_urls_file, 'w') as f:
        f.write(html_file)

    # expected result
    expected_resolved_index = {'test': {html_file}} 

    # actual result
    bot = crawler.crawler(None, "test_urls.txt")
    bot.crawl(depth=1)
    resolved_index = bot.get_resolved_inverted_index()

    assert resolved_index == expected_resolved_index
    
    os.remove(test_urls_file)
