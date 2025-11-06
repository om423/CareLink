import { Activity, AlertTriangle, Calendar, Bell, User, LogOut, Users, ClipboardList } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';

export function DoctorDashboard({ onNavigate }: { onNavigate: (page: string) => void }) {
  const triageReports = [
    { 
      id: 1, 
      patientName: 'John Smith', 
      age: 45, 
      severity: 'High', 
      condition: 'Chest Pain', 
      timestamp: '2025-11-06 09:23 AM',
      status: 'Pending Review'
    },
    { 
      id: 2, 
      patientName: 'Emma Johnson', 
      age: 32, 
      severity: 'Moderate', 
      condition: 'Persistent Cough', 
      timestamp: '2025-11-06 08:45 AM',
      status: 'Under Review'
    },
    { 
      id: 3, 
      patientName: 'Michael Brown', 
      age: 28, 
      severity: 'Mild', 
      condition: 'Headache', 
      timestamp: '2025-11-06 07:30 AM',
      status: 'Completed'
    },
    { 
      id: 4, 
      patientName: 'Sarah Davis', 
      age: 56, 
      severity: 'High', 
      condition: 'Difficulty Breathing', 
      timestamp: '2025-11-05 11:15 PM',
      status: 'Pending Review'
    },
  ];

  return (
    <div className="min-h-screen bg-[#f7fbff]">
      {/* Header */}
      <header className="bg-white border-b border-[#e0e7ff] sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-[#0d6efd] flex items-center justify-center">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-[#0d6efd]">CareLink</h2>
                <p className="text-xs text-[#6b7280]">Doctor Portal</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" className="relative">
                <Bell className="w-5 h-5 text-[#6b7280]" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-[#ef4444] rounded-full"></span>
              </Button>
              <Button variant="ghost" className="flex items-center gap-2 text-[#6b7280]">
                <User className="w-5 h-5" />
                <span className="hidden md:inline">Dr. Anderson</span>
              </Button>
              <Button variant="ghost" onClick={() => onNavigate('landing')}>
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        {/* Overview Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <Card className="border-[#e0e7ff]">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardDescription className="text-[#6b7280]">Incoming Reports</CardDescription>
                <ClipboardList className="w-5 h-5 text-[#0d6efd]" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-3xl text-[#1f2937] mb-1">24</div>
              <p className="text-sm text-[#27ae60]">+6 today</p>
            </CardContent>
          </Card>

          <Card className="border-[#e0e7ff] border-l-4 border-l-[#ef4444]">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardDescription className="text-[#6b7280]">High-Risk Patients</CardDescription>
                <AlertTriangle className="w-5 h-5 text-[#ef4444]" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-3xl text-[#1f2937] mb-1">8</div>
              <p className="text-sm text-[#ef4444]">Requires immediate attention</p>
            </CardContent>
          </Card>

          <Card className="border-[#e0e7ff]">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardDescription className="text-[#6b7280]">Active Patients</CardDescription>
                <Users className="w-5 h-5 text-[#2d9cdb]" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-3xl text-[#1f2937] mb-1">156</div>
              <p className="text-sm text-[#6b7280]">Total under care</p>
            </CardContent>
          </Card>

          <Card className="border-[#e0e7ff] bg-gradient-to-br from-[#27ae60] to-[#229954] text-white cursor-pointer hover:shadow-lg transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardDescription className="text-white/90">Availability</CardDescription>
                <Calendar className="w-5 h-5 text-white" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl mb-1">Available</div>
              <p className="text-sm text-white/90">Click to manage schedule</p>
            </CardContent>
          </Card>
        </div>

        {/* Triage Reports Table */}
        <Card className="border-[#e0e7ff]">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-[#1f2937]">Recent Triage Reports</CardTitle>
                <CardDescription className="text-[#6b7280]">Patient assessments requiring review</CardDescription>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" className="border-[#0d6efd] text-[#0d6efd]">
                  Filter
                </Button>
                <Button className="bg-[#0d6efd] hover:bg-[#0b5ed7] text-white">
                  Export Report
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow className="border-[#e0e7ff]">
                  <TableHead className="text-[#1f2937]">Patient Name</TableHead>
                  <TableHead className="text-[#1f2937]">Age</TableHead>
                  <TableHead className="text-[#1f2937]">Condition</TableHead>
                  <TableHead className="text-[#1f2937]">Severity</TableHead>
                  <TableHead className="text-[#1f2937]">Timestamp</TableHead>
                  <TableHead className="text-[#1f2937]">Status</TableHead>
                  <TableHead className="text-right text-[#1f2937]">Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {triageReports.map((report) => (
                  <TableRow key={report.id} className="border-[#e0e7ff] hover:bg-[#f7fbff]">
                    <TableCell className="text-[#1f2937]">{report.patientName}</TableCell>
                    <TableCell className="text-[#6b7280]">{report.age}</TableCell>
                    <TableCell className="text-[#1f2937]">{report.condition}</TableCell>
                    <TableCell>
                      <Badge 
                        className={
                          report.severity === 'High' 
                            ? 'bg-[#ef4444] text-white' 
                            : report.severity === 'Moderate'
                            ? 'bg-[#f59e0b] text-white'
                            : 'bg-[#27ae60] text-white'
                        }
                      >
                        {report.severity}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-[#6b7280]">{report.timestamp}</TableCell>
                    <TableCell>
                      <Badge 
                        variant="outline"
                        className={
                          report.status === 'Pending Review'
                            ? 'border-[#ef4444] text-[#ef4444]'
                            : report.status === 'Under Review'
                            ? 'border-[#f59e0b] text-[#f59e0b]'
                            : 'border-[#27ae60] text-[#27ae60]'
                        }
                      >
                        {report.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button 
                        size="sm" 
                        variant="ghost" 
                        className="text-[#0d6efd] hover:bg-[#e5f1fb]"
                      >
                        Review
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <div className="grid md:grid-cols-2 gap-6 mt-8">
          <Card className="border-[#e0e7ff]">
            <CardHeader>
              <CardTitle className="text-[#1f2937]">Today's Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-[#f7fbff] rounded-lg">
                  <span className="text-[#6b7280]">Reports Reviewed</span>
                  <span className="text-[#1f2937]">12 / 24</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-[#f7fbff] rounded-lg">
                  <span className="text-[#6b7280]">Appointments Scheduled</span>
                  <span className="text-[#1f2937]">8</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-[#f7fbff] rounded-lg">
                  <span className="text-[#6b7280]">Follow-ups Required</span>
                  <span className="text-[#1f2937]">5</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-[#e0e7ff] bg-gradient-to-br from-[#e5f1fb] to-white">
            <CardHeader>
              <CardTitle className="text-[#1f2937]">Clinical Notes</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-[#6b7280] mb-4">
                Remember to review the high-risk patient cases first. Pay special attention to any chest pain or breathing difficulty reports.
              </p>
              <Button variant="outline" className="w-full border-[#0d6efd] text-[#0d6efd]">
                Add New Note
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
