from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import json
import datetime
import re
from sentence_transformers import SentenceTransformer
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize knowledge base
class KnowledgeBase:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.qa_pairs = self._load_qa_pairs()
        self.qa_embeddings = self._compute_embeddings()
        
    def _load_qa_pairs(self):
        # Load the Q&A pairs from the knowledge base
        qa_pairs = [
            {
                "query": "What are the veg starters available at Barbeque Nation?",
                "answer": "The veg starters available are Grill Veg, Mushroom, Paneer, veg kebab, Cajun Spice Potato, and Pineapple.",
                "source": "Menu List _ Barbeque Nation.pdf"
            },
            {
                "query": "What vegetarian dishes are served?",
                "answer": "For vegetarian guests, we offer veg starters like Grill Veg, Mushroom, Paneer, veg kebab, Cajun Spice Potato, and Pineapple; main courses such as Noodles, Oriental Veg, Paneer, Aloo, Veg Kofta, Veg Dry & Gravy, Dal Tadka, Dal Makhani, Veg Biryani, and Rice; and desserts including Angori Gulab Jamun, Phirnee, Ice Cream, Pie/tart, Fruits, Pastry, Brownie, and Pudding/soufflé. We also have veg soups and salads.",
                "source": "Menu List _ Barbeque Nation.pdf"
            },
            {
                "query": "Can I get Jain food at Barbeque Nation, and what type of fish do you serve?",
                "answer": "Yes, Jain food is available, but the variety is limited. We serve Basa fish, which is boneless.",
                "source": "Menu and Drinks _ Barbeque Nation.pdf"
            },
            {
                "query": "What flavors of kulfi do you serve at Barbeque Nation?",
                "answer": "We serve six flavors of kulfi: Strawberry, Malai, Chocolate, Kesar Badam, Paan, and Mango.",
                "source": "Menu and Drinks _ Barbeque Nation.pdf"
            },
            {
                "query": "What non-veg starters are available that are not seafood?",
                "answer": "The non-veg starters available that are not seafood are Chicken Tangdi, Chicken Skewer, and Mutton.",
                "source": "Menu List _ Barbeque Nation.pdf"
            },
            {
                "query": "What is the address of the Barbeque Nation outlet in Indiranagar, Bangalore?",
                "answer": "The address is No.4005, HAL 2nd Stage, 100 Feet Road, Indiranagar, Bangalore-560038.",
                "source": "Bangalore _ Bengaluru - Indiranagar _ Barbeque Nation.pdf"
            },
            {
                "query": "Does the Indiranagar outlet have these facilities?",
                "answer": "Yes, the Indiranagar outlet has a bar and baby chairs available.",
                "source": "Bangalore _ Bengaluru - Indiranagar _ Barbeque Nation.pdf"
            },
            {
                "query": "For the Indiranagar outlet, what are the lunch timings on Saturday, and do they offer complimentary drinks?",
                "answer": "On Saturday, the lunch session at the Indiranagar outlet opens at 12:00 PM, with last entry at 3:00 PM, and closes at 4:00 PM. Yes, they offer complimentary drinks for lunch from Monday to Saturday, which includes 1 round of soft drink or mocktail.",
                "source": "Bangalore _ Bengaluru - Indiranagar _ Barbeque Nation.pdf"
            },
            {
                "query": "Does the JP Nagar outlet have baby chairs?",
                "answer": "Yes, the JP Nagar outlet has baby chairs available.",
                "source": "Bangalore _ JP Nagar _ Barbeque Nation.pdf"
            },
            {
                "query": "For the JP Nagar outlet, what is the address, and do they have a bar?",
                "answer": "The address of the JP Nagar outlet is 67, 3rd Floor, 6th B Main, Phase III, J P Nagar, Bengaluru, Karnataka 560078, India. Yes, they have a bar available.",
                "source": "Bangalore _ JP Nagar _ Barbeque Nation.pdf"
            },
            {
                "query": "What parking facilities does the Electronic City outlet offer?",
                "answer": "The Electronic City outlet offers self or chargeable parking.",
                "source": "Bangalore _ Electronic City _ Barbeque Nation.pdf"
            },
            {
                "query": "What are the dinner timings for the Koramangala 1st Block outlet on Sunday?",
                "answer": "The dinner session at the Koramangala 1st Block outlet opens at 6:30 PM, with last entry at 10:00 PM, and closes at 11:00 PM.",
                "source": "Bangalore _ Koramangala 1st Block _ Barbeque Nation.pdf"
            },
            {
                "query": "What are the dinner timings for the Connaught Place outlet in New Delhi?",
                "answer": "The dinner session at the Connaught Place outlet opens at 6:30 PM, with last entry at 10:00 PM, and closes at 11:00 PM.",
                "source": "New Delhi - Connaught Place _ CP _ cp _ Barbeque Nation.pdf"
            },
            {
                "query": "Is the Vasant Kunj outlet suitable?",
                "answer": "Yes, the Sector C, Vasant Kunj outlet has a bar available.",
                "source": "New Delhi - Sector C, Vasant Kunj _ Barbeque Nation.pdf"
            },
            {
                "query": "What are the dinner timings, and is there a bar available?",
                "answer": "The dinner session at the Sector C, Vasant Kunj outlet opens at 6:30 PM, with last entry at 10:00 PM, and closes at 11:00 PM. Yes, there is a bar available.",
                "source": "New Delhi - Sector C, Vasant Kunj _ Barbeque Nation.pdf"
            },
            {
                "query": "Does the Unity Mall, Janakpuri outlet have a private dining room?",
                "answer": "No, the Unity Mall, Janakpuri outlet does not have a private dining room available.",
                "source": "New Delhi - Unity Mall, Janakpuri _ Barbeque Nation.pdf"
            },
            {
                "query": "Which Bangalore outlets have valet parking, and do they all have the same menu?",
                "answer": "The Bangalore outlets in Indiranagar, JP Nagar, and Koramangala 1st Block have parking assistance for valet parking, while the Electronic City outlet has self or chargeable parking. Yes, all outlets have the same standard menu.",
                "source": "Outlet-specific documents and Menu and Drinks _ Barbeque Nation.pdf"
            },
            {
                "query": "Specifically, do both have baby chairs and lifts?",
                "answer": "Both the Indiranagar and Koramangala 1st Block outlets have baby chairs and lift availability.",
                "source": "Bangalore _ Bengaluru - Indiranagar _ Barbeque Nation.pdf and Bangalore _ Koramangala 1st Block _ Barbeque Nation.pdf"
            },
            {
                "query": "Which New Delhi outlets have valet parking, and do any of them offer early bird discounts?",
                "answer": "The Connaught Place and Sector C, Vasant Kunj outlets have parking assistance for valet parking, while the Unity Mall, Janakpuri outlet has self/mall parking/chargeable. None of the New Delhi outlets offer early bird discounts.",
                "source": "Outlet-specific documents"
            },
            {
                "query": "Compare the facilities at the Electronic City and Koramangala outlets in Bangalore. Which one has better parking options?",
                "answer": "The Electronic City outlet has self or chargeable parking, while the Koramangala 1st Block outlet has parking assistance. Therefore, the Koramangala outlet has better parking options with assistance.",
                "source": "Bangalore _ Electronic City _ Barbeque Nation.pdf and Bangalore _ Koramangala 1st Block _ Barbeque Nation.pdf"
            },
            {
                "query": "What non-veg main course options are available at Barbeque Nation?",
                "answer": "The non-veg main course options include Chicken, Mutton, Fish, Noodles, Oriental Non-Veg, and Non-Veg Biryani.",
                "source": "Menu List _ Barbeque Nation.pdf"
            },
            {
                "query": "What desserts do you offer?",
                "answer": "We offer a variety of desserts including Angori Gulab Jamun, Phirnee, Ice Cream, Pie/Tart, Fruits, Pastry, Brownie, and Pudding/Soufflé.",
                "source": "Menu List _ Barbeque Nation.pdf"
            },
            {
                "query": "Do you serve soups and salads at Barbeque Nation, and are they vegetarian?",
                "answer": "Yes, we serve soups and salads at Barbeque Nation, and they are vegetarian options.",
                "source": "Menu List _ Barbeque Nation.pdf"
            },
            {
                "query": "What types of drinks are available at Barbeque Nation?",
                "answer": "We offer soft drinks, mocktails, and alcoholic beverages at outlets with a bar.",
                "source": "Menu and Drinks _ Barbeque Nation.pdf"
            },
            {
                "query": "What spicy dishes do you have on the menu?",
                "answer": "For spicy food lovers, we have options like Cajun Spice Potato among the veg starters, and spicy variants of Chicken, Mutton, and Fish in the non-veg main courses.",
                "source": "Menu List _ Barbeque Nation.pdf"
            },
            {
                "query": "Does the Indiranagar outlet in Bangalore have a lift?",
                "answer": "Yes, the Indiranagar outlet has lift availability.",
                "source": "Bangalore _ Bengaluru - Indiranagar _ Barbeque Nation.pdf"
            },
            {
                "query": "Is the JP Nagar outlet noisy?",
                "answer": "The JP Nagar outlet is located on the 3rd floor of a building, which generally offers a quieter dining experience compared to street-level locations.",
                "source": "Bangalore _ JP Nagar _ Barbeque Nation.pdf"
            },
            {
                "query": "What is the seating capacity at the Electronic City outlet, and do they serve alcohol?",
                "answer": "The seating capacity at the Electronic City outlet is not specified, but it follows standard Barbeque Nation sizing. Yes, they serve alcohol as there is a bar available.",
                "source": "Bangalore _ Electronic City _ Barbeque Nation.pdf"
            },
            {
                "query": "Does the Koramangala 1st Block outlet have a bar?",
                "answer": "Yes, the Koramangala 1st Block outlet has a bar available.",
                "source": "Bangalore _ Koramangala 1st Block _ Barbeque Nation.pdf"
            },
            {
                "query": "Is the Indiranagar outlet good for families?",
                "answer": "Yes, the Indiranagar outlet is family-friendly with baby chairs and lift availability.",
                "source": "Bangalore _ Bengaluru - Indiranagar _ Barbeque Nation.pdf"
            },
            {
                "query": "Does the JP Nagar outlet have wheelchair access, and what are the dinner timings on Friday?",
                "answer": "Yes, the JP Nagar outlet has wheelchair access via a lift. The dinner session on Friday opens at 6:30 PM, with last entry at 10:00 PM, and closes at 11:00 PM.",
                "source": "Bangalore _ JP Nagar _ Barbeque Nation.pdf"
            },
            {
                "query": "What is the contact number for the Electronic City outlet?",
                "answer": "The contact number is not explicitly listed, but you can reach out via the central Barbeque Nation customer service or online booking system.",
                "source": "Bangalore _ Electronic City _ Barbeque Nation.pdf"
            },
            {
                "query": "Is the Koramangala 1st Block outlet usually crowded?",
                "answer": "The Koramangala 1st Block outlet can get crowded due to its popular location, especially on weekends, but booking in advance can help manage this.",
                "source": "Bangalore _ Koramangala 1st Block _ Barbeque Nation.pdf"
            },
            {
                "query": "What is the seating capacity of the Connaught Place outlet?",
                "answer": "The exact seating capacity isn't specified, but it follows Barbeque Nation's standard spacious layout suitable for large groups.",
                "source": "New Delhi - Connaught Place _ CP _ cp _ Barbeque Nation.pdf"
            },
            {
                "query": "What's the ambience like at the Vasant Kunj outlet?",
                "answer": "The Sector C, Vasant Kunj outlet offers a modern and comfortable ambience, enhanced by its bar and spacious seating.",
                "source": "New Delhi - Sector C, Vasant Kunj _ Barbeque Nation.pdf"
            },
            {
                "query": "Does the Unity Mall, Janakpuri outlet have a lift, and do they offer mocktails?",
                "answer": "Yes, the Unity Mall, Janakpuri outlet has a lift as it's in a mall. Yes, mocktails are available as part of the standard drink menu.",
                "source": "New Delhi - Unity Mall, Janakpuri _ Barbeque Nation.pdf"
            },
            {
                "query": "Can I book a table online for the Connaught Place outlet?",
                "answer": "Yes, you can book a table online for the Connaught Place outlet through the Barbeque Nation website or app.",
                "source": "General Barbeque Nation policy"
            },
            {
                "query": "Is the Unity Mall, Janakpuri outlet suitable for a group of 15?",
                "answer": "Yes, the Unity Mall, Janakpuri outlet is suitable for a group of 15 with its spacious seating, though it lacks a private dining room.",
                "source": "New Delhi - Unity Mall, Janakpuri _ Barbeque Nation.pdf"
            },
            {
                "query": "Does the Vasant Kunj outlet accept digital payments, and what are the lunch hours on Sunday?",
                "answer": "Yes, the Sector C, Vasant Kunj outlet accepts digital payments. Lunch hours on Sunday are from 12:00 PM to 4:00 PM, with last entry at 3:00 PM.",
                "source": "New Delhi - Sector C, Vasant Kunj _ Barbeque Nation.pdf"
            },
            # Adding more Q&A pairs from the dataset
            {
                "query": "Which Bangalore outlets have wheelchair access, and which one is easiest to reach?",
                "answer": "The Indiranagar, JP Nagar, and Koramangala 1st Block outlets have wheelchair access via lifts. The Indiranagar outlet is easiest to reach due to its location on 100 Feet Road, a well-connected area.",
                "source": "Outlet-specific documents"
            },
            {
                "query": "Which New Delhi outlets have a bar, and which one has the largest seating capacity?",
                "answer": "The Connaught Place and Sector C, Vasant Kunj outlets have bars. Connaught Place likely has the largest seating capacity due to its central, high-traffic location.",
                "source": "Outlet-specific documents"
            },
            {
                "query": "Which Bangalore outlets have baby chairs, and do they offer kid-friendly food?",
                "answer": "The Indiranagar, JP Nagar, and Koramangala 1st Block outlets have baby chairs. Yes, all outlets offer kid-friendly food like Noodles, Ice Cream, and mild-flavored starters.",
                "source": "Outlet-specific documents and Menu List _ Barbeque Nation.pdf"
            },
            {
                "query": "Which New Delhi outlets are open on Sunday evenings, and do they get crowded?",
                "answer": "All New Delhi outlets—Connaught Place, Sector C, Vasant Kunj, and Unity Mall, Janakpuri—are open on Sunday evenings from 6:30 PM to 11:00 PM. They can get crowded, especially Connaught Place, due to its popularity.",
                "source": "Outlet-specific documents"
            },
            {
                "query": "Which Bangalore outlets offer complimentary drinks, and what's included?",
                "answer": "The Indiranagar, JP Nagar, and Koramangala 1st Block outlets offer complimentary drinks for lunch from Monday to Saturday, including 1 round of soft drink or mocktail. Electronic City follows the same policy.",
                "source": "Outlet-specific documents"
            },
            {
                "query": "Which New Delhi outlets are near metro stations, and do they have parking?",
                "answer": "The Connaught Place outlet is near the Rajiv Chowk metro station and has valet parking. Unity Mall, Janakpuri is near the Janakpuri West metro station with self/mall parking. Vasant Kunj has valet parking but is farther from metro stations.",
                "source": "Outlet-specific documents"
            },
            {
                "query": "Are there any gluten-free options at Barbeque Nation?",
                "answer": "Yes, gluten-free options include grilled items like Paneer, Chicken, and Fish, as well as salads and fruits. Please inform the staff for specific preparations.",
                "source": "Menu List _ Barbeque Nation.pdf"
            },
            {
                "query": "What's available for celebrations?",
                "answer": "For celebrations, we offer a wide menu with starters, main courses, and desserts, plus a festive atmosphere. Some outlets have bars, and you can pre-book for groups.",
                "source": "Menu and Drinks _ Barbeque Nation.pdf"
            },
            {
                "query": "Can I customize my meal at Barbeque Nation, and what's the average cost per person?",
                "answer": "Yes, you can request customizations like Jain food or spice levels, subject to availability. The average cost per person varies by outlet but typically ranges from ₹800-₹1200 for lunch/dinner.",
                "source": "Menu and Drinks _ Barbeque Nation.pdf"
            },
            {
                "query": "Do all Barbeque Nation outlets have live grills?",
                "answer": "Yes, all Barbeque Nation outlets feature live grills at the table as part of the dining experience.",
                "source": "General Barbeque Nation policy"
            },
            {
                "query": "Do you offer takeaway options?",
                "answer": "Yes, Barbeque Nation offers takeaway options from all outlets. You can order from the menu via phone or online.",
                "source": "General Barbeque Nation policy"
            },
            {
                "query": "What are the peak hours at the Indiranagar outlet?",
                "answer": "Peak hours at the Indiranagar outlet are typically 1:00 PM - 2:30 PM for lunch and 7:30 PM - 9:30 PM for dinner, especially on weekends.",
                "source": "Bangalore _ Bengaluru - Indiranagar _ Barbeque Nation.pdf"
            },
            {
                "query": "Does the JP Nagar outlet have a good view?",
                "answer": "The JP Nagar outlet, located on the 3rd floor, offers a decent urban view of the surrounding area, though it's not a scenic highlight.",
                "source": "Bangalore _ JP Nagar _ Barbeque Nation.pdf"
            },
            {
                "query": "Is the Electronic City outlet noisy, and do they serve Basa fish?",
                "answer": "The Electronic City outlet may have moderate noise due to its location in a busy tech area. Yes, Basa fish is served as part of the standard menu.",
                "source": "Bangalore _ Electronic City _ Barbeque Nation.pdf and Menu and Drinks _ Barbeque Nation.pdf"
            },
            {
                "query": "What payment options are available at the Koramangala 1st Block outlet?",
                "answer": "The Koramangala 1st Block outlet accepts cash, card, and digital payments like UPI.",
                "source": "General Barbeque Nation policy"
            },
            {
                "query": "What's the typical wait time at Indiranagar?",
                "answer": "The wait time at Indiranagar varies but can be 15-30 minutes during peak hours without a reservation. Booking ahead reduces wait time.",
                "source": "Bangalore _ Bengaluru - Indiranagar _ Barbeque Nation.pdf"
            },
            {
                "query": "How many waitstaff are typically at the Connaught Place outlet?",
                "answer": "The Connaught Place outlet has a sufficient number of waitstaff to handle its busy crowd, though exact numbers aren't specified.",
                "source": "New Delhi - Connaught Place _ CP _ cp _ Barbeque Nation.pdf"
            },
            {
                "query": "Is the Vasant Kunj outlet quiet?",
                "answer": "The Sector C, Vasant Kunj outlet offers a relatively quiet dining experience due to its location away from central bustle.",
                "source": "New Delhi - Sector C, Vasant Kunj _ Barbeque Nation.pdf"
            },
            {
                "query": "Does the Unity Mall, Janakpuri outlet have baby chairs, and what are the lunch hours on Saturday?",
                "answer": "Yes, the Unity Mall, Janakpuri outlet has baby chairs. Lunch hours on Saturday are from 12:00 PM to 4:00 PM, with last entry at 3:00 PM.",
                "source": "New Delhi - Unity Mall, Janakpuri _ Barbeque Nation.pdf"
            },
            {
                "query": "Is the Connaught Place outlet noisy?",
                "answer": "Yes, the Connaught Place outlet can be noisy due to its central location and high footfall, especially during peak hours.",
                "source": "New Delhi - Connaught Place _ CP _ cp _ Barbeque Nation.pdf"
            },
            {
                "query": "Can I make a reservation at the Vasant Kunj outlet?",
                "answer": "Yes, you can make a reservation at the Sector C, Vasant Kunj outlet via the Barbeque Nation website or app.",
                "source": "General Barbeque Nation policy"
            },
            {
                "query": "Which Bangalore outlet is the most affordable, and do they all charge the same?",
                "answer": "Pricing is generally consistent across Bangalore outlets—Indiranagar, JP Nagar, Electronic City, and Koramangala 1st Block—at around ₹800-₹1200 per person, though Electronic City might be slightly cheaper due to its location.",
                "source": "General Barbeque Nation policy"
            },
            {
                "query": "Which New Delhi outlet has the best atmosphere, and do they all have bars?",
                "answer": "The Sector C, Vasant Kunj outlet offers the best atmosphere with a quieter, modern vibe. Only Connaught Place and Vasant Kunj have bars; Janakpuri does not.",
                "source": "Outlet-specific documents"
            },
            {
                "query": "Which Bangalore outlets allow online booking, and which is easiest to book?",
                "answer": "All Bangalore outlets—Indiranagar, JP Nagar, Electronic City, and Koramangala 1st Block—allow online booking. Indiranagar is typically easiest due to its high availability and popularity.",
                "source": "General Barbeque Nation policy"
            },
            {
                "query": "Which New Delhi outlets are best for families, and do they have baby chairs?",
                "answer": "The Sector C, Vasant Kunj and Unity Mall, Janakpuri outlets are best for families due to quieter settings and space. Both have baby chairs; Connaught Place does too but is noisier.",
                "source": "Outlet-specific documents"
            }
        ]
        return qa_pairs
    
    def _compute_embeddings(self):
        embeddings = []
        for qa in self.qa_pairs:
            embedding = self.model.encode(qa["query"])
            qa_with_embedding = qa.copy()
            qa_with_embedding["embedding"] = embedding
            embeddings.append(qa_with_embedding)
        return embeddings
    
    def query(self, question, threshold=0.6):
        question_embedding = self.model.encode(question)
        similarities = []
        
        for qa in self.qa_embeddings:
            similarity = np.dot(question_embedding, qa["embedding"])
            similarities.append((similarity, qa))
        
        # Sort by similarity score
        similarities.sort(key=lambda x: x[0], reverse=True)
        
        # Return the most similar answer if above threshold
        if similarities[0][0] >= threshold:
            return {
                "answer": similarities[0][1]["answer"],
                "source": similarities[0][1]["source"],
                "confidence": similarities[0][0]
            }
        else:
            return {
                "answer": "I'm sorry, I don't have enough information to answer that question accurately. Would you like to speak with a customer service representative?",
                "source": None,
                "confidence": similarities[0][0]
            }

# Initialize knowledge base
kb = KnowledgeBase()

# Google Sheets logger
class SheetLogger:
    def __init__(self):
        try:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open("BBQ Nation Logs").sheet1
            self.initialized = True
        except Exception as e:
            print(f"Error initializing Google Sheets: {e}")
            self.initialized = False
    
    def log(self, data):
        if not self.initialized:
            print("Logger not initialized, skipping log")
            return False
        
        try:
            self.sheet.append_row([
                data.get("timestamp", datetime.datetime.now().isoformat()),
                data.get("phone", ""),
                data.get("outcome", ""),
                data.get("summary", "")[:50]  # Truncate to 50 chars
            ])
            return True
        except Exception as e:
            print(f"Error logging to Google Sheets: {e}")
            return False

# Initialize logger
logger = SheetLogger()

# State machine definitions
class StateMachine:
    def __init__(self):
        self.states = {
            "start": {
                "template": "start.jinja",
                "transitions": {
                    "1": "collect_city",
                    "2": "collect_city",
                    "3": "knowledge_query",
                    "4": "feedback"
                }
            },
            "collect_city": {
                "template": "city_selection.jinja",
                "transitions": {
                    "1": "collect_location_bangalore",
                    "2": "collect_location_delhi",
                    "back": "start"
                }
            },
            "collect_location_bangalore": {
                "template": "location_bangalore.jinja",
                "transitions": {
                    "1": "main_options",  # Indiranagar
                    "2": "main_options",  # JP Nagar
                    "3": "main_options",  # Electronic City
                    "4": "main_options",  # Koramangala
                    "back": "collect_city"
                }
            },
            "collect_location_delhi": {
                "template": "location_delhi.jinja",
                "transitions": {
                    "1": "main_options",  # Connaught Place
                    "2": "main_options",  # Vasant Kunj
                    "3": "main_options",  # Janakpuri
                    "back": "collect_city"
                }
            },
            "main_options": {
                "template": "main_options.jinja",
                "transitions": {
                    "1": "new_booking",
                    "2": "modify_booking",
                    "3": "knowledge_query",
                    "4": "feedback",
                    "back": "collect_city"
                }
            },
            "new_booking": {
                "template": "new_booking.jinja",
                "transitions": {
                    "next": "collect_date",
                    "back": "main_options"
                }
            },
            "collect_date": {
                "template": "collect_date.jinja",
                "transitions": {
                    "next": "collect_time",
                    "back": "new_booking"
                },
                "validation": lambda x: bool(re.match(r"^\d{2}-\d{2}-\d{4}$", x))
            },
            "collect_time": {
                "template": "collect_time.jinja",
                "transitions": {
                    "1": "collect_guests",  # Lunch
                    "2": "collect_guests",  # Dinner
                    "back": "collect_date"
                }
            },
            "collect_guests": {
                "template": "collect_guests.jinja",
                "transitions": {
                    "next": "collect_phone",
                    "back": "collect_time"
                },
                "validation": lambda x: x.isdigit() and 1 <= int(x) <= 20
            },
            "collect_phone": {
                "template": "collect_phone.jinja",
                "transitions": {
                    "next": "booking_confirmation",
                    "back": "collect_guests"
                },
                "validation": lambda x: bool(re.match(r"^\d{10}$", x))
            },
            "booking_confirmation": {
                "template": "booking_confirmation.jinja",
                "transitions": {
                    "1": "booking_complete",  # Confirm
                    "2": "new_booking",      # Start over
                    "back": "collect_phone"
                }
            },
            "booking_complete": {
                "template": "booking_complete.jinja",
                "transitions": {
                    "1": "start",  # Back to start
                    "2": "end"     # End conversation
                }
            },
            "modify_booking": {
                "template": "modify_booking.jinja",
                "transitions": {
                    "next": "verify_reference",
                    "back": "main_options"
                }
            },
            "verify_reference": {
                "template": "verify_reference.jinja",
                "transitions": {
                    "next": "modification_options",
                    "back": "modify_booking"
                },
                "validation": lambda x: bool(re.match(r"^[A-Z0-9]{6}$", x))
            },
            "modification_options": {
                "template": "modification_options.jinja",
                "transitions": {
                    "1": "collect_date",      # Change date
                    "2": "collect_time",      # Change time
                    "3": "collect_guests",    # Change guests
                    "4": "cancel_booking",    # Cancel booking
                    "back": "verify_reference"
                }
            },
            "cancel_booking": {
                "template": "cancel_booking.jinja",
                "transitions": {
                    "1": "cancellation_complete",  # Confirm cancellation
                    "2": "modification_options",   # Back to modification options
                    "back": "modification_options"
                }
            },
            "cancellation_complete": {
                "template": "cancellation_complete.jinja",
                "transitions": {
                    "1": "start",  # Back to start
                    "2": "end"     # End conversation
                }
            },
            "knowledge_query": {
                "template": "knowledge_query.jinja",
                "transitions": {
                    "next": "knowledge_response",
                    "back": "main_options"
                }
            },
            "knowledge_response": {
                "template": "knowledge_response.jinja",
                "transitions": {
                    "1": "knowledge_query",  # Ask another question
                    "2": "main_options",     # Back to main options
                    "back": "knowledge_query"
                }
            },
            "feedback": {
                "template": "feedback.jinja",
                "transitions": {
                    "next": "collect_ratings",
                    "back": "main_options"
                }
            },
            "collect_ratings": {
                "template": "collect_ratings.jinja",
                "transitions": {
                    "next": "collect_comments",
                    "back": "feedback"
                },
                "validation": lambda x: x.isdigit() and 1 <= int(x) <= 5
            },
            "collect_comments": {
                "template": "collect_comments.jinja",
                "transitions": {
                    "next": "feedback_complete",
                    "back": "collect_ratings"
                }
            },
            "feedback_complete": {
                "template": "feedback_complete.jinja",
                "transitions": {
                    "1": "start",  # Back to start
                    "2": "end"     # End conversation
                }
            },
            "end": {
                "template": "end.jinja",
                "transitions": {}  # No transitions from end state
            }
        }
        
    def get_template(self, state):
        return self.states[state]["template"]
    
    def get_next_state(self, current_state, input_value):
        if current_state not in self.states:
            return "start"  # Default to start if invalid state
        
        transitions = self.states[current_state]["transitions"]
        
        # Check if input requires validation
        if "validation" in self.states[current_state]:
            validator = self.states[current_state]["validation"]
            if not validator(input_value):
                return current_state  # Stay in current state if validation fails
        
        # Process transition
        if input_value in transitions:
            return transitions[input_value]
        elif "next" in transitions and input_value.lower() != "back":
            return transitions["next"]
        else:
            return current_state  # Stay in current state if no valid transition

# Initialize state machine
state_machine = StateMachine()

# Jinja2 template environment
from jinja2 import Environment, FileSystemLoader
template_env = Environment(loader=FileSystemLoader('templates'))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    current_state = data.get('state', 'start')
    context = data.get('context', {})
    
    # Process knowledge query if in knowledge_query state
    if current_state == "knowledge_query":
        kb_response = kb.query(user_input)
        context['kb_response'] = kb_response
        next_state = "knowledge_response"
    else:
        # Normal state transition
        next_state = state_machine.get_next_state(current_state, user_input)
    
    # Update context based on user input and current state
    if current_state == "collect_city" and user_input == "1":
        context['city'] = "Bangalore"
    elif current_state == "collect_city" and user_input == "2":
        context['city'] = "Delhi"
    elif current_state == "collect_location_bangalore":
        locations = ["Indiranagar", "JP Nagar", "Electronic City", "Koramangala"]
        if user_input.isdigit() and 1 <= int(user_input) <= 4:
            context['location'] = locations[int(user_input) - 1]
    elif current_state == "collect_location_delhi":
        locations = ["Connaught Place", "Vasant Kunj", "Janakpuri"]
        if user_input.isdigit() and 1 <= int(user_input) <= 3:
            context['location'] = locations[int(user_input) - 1]
    elif current_state == "collect_date":
        context['date'] = user_input
    elif current_state == "collect_time":
        if user_input == "1":
            context['time_slot'] = "Lunch (12:00 PM - 4:00 PM)"
        elif user_input == "2":
            context['time_slot'] = "Dinner (6:30 PM - 11:00 PM)"
    elif current_state == "collect_guests":
        context['guests'] = user_input
    elif current_state == "collect_phone":
        context['phone'] = user_input
    elif current_state == "verify_reference":
        context['reference'] = user_input
    elif current_state == "collect_ratings":
        context['rating'] = user_input
    elif current_state == "collect_comments":
        context['comments'] = user_input
    
    # Log completed actions
    if current_state == "booking_complete":
        logger.log({
            "timestamp": datetime.datetime.now().isoformat(),
            "phone": context.get('phone', ''),
            "outcome": "new_booking",
            "summary": f"New booking at {context.get('location', '')} for {context.get('guests', '')} guests on {context.get('date', '')}"
        })
    elif current_state == "cancellation_complete":
        logger.log({
            "timestamp": datetime.datetime.now().isoformat(),
            "phone": context.get('phone', ''),
            "outcome": "cancellation",
            "summary": f"Cancelled booking {context.get('reference', '')}"
        })
    elif current_state == "feedback_complete":
        logger.log({
            "timestamp": datetime.datetime.now().isoformat(),
            "phone": context.get('phone', ''),
            "outcome": "feedback",
            "summary": f"Rating: {context.get('rating', '')}/5"
        })
    
    # Generate response using Jinja template
    template = template_env.get_template(state_machine.get_template(next_state))
    response_text = template.render(context=context)
    
    # Generate Retell response
    retell_response = {
        "response": response_text,
        "state": next_state,
        "context": context
    }
    
    return jsonify(retell_response)

if __name__ == '__main__':
    app.run(debug=True)
