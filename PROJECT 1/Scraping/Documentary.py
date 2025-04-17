from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time

def scrape_imdb_movies():
    chrome_driver_path = r"C:\\chromedriver\\chromedriver.exe"  # Update with actual path
    
    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (optional)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    
    # Start the ChromeDriver service
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres=documentary"
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)
        
        total_movies = 300  # Total movies expected
        scraped_data = []
        unique_movies = set()
        movie_count = 0

        while movie_count < total_movies:
            print(f"\nScraping... Collected {movie_count}/{total_movies} movies")

            try:
                # Locate the movie list
                movies_list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list")))
                movies = movies_list.find_elements(By.TAG_NAME, "li")

                for movie in movies:
                    try:
                        name = movie.find_element(By.TAG_NAME, "h3").text.strip()
                    except:
                        name = "N/A"
                    
                    # Skip duplicate movies
                    if name in unique_movies:
                        continue
                    
                    unique_movies.add(name)

                    try:
                        rating_text = movie.find_element(By.XPATH, './/span[contains(@class, "ipc-rating-star")]').text.strip()
                        rating_match = re.match(r"(\d+\.\d+)", rating_text)  # Extract numeric rating
                        rating = rating_match.group(1) if rating_match else "N/A"
    
                        votes_match = re.search(r"\(([\dKk]+)\)", rating_text)  # Extract votes count
                        votes = votes_match.group(1) if votes_match else "N/A"
                    except:
                        rating = "N/A"
                        votes = "N/A"

                    try:
                        duration_element = movie.find_element(By.XPATH, ".//div[1]/div[2]/div[2]/span[2]")
                        duration = duration_element.text.strip()
                    except:
                        duration = "N/A"

                    genre = "Documentary"  # Set genre to Action explicitly

                    movie_count += 1
                    print(f"{movie_count}/{total_movies}. {name} - {rating} - {votes} - {duration} - {genre}")

                    # Store data
                    scraped_data.append([name, rating, votes, duration, genre])
                
                # Click the "Load More" button if available
                try:
                    load_more_button = driver.find_element(By.CLASS_NAME, "ipc-see-more__button")
                    if load_more_button.is_displayed():
                        driver.execute_script("arguments[0].click();", load_more_button)
                        time.sleep(2)  # Allow time for content to load
                    else:
                        print("No more movies to load.")
                        break
                except:
                    print("No more movies to load.")
                    break
            
            except Exception as e:
                print(f"Error occurred: {e}")
                break

    finally:
        driver.quit()
    
        # Save data to CSV file
        output_file = "documentary_movies.csv"
        df = pd.DataFrame(scraped_data, columns=["Name", "Rating", "Votes", "Duration", "Genre"])
        df.to_csv(output_file, index=False)
        print(f"\nScraping completed. Data saved to {output_file}")
        print(f"Total unique movies scraped: {len(df)}/{total_movies}")

# Run the scraper
scrape_imdb_movies()
