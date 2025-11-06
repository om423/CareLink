import { useState } from 'react';
import { LandingPage } from './components/LandingPage';
import { PatientDashboard } from './components/PatientDashboard';
import { DoctorDashboard } from './components/DoctorDashboard';
import { AITriage } from './components/AITriage';
import { ProfilePage } from './components/ProfilePage';
import { AppointmentBooking } from './components/AppointmentBooking';
import { StyleGuide } from './components/StyleGuide';

type Page = 'landing' | 'patient-dashboard' | 'doctor-dashboard' | 'ai-triage' | 'profile' | 'appointments' | 'style-guide';

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('landing');

  const handleNavigate = (page: string) => {
    setCurrentPage(page as Page);
  };

  return (
    <div className="min-h-screen">
      {currentPage === 'landing' && <LandingPage onNavigate={handleNavigate} />}
      {currentPage === 'patient-dashboard' && <PatientDashboard onNavigate={handleNavigate} />}
      {currentPage === 'doctor-dashboard' && <DoctorDashboard onNavigate={handleNavigate} />}
      {currentPage === 'ai-triage' && <AITriage onNavigate={handleNavigate} />}
      {currentPage === 'profile' && <ProfilePage onNavigate={handleNavigate} />}
      {currentPage === 'appointments' && <AppointmentBooking onNavigate={handleNavigate} />}
      {currentPage === 'style-guide' && <StyleGuide onNavigate={handleNavigate} />}

      {/* Quick Navigation Menu (Developer Helper) */}
      <div className="fixed bottom-4 right-4 bg-white border-2 border-[#0d6efd] rounded-xl shadow-2xl p-4 z-50">
        <p className="text-xs text-[#6b7280] mb-3">Quick Navigation</p>
        <div className="flex flex-col gap-2">
          <button
            onClick={() => setCurrentPage('landing')}
            className={`text-xs px-3 py-2 rounded-lg text-left transition-colors ${
              currentPage === 'landing' 
                ? 'bg-[#0d6efd] text-white' 
                : 'bg-[#f7fbff] text-[#1f2937] hover:bg-[#e5f1fb]'
            }`}
          >
            1️⃣ Landing
          </button>
          <button
            onClick={() => setCurrentPage('patient-dashboard')}
            className={`text-xs px-3 py-2 rounded-lg text-left transition-colors ${
              currentPage === 'patient-dashboard' 
                ? 'bg-[#0d6efd] text-white' 
                : 'bg-[#f7fbff] text-[#1f2937] hover:bg-[#e5f1fb]'
            }`}
          >
            2️⃣ Patient Dashboard
          </button>
          <button
            onClick={() => setCurrentPage('doctor-dashboard')}
            className={`text-xs px-3 py-2 rounded-lg text-left transition-colors ${
              currentPage === 'doctor-dashboard' 
                ? 'bg-[#0d6efd] text-white' 
                : 'bg-[#f7fbff] text-[#1f2937] hover:bg-[#e5f1fb]'
            }`}
          >
            3️⃣ Doctor Dashboard
          </button>
          <button
            onClick={() => setCurrentPage('ai-triage')}
            className={`text-xs px-3 py-2 rounded-lg text-left transition-colors ${
              currentPage === 'ai-triage' 
                ? 'bg-[#0d6efd] text-white' 
                : 'bg-[#f7fbff] text-[#1f2937] hover:bg-[#e5f1fb]'
            }`}
          >
            4️⃣ AI Triage
          </button>
          <button
            onClick={() => setCurrentPage('profile')}
            className={`text-xs px-3 py-2 rounded-lg text-left transition-colors ${
              currentPage === 'profile' 
                ? 'bg-[#0d6efd] text-white' 
                : 'bg-[#f7fbff] text-[#1f2937] hover:bg-[#e5f1fb]'
            }`}
          >
            5️⃣ Profile
          </button>
          <button
            onClick={() => setCurrentPage('appointments')}
            className={`text-xs px-3 py-2 rounded-lg text-left transition-colors ${
              currentPage === 'appointments' 
                ? 'bg-[#0d6efd] text-white' 
                : 'bg-[#f7fbff] text-[#1f2937] hover:bg-[#e5f1fb]'
            }`}
          >
            6️⃣ Appointments
          </button>
          <button
            onClick={() => setCurrentPage('style-guide')}
            className={`text-xs px-3 py-2 rounded-lg text-left transition-colors ${
              currentPage === 'style-guide' 
                ? 'bg-[#27ae60] text-white' 
                : 'bg-[#f7fbff] text-[#1f2937] hover:bg-[#e5f1fb]'
            }`}
          >
            7️⃣ Style Guide
          </button>
        </div>
      </div>
    </div>
  );
}
