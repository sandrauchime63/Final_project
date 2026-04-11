import json

data = {
    "school": "UNILAG",
    "faqs": [
      {
        "question": "What are the admission requirements?",
        "answer": "You need 5 credits including Maths and English."
      },
      {
        "question": "What is the tuition fee?",
        "answer": "₦100,000 per session."
      }
    ],
    "website": "https://unilag.edu.ng",
    "important_pages": {
      "admissions": "https://unilag.edu.ng/admissions",
      "courses": "https://unilag.edu.ng/courses"
    },
  "keywords": [
    "admission", 
    "fees", 
    "courses"
],
  "category": "admissions",
  "last_updated": "2026-04-06"
}
with open("Final_files/school_file.json", "w") as file:
    json.dump(data, file, indent=4)