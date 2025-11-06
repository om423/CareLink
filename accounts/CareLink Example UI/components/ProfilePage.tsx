import { ArrowLeft, User, Save, AlertCircle, Lock, Mail } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Textarea } from './ui/textarea';

export function ProfilePage({ onNavigate }: { onNavigate: (page: string) => void }) {
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
                <h2 className="text-[#1f2937]">My Profile</h2>
                <p className="text-sm text-[#6b7280]">Manage your personal information</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Profile Header */}
        <Card className="border-[#e0e7ff] mb-6">
          <CardContent className="pt-6">
            <div className="flex items-center gap-6">
              <div className="w-24 h-24 rounded-full bg-gradient-to-br from-[#0d6efd] to-[#2d9cdb] flex items-center justify-center">
                <User className="w-12 h-12 text-white" />
              </div>
              <div className="flex-1">
                <h2 className="text-2xl text-[#1f2937] mb-1">Sarah Johnson</h2>
                <p className="text-[#6b7280] mb-2">sarah.johnson@email.com</p>
                <Button variant="outline" size="sm" className="border-[#0d6efd] text-[#0d6efd]">
                  Change Photo
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Tabs */}
        <Tabs defaultValue="basic" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 bg-white border border-[#e0e7ff]">
            <TabsTrigger 
              value="basic"
              className="data-[state=active]:bg-[#0d6efd] data-[state=active]:text-white"
            >
              Basic Info
            </TabsTrigger>
            <TabsTrigger 
              value="medical"
              className="data-[state=active]:bg-[#0d6efd] data-[state=active]:text-white"
            >
              Medical History
            </TabsTrigger>
            <TabsTrigger 
              value="settings"
              className="data-[state=active]:bg-[#0d6efd] data-[state=active]:text-white"
            >
              Settings
            </TabsTrigger>
          </TabsList>

          {/* Basic Info Tab */}
          <TabsContent value="basic">
            <Card className="border-[#e0e7ff]">
              <CardHeader>
                <CardTitle className="text-[#1f2937]">Personal Information</CardTitle>
                <CardDescription className="text-[#6b7280]">
                  Update your personal details and contact information
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="firstName" className="text-[#1f2937]">First Name</Label>
                    <Input 
                      id="firstName" 
                      defaultValue="Sarah" 
                      className="border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="lastName" className="text-[#1f2937]">Last Name</Label>
                    <Input 
                      id="lastName" 
                      defaultValue="Johnson" 
                      className="border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                    />
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="dob" className="text-[#1f2937]">Date of Birth</Label>
                    <Input 
                      id="dob" 
                      type="date" 
                      defaultValue="1990-05-15" 
                      className="border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="gender" className="text-[#1f2937]">Gender</Label>
                    <Input 
                      id="gender" 
                      defaultValue="Female" 
                      className="border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                    />
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="phone" className="text-[#1f2937]">Phone Number</Label>
                    <Input 
                      id="phone" 
                      type="tel" 
                      defaultValue="(555) 123-4567" 
                      className="border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email" className="text-[#1f2937]">Email</Label>
                    <Input 
                      id="email" 
                      type="email" 
                      defaultValue="sarah.johnson@email.com" 
                      className="border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="address" className="text-[#1f2937]">Address</Label>
                  <Input 
                    id="address" 
                    defaultValue="123 Main Street, San Francisco, CA 94102" 
                    className="border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                  />
                </div>

                <Button className="bg-[#27ae60] hover:bg-[#229954] text-white">
                  <Save className="w-4 h-4 mr-2" />
                  Save Changes
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Medical History Tab */}
          <TabsContent value="medical">
            <div className="space-y-6">
              <Card className="border-[#e0e7ff]">
                <CardHeader>
                  <CardTitle className="text-[#1f2937]">Medical Information</CardTitle>
                  <CardDescription className="text-[#6b7280]">
                    Keep your medical history up to date for better care
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <Label htmlFor="height" className="text-[#1f2937]">Height (cm)</Label>
                      <Input 
                        id="height" 
                        type="number" 
                        defaultValue="165" 
                        className="border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="weight" className="text-[#1f2937]">Weight (kg)</Label>
                      <Input 
                        id="weight" 
                        type="number" 
                        defaultValue="60" 
                        className="border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="bloodType" className="text-[#1f2937]">Blood Type</Label>
                    <Input 
                      id="bloodType" 
                      defaultValue="A+" 
                      className="border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="allergies" className="text-[#1f2937]">Allergies</Label>
                    <Textarea 
                      id="allergies" 
                      placeholder="List any allergies (medications, foods, environmental)"
                      defaultValue="Penicillin, Peanuts"
                      className="min-h-[100px] border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="conditions" className="text-[#1f2937]">Chronic Conditions</Label>
                    <Textarea 
                      id="conditions" 
                      placeholder="List any ongoing medical conditions"
                      defaultValue="Asthma"
                      className="min-h-[100px] border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="medications" className="text-[#1f2937]">Current Medications</Label>
                    <Textarea 
                      id="medications" 
                      placeholder="List medications you're currently taking"
                      defaultValue="Albuterol inhaler as needed"
                      className="min-h-[100px] border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                    />
                  </div>

                  <Button className="bg-[#27ae60] hover:bg-[#229954] text-white">
                    <Save className="w-4 h-4 mr-2" />
                    Save Medical Information
                  </Button>
                </CardContent>
              </Card>

              <Card className="border-[#f59e0b] bg-[#fffbeb]">
                <CardContent className="pt-6">
                  <div className="flex gap-3">
                    <AlertCircle className="w-5 h-5 text-[#f59e0b] flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="text-[#f59e0b] mb-1">Important</h4>
                      <p className="text-sm text-[#6b7280]">
                        Always keep your medical information current. This helps healthcare providers give you the best possible care.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Settings Tab */}
          <TabsContent value="settings">
            <div className="space-y-6">
              <Card className="border-[#e0e7ff]">
                <CardHeader>
                  <CardTitle className="text-[#1f2937]">Account Settings</CardTitle>
                  <CardDescription className="text-[#6b7280]">
                    Manage your account security and preferences
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-2">
                    <Label htmlFor="currentEmail" className="text-[#1f2937]">Email Address</Label>
                    <div className="flex gap-2">
                      <Input 
                        id="currentEmail" 
                        type="email" 
                        defaultValue="sarah.johnson@email.com" 
                        className="border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                      />
                      <Button variant="outline" className="border-[#0d6efd] text-[#0d6efd]">
                        <Mail className="w-4 h-4 mr-2" />
                        Change
                      </Button>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label className="text-[#1f2937]">Password</Label>
                    <Button variant="outline" className="w-full justify-start border-[#e0e7ff]">
                      <Lock className="w-4 h-4 mr-2" />
                      Change Password
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-[#e0e7ff]">
                <CardHeader>
                  <CardTitle className="text-[#1f2937]">Privacy & Notifications</CardTitle>
                  <CardDescription className="text-[#6b7280]">
                    Control how we communicate with you
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-[#f7fbff] rounded-lg">
                    <div>
                      <h4 className="text-[#1f2937] mb-1">Email Notifications</h4>
                      <p className="text-sm text-[#6b7280]">Receive updates about your health</p>
                    </div>
                    <input type="checkbox" defaultChecked className="w-5 h-5 text-[#0d6efd]" />
                  </div>

                  <div className="flex items-center justify-between p-4 bg-[#f7fbff] rounded-lg">
                    <div>
                      <h4 className="text-[#1f2937] mb-1">SMS Reminders</h4>
                      <p className="text-sm text-[#6b7280]">Get appointment reminders via text</p>
                    </div>
                    <input type="checkbox" defaultChecked className="w-5 h-5 text-[#0d6efd]" />
                  </div>

                  <div className="flex items-center justify-between p-4 bg-[#f7fbff] rounded-lg">
                    <div>
                      <h4 className="text-[#1f2937] mb-1">Marketing Emails</h4>
                      <p className="text-sm text-[#6b7280]">Receive health tips and updates</p>
                    </div>
                    <input type="checkbox" className="w-5 h-5 text-[#0d6efd]" />
                  </div>
                </CardContent>
              </Card>

              <Card className="border-[#ef4444]">
                <CardHeader>
                  <CardTitle className="text-[#ef4444]">Danger Zone</CardTitle>
                  <CardDescription className="text-[#6b7280]">
                    Irreversible actions for your account
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button variant="destructive" className="bg-[#ef4444] hover:bg-[#dc2626]">
                    Delete Account
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
