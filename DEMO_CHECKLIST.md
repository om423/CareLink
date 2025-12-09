# CareLink Demo Checklist - User Stories Demonstration

## Demo Logins

### Patient Account
- **Username:** `ompatel`
- **Password:** `password123`
- **Name:** Om Patel

### Doctor Account
- **Username:** `ritwij` (or `gautam`, `varsha`, `rlafeldt2`)
- **Password:** `password123`
- **Name:** Ritwij Ghosh (or gautam valiveti, Varsha Kantheti, Doctor Lafeldt)

### Admin Account (for User Story #12)
- **Username:** `admin`
- **Password:** `admin123`

---

## User Stories Demo Flow

### **User Story #1: Patient Profile Creation**
**As a patient, I want to create a personal profile containing my age, weight, medical history, and allergies so that the AI triage can provide more accurate assessments.**

**Demo Steps:**
1. ✅ Log in as patient (`ompatel` / `password123`)
2. ✅ Navigate to "My Profile" in the navbar
3. ✅ Show the profile form with fields:
   - Age
   - Weight
   - Medical History
   - Allergies
4. ✅ Fill in sample data (e.g., Age: 28, Weight: 150 lbs, Medical History: "Hypertension", Allergies: "Penicillin")
5. ✅ Save the profile
6. ✅ **Key Point:** Explain that this data will be used to enhance AI triage accuracy

---

### **User Story #2: AI-Based Preliminary Diagnosis**
**As a patient, I want to describe my symptoms in plain language so that I can receive an AI-based preliminary diagnosis.**

**Demo Steps:**
1. ✅ Log in as patient (`ompatel` / `password123`)
2. ✅ Navigate to "AI Triage" or "New Assessment" in the navbar
3. ✅ Show the chat interface
4. ✅ Type symptoms in plain language, e.g.:
   - "I've been having chest pain for the past 2 hours, and I feel short of breath"
   - "I have a persistent headache and feel nauseous"
5. ✅ Show the AI response with:
   - Summary of symptoms
   - Possible causes
   - Red flags to watch for
   - Recommended actions
6. ✅ **Key Point:** Emphasize natural language input and AI-powered analysis

---

### **User Story #3: View Nearby Clinics and Doctors on Map**
**As a patient, I want to view nearby clinics and doctors on a map so that I can choose where to seek care.**

**Demo Steps:**
1. ✅ Log in as patient (`ompatel` / `password123`)
2. ✅ Navigate to "Find a Doctor" in the navbar
3. ✅ Show the interactive map with doctor markers
4. ✅ Click on a doctor marker to show:
   - Doctor name and specialty
   - Clinic name and address
   - Consultation fee
   - Years of experience
5. ✅ Show distance filtering (if implemented)
6. ✅ Zoom in/out to show doctors across different cities
7. ✅ **Key Point:** Highlight the geographic distribution (211 doctors across the US)

---

### **User Story #4: Estimated Severity Levels**
**As a patient, I want to receive estimated severity levels for my symptoms so I can decide whether to visit an ER or clinic.**

**Demo Steps:**
1. ✅ Log in as patient (`ompatel` / `password123`)
2. ✅ Navigate to "AI Triage" and submit symptoms
3. ✅ Show the severity badge (Mild/Moderate/Severe/Critical) with color coding:
   - **Mild:** Green
   - **Moderate:** Yellow
   - **Severe:** Orange
   - **Critical:** Red
4. ✅ Navigate to "Triage History" and show different severity levels
5. ✅ Click on a triage detail to show the full assessment
6. ✅ **Key Point:** Explain how severity helps patients decide on care urgency

---

### **User Story #5: Book Appointments Online**
**As a patient, I want to book appointments online directly from the platform to save time.**

**Demo Steps:**
1. ✅ Log in as patient (`ompatel` / `password123`)
2. ✅ Navigate to "Appointments" in the navbar
3. ✅ Show the doctor selection interface
4. ✅ Select a doctor and specialty filter
5. ✅ Choose appointment date and time
6. ✅ Fill in appointment reason
7. ✅ Submit the booking
8. ✅ Show the appointment confirmation
9. ✅ Navigate to "My Appointments" to show the booked appointment
10. ✅ **Key Point:** Demonstrate seamless online booking workflow

---

### **User Story #6: Review Triage History**
**As a patient, I want to review my AI-generated triage history for personal tracking.**

**Demo Steps:**
1. ✅ Log in as patient (`ompatel` / `password123`)
2. ✅ Navigate to "Triage History" in the navbar
3. ✅ Show the list of past triage interactions with:
   - Date and time
   - Symptoms summary
   - Severity level
   - Status
4. ✅ Click on a specific triage to show:
   - Full symptom description
   - Complete AI assessment
   - Severity details
   - Doctor notes (if any)
5. ✅ **Key Point:** Show how patients can track their health over time

---

### **User Story #7: Doctor Dashboard - View Triage Reports**
**As a doctor/admin, I want to view incoming triage reports so I can prioritize high-risk patients.**

**Demo Steps:**
1. ✅ Log out and log in as doctor (`ritwij` / `password123`)
2. ✅ Navigate to "Doctor Portal" or "Triage Dashboard"
3. ✅ Show the dashboard with:
   - List of triage reports
   - Severity indicators (Critical/Severe highlighted)
   - Patient information
   - Timestamps
   - Review status
4. ✅ Show sorting/filtering by severity
5. ✅ Click on a high-severity (Critical/Severe) report
6. ✅ **Key Point:** Emphasize prioritization by severity for urgent cases

---

### **User Story #8: Doctor Notes on Triage Reports**
**As a doctor/admin, I want to add professional notes or feedback to AI-generated triage reports for accuracy.**

**Demo Steps:**
1. ✅ Log in as doctor (`ritwij` / `password123`)
2. ✅ Navigate to "Triage Dashboard"
3. ✅ Click on a triage report to view details
4. ✅ Scroll to "Doctor Notes / Feedback" section
5. ✅ Add professional notes, e.g.:
   - "Patient should follow up in 48 hours"
   - "AI assessment is accurate, recommend ER visit"
   - "Consider additional tests for differential diagnosis"
6. ✅ Save the notes (AJAX - no page refresh)
7. ✅ Show that notes are saved and timestamped
8. ✅ **Key Point:** Show how doctors can add clinical context to AI assessments

---

### **User Story #9: Manage Availability and Clinic Information**
**As a doctor/admin, I want to manage my availability and clinic information displayed on the platform.**

**Demo Steps:**
1. ✅ Log in as doctor (`ritwij` / `password123`)
2. ✅ Navigate to doctor profile or settings (if available)
3. ✅ Show clinic information:
   - Clinic name
   - Address
   - Specialty
   - Consultation fee
   - Years of experience
4. ✅ Show availability management (if implemented in DoctorAvailability model)
5. ✅ **Note:** If not fully implemented, explain that the model exists and can be extended
6. ✅ **Key Point:** Show how doctors can manage their presence on the platform

---

### **User Story #10: Verify Data Integrity**
**As a doctor/admin, I want to verify patient-reported symptoms against actual medical records for data integrity.**

**Demo Steps:**
1. ✅ Log in as doctor (`ritwij` / `password123`)
2. ✅ Navigate to a triage report detail page
3. ✅ Show the data integrity verification section (if visible in UI)
4. ✅ If not in UI, explain the backend functionality:
   - `data_integrity_status` field (pending/verified/discrepancy)
   - `data_integrity_notes` field
   - `verify_integrity` endpoint exists
5. ✅ **Alternative:** Show in Django admin panel
6. ✅ **Key Point:** Explain how doctors can flag discrepancies between patient reports and medical records

---

### **User Story #11: Platform Performance Metrics**
**As an admin, I want to monitor overall platform performance and user satisfaction metrics.**

**Demo Steps:**
1. ✅ Log in as admin (`admin` / `admin123`)
2. ✅ Navigate to Django Admin panel (`/admin/`)
3. ✅ Show available metrics:
   - Total users (patients and doctors)
   - Total triage interactions
   - Triage interactions by severity
   - Appointments booked
   - Doctor notes added
4. ✅ **Note:** If custom dashboard not implemented, show Django admin statistics
5. ✅ **Key Point:** Explain how admins can monitor platform health

---

### **User Story #12: Manage User Accounts and Permissions**
**As an admin, I want to manage user accounts, permissions, and access levels so that I can maintain secure and organized platform operations.**

**Demo Steps:**
1. ✅ Log in as admin (`admin` / `admin123`)
2. ✅ Navigate to Django Admin panel (`/admin/`)
3. ✅ Show user management:
   - List of all users
   - User roles (patient/doctor)
   - Staff status
   - Superuser status
4. ✅ Create/edit a user:
   - Change role
   - Grant/revoke staff permissions
   - Set superuser status
5. ✅ Show PatientProfile management with CSV export
6. ✅ Show Group and Permission management
7. ✅ **Key Point:** Demonstrate comprehensive admin control over user access

---

## Quick Demo Tips

### **Before Starting:**
- ✅ Ensure server is running: `python manage.py runserver`
- ✅ Have both patient and doctor accounts ready
- ✅ Create at least 1-2 sample triage interactions as patient before demo
- ✅ Book at least 1 appointment as patient before demo

### **Demo Flow Suggestions:**
1. **Start with Patient Journey:**
   - Login → Profile → Triage → History → Find Doctor → Book Appointment

2. **Switch to Doctor Journey:**
   - Login → Dashboard → View Triage → Add Notes → Verify Integrity

3. **End with Admin:**
   - Login → Admin Panel → User Management → Metrics

### **Key Talking Points:**
- ✅ **AI Integration:** Google Gemini API for intelligent symptom analysis
- ✅ **Geographic Coverage:** 211 doctors across major US cities
- ✅ **Role-Based Access:** Separate patient and doctor interfaces
- ✅ **Data Integrity:** Verification system for medical accuracy
- ✅ **User Experience:** Clean, medical-themed UI with intuitive navigation

---

## Troubleshooting

- **If AI triage doesn't work:** Check `GEMINI_API_KEY` is set in environment
- **If map doesn't load:** Check browser console for JavaScript errors
- **If doctors don't appear:** Run `python manage.py geocode_doctors`
- **If appointments fail:** Ensure DoctorProfile exists for selected doctor

---

## Additional Features to Highlight

- ✅ **Real-time Chat Interface:** Smooth, conversational AI interaction
- ✅ **Severity Color Coding:** Visual indicators for urgency
- ✅ **Patient Context Integration:** AI uses profile data for better assessments
- ✅ **Doctor Dashboard Prioritization:** Critical cases highlighted first
- ✅ **AJAX Notes Saving:** Seamless doctor feedback without page refresh
- ✅ **Comprehensive Admin Panel:** Full control over platform data

