import { Heart, MessageSquare, MapPin, Calendar, Shield, Activity } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { ImageWithFallback } from './figma/ImageWithFallback';

export function LandingPage({ onNavigate }: { onNavigate: (page: string) => void }) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-[#f7fbff] to-white">
      {/* Header */}
      <header className="border-b border-[#e0e7ff] bg-white">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-xl bg-[#0d6efd] flex items-center justify-center">
              <Heart className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-[#0d6efd]">CareLink</h1>
              <p className="text-xs text-[#6b7280]">AI-Enhanced Telehealth Triage</p>
            </div>
          </div>
          <Button 
            variant="outline" 
            className="border-[#0d6efd] text-[#0d6efd] hover:bg-[#0d6efd] hover:text-white"
            onClick={() => onNavigate('patient-dashboard')}
          >
            Sign In
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <div className="inline-block px-4 py-2 bg-[#e5f1fb] rounded-full">
              <p className="text-sm text-[#0d6efd]">AI-Powered Healthcare at Your Fingertips</p>
            </div>
            <h1 className="text-4xl md:text-5xl text-[#1f2937]">
              Your Health, <span className="text-[#0d6efd]">Our Priority</span>
            </h1>
            <p className="text-lg text-[#6b7280]">
              Get instant AI-powered symptom analysis, find nearby care facilities, and book appointments with trusted healthcare professionals.
            </p>
            <div className="flex gap-4">
              <Button 
                className="bg-[#0d6efd] hover:bg-[#0b5ed7] text-white px-8 py-6"
                onClick={() => onNavigate('ai-triage')}
              >
                <Activity className="w-5 h-5 mr-2" />
                Start Triage
              </Button>
              <Button 
                variant="outline" 
                className="border-[#2d9cdb] text-[#2d9cdb] hover:bg-[#2d9cdb] hover:text-white px-8 py-6"
                onClick={() => onNavigate('patient-dashboard')}
              >
                Learn More
              </Button>
            </div>
          </div>
          <div className="relative">
            <div className="rounded-2xl overflow-hidden shadow-2xl">
              <ImageWithFallback 
                src="https://images.unsplash.com/photo-1758691462860-b1b9532c7394?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkb2N0b3IlMjBwYXRpZW50JTIwdGVsZWhlYWx0aHxlbnwxfHx8fDE3NjIzOTYyMTJ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                alt="Telehealth consultation"
                className="w-full h-auto object-cover"
              />
            </div>
            <div className="absolute -bottom-6 -left-6 bg-white p-4 rounded-xl shadow-lg">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-[#27ae60] flex items-center justify-center">
                  <Shield className="w-6 h-6 text-white" />
                </div>
                <div>
                  <p className="text-sm text-[#1f2937]">HIPAA Compliant</p>
                  <p className="text-xs text-[#6b7280]">Your data is secure</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl text-[#1f2937] mb-4">How CareLink Helps You</h2>
          <p className="text-[#6b7280] max-w-2xl mx-auto">
            Our AI-powered platform makes healthcare accessible, efficient, and patient-centered.
          </p>
        </div>
        <div className="grid md:grid-cols-3 gap-8">
          <Card className="border-[#e0e7ff] hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="w-14 h-14 rounded-xl bg-[#e5f1fb] flex items-center justify-center mb-4">
                <MessageSquare className="w-7 h-7 text-[#0d6efd]" />
              </div>
              <CardTitle className="text-[#1f2937]">AI Symptom Analysis</CardTitle>
              <CardDescription className="text-[#6b7280]">
                Describe your symptoms and get instant AI-powered health assessment
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-[#e0e7ff] hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="w-14 h-14 rounded-xl bg-[#d4f4e2] flex items-center justify-center mb-4">
                <MapPin className="w-7 h-7 text-[#27ae60]" />
              </div>
              <CardTitle className="text-[#1f2937]">Find Nearby Care</CardTitle>
              <CardDescription className="text-[#6b7280]">
                Locate the nearest clinics and hospitals based on your condition
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-[#e0e7ff] hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="w-14 h-14 rounded-xl bg-[#dbeafe] flex items-center justify-center mb-4">
                <Calendar className="w-7 h-7 text-[#2d9cdb]" />
              </div>
              <CardTitle className="text-[#1f2937]">Book Appointments</CardTitle>
              <CardDescription className="text-[#6b7280]">
                Schedule visits with healthcare professionals at your convenience
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-[#e0e7ff] mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 rounded-lg bg-[#0d6efd] flex items-center justify-center">
                  <Heart className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-[#1f2937]">CareLink</h3>
              </div>
              <p className="text-sm text-[#6b7280]">
                AI-Enhanced Telehealth Triage for better healthcare access
              </p>
            </div>
            <div>
              <h4 className="text-[#1f2937] mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-[#6b7280]">
                <li><a href="#" className="hover:text-[#0d6efd]">Features</a></li>
                <li><a href="#" className="hover:text-[#0d6efd]">Pricing</a></li>
                <li><a href="#" className="hover:text-[#0d6efd]">Security</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-[#1f2937] mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-[#6b7280]">
                <li><a href="#" className="hover:text-[#0d6efd]">About Us</a></li>
                <li><a href="#" className="hover:text-[#0d6efd]">Careers</a></li>
                <li><a href="#" className="hover:text-[#0d6efd]">Contact</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-[#1f2937] mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-[#6b7280]">
                <li><a href="#" className="hover:text-[#0d6efd]">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-[#0d6efd]">Terms of Service</a></li>
                <li><a href="#" className="hover:text-[#0d6efd]">HIPAA Compliance</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-[#e0e7ff] mt-8 pt-8 text-center text-sm text-[#6b7280]">
            <p>&copy; 2025 CareLink. All rights reserved. Not for collecting PII or sensitive medical data.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
