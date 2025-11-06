import { Activity, FileText, MapPin, Calendar, User, LogOut, Home, ClipboardList } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';

export function PatientDashboard({ onNavigate }: { onNavigate: (page: string) => void }) {
  const triageHistory = [
    { id: 1, date: '2025-11-03', severity: 'Mild', condition: 'Common Cold', status: 'Completed' },
    { id: 2, date: '2025-10-28', severity: 'Moderate', condition: 'Allergic Reaction', status: 'Follow-up Needed' },
    { id: 3, date: '2025-10-15', severity: 'Mild', condition: 'Headache', status: 'Completed' },
  ];

  const nearbyClinics = [
    { name: 'City Medical Center', distance: '0.8 mi', specialty: 'General Practice' },
    { name: 'HealthPlus Urgent Care', distance: '1.2 mi', specialty: 'Urgent Care' },
    { name: 'Family Health Clinic', distance: '2.1 mi', specialty: 'Family Medicine' },
  ];

  return (
    <div className="min-h-screen bg-[#f7fbff]">
      {/* Header */}
      <header className="bg-white border-b border-[#e0e7ff] sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-8">
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 rounded-xl bg-[#0d6efd] flex items-center justify-center">
                  <Activity className="w-6 h-6 text-white" />
                </div>
                <h2 className="text-[#0d6efd]">CareLink</h2>
              </div>
              <nav className="hidden md:flex items-center gap-6">
                <button className="flex items-center gap-2 text-[#0d6efd]" onClick={() => onNavigate('landing')}>
                  <Home className="w-4 h-4" />
                  Home
                </button>
                <button className="flex items-center gap-2 text-[#6b7280] hover:text-[#0d6efd]" onClick={() => onNavigate('ai-triage')}>
                  <ClipboardList className="w-4 h-4" />
                  Triage
                </button>
                <button className="flex items-center gap-2 text-[#6b7280] hover:text-[#0d6efd]" onClick={() => onNavigate('profile')}>
                  <User className="w-4 h-4" />
                  My Profile
                </button>
                <button className="flex items-center gap-2 text-[#6b7280] hover:text-[#0d6efd]" onClick={() => onNavigate('appointments')}>
                  <Calendar className="w-4 h-4" />
                  Appointments
                </button>
              </nav>
            </div>
            <Button variant="ghost" className="text-[#6b7280]" onClick={() => onNavigate('landing')}>
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-[#0d6efd] to-[#2d9cdb] text-white">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl mb-2">Welcome back, Sarah!</h1>
              <p className="text-blue-100">How are you feeling today?</p>
            </div>
            <div className="hidden md:block bg-white/20 backdrop-blur-sm rounded-xl p-4">
              <p className="text-sm mb-1">Last check-in</p>
              <p>3 days ago</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Main Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* Quick Actions */}
            <div className="grid md:grid-cols-2 gap-4">
              <Card className="border-[#e0e7ff] hover:shadow-lg transition-shadow cursor-pointer" onClick={() => onNavigate('ai-triage')}>
                <CardHeader>
                  <div className="w-12 h-12 rounded-xl bg-[#0d6efd] flex items-center justify-center mb-3">
                    <Activity className="w-6 h-6 text-white" />
                  </div>
                  <CardTitle className="text-[#1f2937]">Start a New Triage</CardTitle>
                  <CardDescription className="text-[#6b7280]">
                    Get AI-powered symptom analysis in minutes
                  </CardDescription>
                </CardHeader>
              </Card>

              <Card className="border-[#e0e7ff] hover:shadow-lg transition-shadow cursor-pointer" onClick={() => onNavigate('appointments')}>
                <CardHeader>
                  <div className="w-12 h-12 rounded-xl bg-[#27ae60] flex items-center justify-center mb-3">
                    <Calendar className="w-6 h-6 text-white" />
                  </div>
                  <CardTitle className="text-[#1f2937]">Book Appointment</CardTitle>
                  <CardDescription className="text-[#6b7280]">
                    Schedule a visit with a healthcare professional
                  </CardDescription>
                </CardHeader>
              </Card>
            </div>

            {/* Triage History */}
            <Card className="border-[#e0e7ff]">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-[#1f2937]">Triage History</CardTitle>
                    <CardDescription className="text-[#6b7280]">Your recent health assessments</CardDescription>
                  </div>
                  <FileText className="w-5 h-5 text-[#6b7280]" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {triageHistory.map((record) => (
                    <div key={record.id} className="flex items-center justify-between p-4 bg-[#f7fbff] rounded-xl">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h4 className="text-[#1f2937]">{record.condition}</h4>
                          <Badge 
                            variant={record.severity === 'Mild' ? 'secondary' : 'default'}
                            className={
                              record.severity === 'Mild' 
                                ? 'bg-[#27ae60] text-white' 
                                : 'bg-[#f59e0b] text-white'
                            }
                          >
                            {record.severity}
                          </Badge>
                        </div>
                        <p className="text-sm text-[#6b7280]">{record.date}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-[#6b7280]">{record.status}</p>
                      </div>
                    </div>
                  ))}
                </div>
                <Button variant="outline" className="w-full mt-4 border-[#0d6efd] text-[#0d6efd]">
                  View All History
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Nearby Clinics */}
            <Card className="border-[#e0e7ff]">
              <CardHeader>
                <div className="flex items-center gap-2 mb-2">
                  <MapPin className="w-5 h-5 text-[#2d9cdb]" />
                  <CardTitle className="text-[#1f2937]">Nearby Clinics</CardTitle>
                </div>
                <CardDescription className="text-[#6b7280]">Healthcare facilities near you</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {nearbyClinics.map((clinic, index) => (
                    <div key={index} className="p-3 bg-[#f7fbff] rounded-lg">
                      <h4 className="text-[#1f2937] mb-1">{clinic.name}</h4>
                      <div className="flex items-center justify-between">
                        <p className="text-sm text-[#6b7280]">{clinic.specialty}</p>
                        <Badge variant="outline" className="border-[#2d9cdb] text-[#2d9cdb]">
                          {clinic.distance}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
                <Button className="w-full mt-4 bg-[#2d9cdb] hover:bg-[#2686b8] text-white">
                  View on Map
                </Button>
              </CardContent>
            </Card>

            {/* Health Tips */}
            <Card className="border-[#e0e7ff] bg-gradient-to-br from-[#e5f1fb] to-white">
              <CardHeader>
                <CardTitle className="text-[#1f2937]">Today's Health Tip</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-[#6b7280] mb-4">
                  Stay hydrated! Drinking 8 glasses of water daily helps maintain optimal body function and supports your immune system.
                </p>
                <Button variant="link" className="text-[#0d6efd] p-0">
                  Read more tips →
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
