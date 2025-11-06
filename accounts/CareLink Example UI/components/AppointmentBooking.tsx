import { ArrowLeft, Calendar as CalendarIcon, Clock, MapPin, User, Video, CheckCircle, Filter } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Calendar } from './ui/calendar';
import { useState } from 'react';
import { ImageWithFallback } from './figma/ImageWithFallback';

export function AppointmentBooking({ onNavigate }: { onNavigate: (page: string) => void }) {
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(new Date());
  const [showConfirmation, setShowConfirmation] = useState(false);

  const doctors = [
    {
      id: 1,
      name: 'Dr. Michael Chen',
      specialty: 'General Practice',
      rating: 4.9,
      reviews: 234,
      distance: '0.8 mi',
      nextAvailable: '2025-11-07 10:00 AM',
      image: 'https://images.unsplash.com/photo-1666886573421-d19e546cfc4e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZWRpY2FsJTIwaGVhbHRoY2FyZSUyMHByb2Zlc3Npb25hbHxlbnwxfHx8fDE3NjIzNTEyODZ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral'
    },
    {
      id: 2,
      name: 'Dr. Sarah Williams',
      specialty: 'Internal Medicine',
      rating: 4.8,
      reviews: 189,
      distance: '1.2 mi',
      nextAvailable: '2025-11-07 02:30 PM',
      image: 'https://images.unsplash.com/photo-1666886573421-d19e546cfc4e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZWRpY2FsJTIwaGVhbHRoY2FyZSUyMHByb2Zlc3Npb25hbHxlbnwxfHx8fDE3NjIzNTEyODZ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral'
    },
    {
      id: 3,
      name: 'Dr. James Anderson',
      specialty: 'Family Medicine',
      rating: 4.7,
      reviews: 156,
      distance: '2.1 mi',
      nextAvailable: '2025-11-08 09:00 AM',
      image: 'https://images.unsplash.com/photo-1666886573421-d19e546cfc4e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZWRpY2FsJTIwaGVhbHRoY2FyZSUyMHByb2Zlc3Npb25hbHxlbnwxfHx8fDE3NjIzNTEyODZ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral'
    },
  ];

  const timeSlots = [
    '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM',
    '11:00 AM', '11:30 AM', '02:00 PM', '02:30 PM',
    '03:00 PM', '03:30 PM', '04:00 PM', '04:30 PM'
  ];

  const handleBookAppointment = () => {
    setShowConfirmation(true);
    setTimeout(() => {
      setShowConfirmation(false);
      onNavigate('patient-dashboard');
    }, 3000);
  };

  if (showConfirmation) {
    return (
      <div className="min-h-screen bg-[#f7fbff] flex items-center justify-center p-4">
        <Card className="border-[#27ae60] max-w-md w-full">
          <CardContent className="pt-6 text-center">
            <div className="w-16 h-16 bg-[#27ae60] rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-10 h-10 text-white" />
            </div>
            <h2 className="text-2xl text-[#1f2937] mb-2">Appointment Confirmed!</h2>
            <p className="text-[#6b7280] mb-6">
              Your appointment has been successfully scheduled. You'll receive a confirmation email shortly.
            </p>
            <div className="bg-[#f7fbff] rounded-xl p-4 mb-6">
              <div className="flex items-center justify-between mb-3">
                <span className="text-[#6b7280]">Doctor:</span>
                <span className="text-[#1f2937]">Dr. Michael Chen</span>
              </div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-[#6b7280]">Date:</span>
                <span className="text-[#1f2937]">Nov 7, 2025</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[#6b7280]">Time:</span>
                <span className="text-[#1f2937]">10:00 AM</span>
              </div>
            </div>
            <Button 
              className="w-full bg-[#0d6efd] hover:bg-[#0b5ed7] text-white"
              onClick={() => onNavigate('patient-dashboard')}
            >
              Return to Dashboard
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#f7fbff]">
      {/* Header */}
      <header className="bg-white border-b border-[#e0e7ff]">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button 
                variant="ghost" 
                size="icon"
                onClick={() => onNavigate('patient-dashboard')}
              >
                <ArrowLeft className="w-5 h-5 text-[#6b7280]" />
              </Button>
              <div>
                <h2 className="text-[#1f2937]">Book Appointment</h2>
                <p className="text-sm text-[#6b7280]">Find and schedule with healthcare professionals</p>
              </div>
            </div>
            <Button variant="outline" className="border-[#0d6efd] text-[#0d6efd]">
              <Filter className="w-4 h-4 mr-2" />
              Filters
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Doctors List */}
          <div className="lg:col-span-2 space-y-6">
            <div>
              <h3 className="text-[#1f2937] mb-4">Available Doctors</h3>
              <div className="space-y-4">
                {doctors.map((doctor) => (
                  <Card key={doctor.id} className="border-[#e0e7ff] hover:shadow-lg transition-shadow">
                    <CardContent className="pt-6">
                      <div className="flex gap-4">
                        <div className="w-20 h-20 rounded-xl overflow-hidden bg-[#e5f1fb] flex-shrink-0">
                          <ImageWithFallback 
                            src={doctor.image}
                            alt={doctor.name}
                            className="w-full h-full object-cover"
                          />
                        </div>
                        <div className="flex-1">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              <h4 className="text-[#1f2937] mb-1">{doctor.name}</h4>
                              <p className="text-sm text-[#6b7280]">{doctor.specialty}</p>
                            </div>
                            <Badge className="bg-[#27ae60] text-white">
                              ★ {doctor.rating}
                            </Badge>
                          </div>
                          <div className="flex items-center gap-4 mb-3 text-sm text-[#6b7280]">
                            <div className="flex items-center gap-1">
                              <MapPin className="w-4 h-4" />
                              {doctor.distance}
                            </div>
                            <div className="flex items-center gap-1">
                              <User className="w-4 h-4" />
                              {doctor.reviews} reviews
                            </div>
                          </div>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2 text-sm">
                              <Clock className="w-4 h-4 text-[#2d9cdb]" />
                              <span className="text-[#6b7280]">Next: {doctor.nextAvailable}</span>
                            </div>
                            <div className="flex gap-2">
                              <Button 
                                size="sm" 
                                variant="outline" 
                                className="border-[#2d9cdb] text-[#2d9cdb]"
                              >
                                <Video className="w-4 h-4 mr-1" />
                                Virtual
                              </Button>
                              <Button 
                                size="sm" 
                                className="bg-[#0d6efd] hover:bg-[#0b5ed7] text-white"
                              >
                                Book Now
                              </Button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>

            {/* Time Slots */}
            <Card className="border-[#e0e7ff]">
              <CardHeader>
                <CardTitle className="text-[#1f2937]">Available Time Slots</CardTitle>
                <CardDescription className="text-[#6b7280]">
                  Select a convenient time for your appointment
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-3 md:grid-cols-4 gap-3">
                  {timeSlots.map((slot, index) => (
                    <Button
                      key={index}
                      variant={index === 2 ? 'default' : 'outline'}
                      className={
                        index === 2
                          ? 'bg-[#0d6efd] hover:bg-[#0b5ed7] text-white'
                          : 'border-[#e0e7ff] text-[#1f2937] hover:border-[#0d6efd] hover:text-[#0d6efd]'
                      }
                    >
                      {slot}
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Calendar */}
            <Card className="border-[#e0e7ff]">
              <CardHeader>
                <CardTitle className="text-[#1f2937] flex items-center gap-2">
                  <CalendarIcon className="w-5 h-5 text-[#0d6efd]" />
                  Select Date
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Calendar
                  mode="single"
                  selected={selectedDate}
                  onSelect={setSelectedDate}
                  className="rounded-md border-0"
                />
              </CardContent>
            </Card>

            {/* Booking Summary */}
            <Card className="border-[#e0e7ff] bg-gradient-to-br from-[#e5f1fb] to-white">
              <CardHeader>
                <CardTitle className="text-[#1f2937]">Booking Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between p-3 bg-white rounded-lg">
                  <span className="text-sm text-[#6b7280]">Appointment Type</span>
                  <span className="text-sm text-[#1f2937]">In-Person</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-white rounded-lg">
                  <span className="text-sm text-[#6b7280]">Duration</span>
                  <span className="text-sm text-[#1f2937]">30 minutes</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-white rounded-lg">
                  <span className="text-sm text-[#6b7280]">Consultation Fee</span>
                  <span className="text-sm text-[#1f2937]">$75</span>
                </div>
                <Button 
                  className="w-full bg-[#27ae60] hover:bg-[#229954] text-white mt-4"
                  onClick={handleBookAppointment}
                >
                  Confirm Appointment
                </Button>
              </CardContent>
            </Card>

            {/* Quick Info */}
            <Card className="border-[#2d9cdb] bg-[#f0f9ff]">
              <CardContent className="pt-6">
                <div className="flex gap-3">
                  <CalendarIcon className="w-5 h-5 text-[#2d9cdb] flex-shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-[#2d9cdb] mb-2">Same-Day Appointments</h4>
                    <p className="text-xs text-[#6b7280]">
                      Many of our doctors offer same-day appointments for urgent care needs.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
