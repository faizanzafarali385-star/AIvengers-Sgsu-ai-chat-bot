# SGSU Chatbot - Training Update

## ✅ Successfully Trained with SGSU University Data

Your AI chatbot has been successfully trained with comprehensive information from **SCOPE Global Skills University (SGSU)** website.

---

## 📊 What Was Updated

### Knowledge Base Categories Added:

1. **About SGSU** (4 Q&A pairs)
   - University information and accreditation
   - Location and contact details
   - Institution reputation and recognition

2. **Academics & Programs** (5 Q&A pairs)
   - 11+ faculties offered
   - Undergraduate, Postgraduate, and PhD programs
   - Faculty-specific information

3. **Admissions & Enrollment** (4 Q&A pairs)
   - Application process
   - Admission requirements
   - When admissions are open
   - How to apply

4. **Placements & Career** (4 Q&A pairs)
   - SGSU placement record
   - Internship and apprenticeship programs
   - Major recruiters (TCS, Infosys, Amazon, etc.)
   - Industry preparation

5. **Campus Facilities & Infrastructure** (4 Q&A pairs)
   - State-of-the-art labs and equipment
   - Wi-Fi enabled campus
   - Sports and recreation facilities
   - Canteen and student amenities

6. **Industry Partnerships & Accreditation** (3 Q&A pairs)
   - Skill council affiliations
   - Industry partnerships
   - UGC accreditation details

7. **Contact & Support** (5 Q&A pairs)
   - Contact information
   - Social media links
   - Grievance registration
   - Anti-ragging committee

---

## 🎯 Total Knowledge Base Content:

- **29 SGSU-specific Q&A pairs** across 7 categories
- **6 fallback responses** for unknown questions
- **Industry partner information** (NIIT, TCS, Infosys, Amazon, TATA, etc.)
- **All contact details** and links
- **Complete program information**

---

## 🧪 Tested Q&A Examples:

### Q: "What is SGSU?"
**A:** "SCOPE Global Skills University (SGSU) is Central India's first skills university, established in 2023. It's accredited by UGC and part of the AISECT Group."
- **Confidence:** 50%

### Q: "What faculties does SGSU offer?"
**A:** "SGSU offers 11+ faculties: Engineering & Technology Skills, Emerging Technologies, Information Technology & Future Skills, Management Studies, Banking Finance & Commerce, Education & Training, Fashion Technology & Interior Design, Medical & Allied Sciences, Agriculture & Allied Technologies, Mass Communication, Humanities & Liberal Arts, and Sustainable Development Studies."
- **Confidence:** 67%

### Q: "How do I apply to SGSU?"
**A:** "To apply to SGSU, visit the website at https://sgsuniversity.ac.in/enquire-now/ or https://sgsuniversity.ac.in/admission/. You can submit your enquiry online."
- **Confidence:** 71%

### Q: "Where is SGSU located?"
**A:** "SGSU Campus is located at NH-12, Near Misrod, Hoshangabad Road, Bhopal, Madhya Pradesh, India. Contact: +91-7552432903/904."
- **Confidence:** 60%

### Q: "What is SGSU placement record?"
**A:** "SGSU has an excellent placement record with strong industry partnerships. Major recruiters include NIIT, TCS, Infosys, Amazon, TATA, Edelweiss, JustDial, Bajaj Finserv, IndusInd Bank, Paytm, and more."
- **Confidence:** 67%

---

## 🚀 Try These Questions in the Chatbot:

1. "What is SGSU?"
2. "What faculties does SGSU offer?"
3. "What programs does SGSU have?"
4. "How do I apply to SGSU?"
5. "When is admission open?"
6. "What is the admission process?"
7. "Does SGSU offer internships?"
8. "What is SGSU placement record?"
9. "Where is SGSU located?"
10. "How do I contact SGSU?"
11. "What are SGSU placement partners?"
12. "Is SGSU UGC approved?"
13. "What facilities does SGSU have?"
14. "Does SGSU have sports facilities?"
15. "Can I follow SGSU on social media?"

---

## 📁 Files Modified:

- **knowledge_base.json** - Updated with 29 new SGSU-specific Q&A pairs

## 📁 Files Running:

- **main.py** - FastAPI backend (restarted with new KB)
- **serve_frontend.py** - Frontend HTTP server
- **index.html** - Chatbot UI

---

## 🌐 Access the Chatbot:

- **Frontend:** http://localhost:8080
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

---

## 🔧 How the Training Works:

1. **Website Content Fetched** - Extracted from https://sgsuniversity.ac.in/
2. **Q&A Pairs Created** - Manually crafted based on website information
3. **Keywords Assigned** - Each Q&A has relevant keywords for matching
4. **Similarity Algorithm** - Backend matches user questions to Q&As
5. **Confidence Scoring** - Shows how confident the bot is in its answer

---

## 📈 Next Steps:

### To Add More Information:
1. Edit `knowledge_base.json`
2. Add new Q&A pairs in relevant categories
3. Include keywords for better matching
4. Restart the backend

### Example: Adding a New Q&A

```json
{
  "question": "what is agriculture program at sgsu",
  "keywords": ["agriculture", "agriculture technology", "farming", "agri"],
  "answer": "SGSU's Faculty of Agriculture & Allied Technologies offers comprehensive programs in agricultural science, farm management, and sustainable farming practices."
}
```

### To Deploy to Cloud:
1. Follow the guide in `DEPLOY_RENDER.md`
2. Push updated `knowledge_base.json` to GitHub
3. Render will auto-deploy with new content

---

## 📞 SGSU Contact Information (from KB):

**Phone:** +91-7552432903/904, +91-7552432909
**Email:** info@sgsuniversity.ac.in
**Address:** SCOPE Campus, NH-12, Near Misrod, Hoshangabad Road, Bhopal
**Website:** https://sgsuniversity.ac.in/

**Social Media:**
- Facebook: facebook.com/sgsuniversity
- Twitter: twitter.com/sgsuniversity
- LinkedIn: linkedin.com/company/sgsuniversity
- Instagram: instagram.com/sgsuniversity
- YouTube: youtube.com/@SGSUniversity

---

## ✨ Features:

✅ SGSU-specific information
✅ 29 Q&A pairs covering all major topics
✅ Industry partner information
✅ Admission guidance
✅ Placement information
✅ Campus facilities details
✅ Contact information
✅ Social media links
✅ Confidence scoring
✅ Smooth UI with animations

---

## 🎉 Your Chatbot is Ready!

The chatbot is now fully trained to answer questions about SGSU and can serve as a helpful resource for prospective students, current students, and anyone interested in the university.

**Start chatting:** http://localhost:8080
