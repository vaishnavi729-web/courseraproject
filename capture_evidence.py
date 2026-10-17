import asyncio
import time
from playwright.async_api import async_playwright

async def capture_screenshots():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        # 1. admin_login.png
        try:
            print("Capturing admin_login.png...")
            await page.goto("http://127.0.0.1:8000/admin/")
            # Login
            await page.fill('input[name="username"]', "root")
            await page.fill('input[name="password"]', "password123")
            await page.click('input[type="submit"]')
            await page.wait_for_selector('h1:has-text("Site administration")')
            await page.screenshot(path="assessment_submission/screenshots/admin_login.png", full_page=True)
        except Exception as e:
            print(f"Error on admin login: {e}")

        # 2. admin_logout.png
        try:
            print("Capturing admin_logout.png...")
            await page.click('form#logout-form button[type="submit"]')
            await page.wait_for_selector('h1:has-text("Logged out")')
            await page.screenshot(path="assessment_submission/screenshots/admin_logout.png", full_page=True)
        except Exception as e:
            print(f"Error on admin logout: {e}")

        # Frontend captures - anonymous
        # 3. get_dealers.png
        try:
            print("Capturing get_dealers.png...")
            await page.goto("http://127.0.0.1:8000/")
            await page.wait_for_selector('table')
            await asyncio.sleep(2) # wait for fetch to complete
            await page.screenshot(path="assessment_submission/screenshots/get_dealers.png", full_page=True)
        except Exception as e:
            print(f"Error on get_dealers: {e}")

        # 4. dealersbystate.png
        try:
            print("Capturing dealersbystate.png...")
            # Using Kansas filter from dropdown
            await page.select_option('select#state', 'Kansas')
            await asyncio.sleep(2) # wait for fetch
            await page.screenshot(path="assessment_submission/screenshots/dealersbystate.png", full_page=True)
        except Exception as e:
            print(f"Error on dealersbystate: {e}")

        # 5. contact_us.png
        try:
            print("Capturing contact_us.png...")
            await page.goto("http://127.0.0.1:8000/static/ContactUs.html")
            await asyncio.sleep(1)
            await page.screenshot(path="assessment_submission/screenshots/contact_us.png", full_page=True)
        except Exception as e:
            print(f"Error on contact_us: {e}")

        # Login in frontend
        try:
            print("Logging into frontend...")
            await page.goto("http://127.0.0.1:8000/login")
            await page.fill('input[name="username"]', "root")
            await page.fill('input[name="psw"]', "password123")
            await page.click('input[value="Login"]')
            await asyncio.sleep(2)
            await page.wait_for_url("http://127.0.0.1:8000/")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Error logging into frontend: {e}")

        # 6. get_dealers_loggedin.png (home page now logged in)
        try:
            print("Capturing get_dealers_loggedin.png...")
            await page.screenshot(path="assessment_submission/screenshots/get_dealers_loggedin.png", full_page=True)
        except Exception as e:
            print(f"Error on get_dealers_loggedin: {e}")

        # 7. dealer_id_reviews.png (go to dealer 1)
        try:
            print("Capturing dealer_id_reviews.png...")
            await page.goto("http://127.0.0.1:8000/dealer/1")
            await page.wait_for_selector('.reviews_panel')
            await asyncio.sleep(2)
            await page.screenshot(path="assessment_submission/screenshots/dealer_id_reviews.png", full_page=True)
            
            # Click 'post review' icon/button (the link wrapping the image)
        except Exception as e:
            print(f"Error on dealer_id_reviews: {e}")

        # 8. dealership_review_submission.png
        try:
            print("Capturing dealership_review_submission.png...")
            await page.goto("http://127.0.0.1:8000/postreview/1")
            
            # Fill form
            await page.fill('textarea#review', 'Amazing dealership with fantastic services, highly recommended!')
            await page.fill('input[type="date"]', '2023-10-01')
            await page.select_option('select#cars', index=1)
            await page.fill('input[type="int"]', '2020')
            await asyncio.sleep(1)
            await page.screenshot(path="assessment_submission/screenshots/dealership_review_submission.png", full_page=True)
            
            # 9. added_review.png
            print("Capturing added_review.png...")
            await page.click('button.postreview')
            # Wait for return to dealer page
            await page.wait_for_url("http://127.0.0.1:8000/dealer/1")
            await asyncio.sleep(3) # Wait for reviews to load
            await page.screenshot(path="assessment_submission/screenshots/added_review.png", full_page=True)
        except Exception as e:
            print(f"Error on dealership_review_submission/added_review: {e}")

        await browser.close()
        print("Done!")

if __name__ == "__main__":
    asyncio.run(capture_screenshots())
