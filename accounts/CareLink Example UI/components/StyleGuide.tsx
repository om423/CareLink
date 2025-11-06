import { ArrowLeft, Heart, Activity, MapPin, Calendar, User, AlertTriangle, CheckCircle, Info, Bell } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Alert, AlertDescription, AlertTitle } from './ui/alert';
import { Input } from './ui/input';
import { Label } from './ui/label';

export function StyleGuide({ onNavigate }: { onNavigate: (page: string) => void }) {
  return (
    <div className="min-h-screen bg-[#f7fbff]">
      {/* Header */}
      <header className="bg-white border-b border-[#e0e7ff] sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              size="icon"
              onClick={() => onNavigate('landing')}
            >
              <ArrowLeft className="w-5 h-5 text-[#6b7280]" />
            </Button>
            <div>
              <h2 className="text-[#1f2937]">CareLink Design System</h2>
              <p className="text-sm text-[#6b7280]">Component & Style Guide</p>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Color Palette */}
        <section className="mb-12">
          <h2 className="text-2xl text-[#1f2937] mb-6">Color Palette</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Card className="border-[#e0e7ff]">
              <CardHeader>
                <CardTitle className="text-[#1f2937]">Primary Colors</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-16 h-16 rounded-xl bg-[#0d6efd] border-2 border-white shadow-md"></div>
                  <div>
                    <p className="text-sm text-[#1f2937]">Medical Blue</p>
                    <p className="text-xs text-[#6b7280]">#0d6efd</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-16 h-16 rounded-xl bg-[#2d9cdb] border-2 border-white shadow-md"></div>
                  <div>
                    <p className="text-sm text-[#1f2937]">Trust Teal</p>
                    <p className="text-xs text-[#6b7280]">#2d9cdb</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-16 h-16 rounded-xl bg-[#27ae60] border-2 border-white shadow-md"></div>
                  <div>
                    <p className="text-sm text-[#1f2937]">Healing Green</p>
                    <p className="text-xs text-[#6b7280]">#27ae60</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-[#e0e7ff]">
              <CardHeader>
                <CardTitle className="text-[#1f2937]">Neutrals</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-16 h-16 rounded-xl bg-[#f7fbff] border-2 border-[#e0e7ff] shadow-md"></div>
                  <div>
                    <p className="text-sm text-[#1f2937]">Soft White</p>
                    <p className="text-xs text-[#6b7280]">#f7fbff</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-16 h-16 rounded-xl bg-[#1f2937] border-2 border-white shadow-md"></div>
                  <div>
                    <p className="text-sm text-[#1f2937]">Muted Gray</p>
                    <p className="text-xs text-[#6b7280]">#1f2937</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-16 h-16 rounded-xl bg-[#6b7280] border-2 border-white shadow-md"></div>
                  <div>
                    <p className="text-sm text-[#1f2937]">Medium Gray</p>
                    <p className="text-xs text-[#6b7280]">#6b7280</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-[#e0e7ff]">
              <CardHeader>
                <CardTitle className="text-[#1f2937]">Status Colors</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-16 h-16 rounded-xl bg-[#f59e0b] border-2 border-white shadow-md"></div>
                  <div>
                    <p className="text-sm text-[#1f2937]">Warning Amber</p>
                    <p className="text-xs text-[#6b7280]">#f59e0b</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-16 h-16 rounded-xl bg-[#ef4444] border-2 border-white shadow-md"></div>
                  <div>
                    <p className="text-sm text-[#1f2937]">Danger Red</p>
                    <p className="text-xs text-[#6b7280]">#ef4444</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Typography */}
        <section className="mb-12">
          <h2 className="text-2xl text-[#1f2937] mb-6">Typography</h2>
          <Card className="border-[#e0e7ff]">
            <CardContent className="pt-6 space-y-6">
              <div>
                <h1 className="text-[#1f2937] mb-2">Heading 1</h1>
                <p className="text-sm text-[#6b7280]">Used for page titles and hero sections</p>
              </div>
              <div>
                <h2 className="text-[#1f2937] mb-2">Heading 2</h2>
                <p className="text-sm text-[#6b7280]">Used for section titles</p>
              </div>
              <div>
                <h3 className="text-[#1f2937] mb-2">Heading 3</h3>
                <p className="text-sm text-[#6b7280]">Used for card titles and subsections</p>
              </div>
              <div>
                <p className="text-[#1f2937] mb-2">Body Text</p>
                <p className="text-sm text-[#6b7280]">Used for general content and descriptions. Should be readable and comfortable for extended reading.</p>
              </div>
              <div>
                <p className="text-sm text-[#6b7280]">Caption Text</p>
                <p className="text-xs text-[#6b7280]">Used for labels, metadata, and supplementary information</p>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Buttons */}
        <section className="mb-12">
          <h2 className="text-2xl text-[#1f2937] mb-6">Buttons</h2>
          <Card className="border-[#e0e7ff]">
            <CardContent className="pt-6">
              <div className="space-y-6">
                <div>
                  <h3 className="text-[#1f2937] mb-4">Primary Buttons</h3>
                  <div className="flex flex-wrap gap-3">
                    <Button className="bg-[#0d6efd] hover:bg-[#0b5ed7] text-white">
                      Primary Blue
                    </Button>
                    <Button className="bg-[#2d9cdb] hover:bg-[#2686b8] text-white">
                      Secondary Teal
                    </Button>
                    <Button className="bg-[#27ae60] hover:bg-[#229954] text-white">
                      Success Green
                    </Button>
                    <Button className="bg-[#ef4444] hover:bg-[#dc2626] text-white">
                      Danger Red
                    </Button>
                  </div>
                </div>

                <div>
                  <h3 className="text-[#1f2937] mb-4">Outline Buttons</h3>
                  <div className="flex flex-wrap gap-3">
                    <Button variant="outline" className="border-[#0d6efd] text-[#0d6efd]">
                      Outline Blue
                    </Button>
                    <Button variant="outline" className="border-[#2d9cdb] text-[#2d9cdb]">
                      Outline Teal
                    </Button>
                    <Button variant="outline" className="border-[#27ae60] text-[#27ae60]">
                      Outline Green
                    </Button>
                  </div>
                </div>

                <div>
                  <h3 className="text-[#1f2937] mb-4">Button with Icons</h3>
                  <div className="flex flex-wrap gap-3">
                    <Button className="bg-[#0d6efd] hover:bg-[#0b5ed7] text-white">
                      <Heart className="w-4 h-4 mr-2" />
                      With Icon
                    </Button>
                    <Button variant="outline" className="border-[#0d6efd] text-[#0d6efd]">
                      <Calendar className="w-4 h-4 mr-2" />
                      Book Now
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Badges */}
        <section className="mb-12">
          <h2 className="text-2xl text-[#1f2937] mb-6">Badges</h2>
          <Card className="border-[#e0e7ff]">
            <CardContent className="pt-6">
              <div className="flex flex-wrap gap-3">
                <Badge className="bg-[#27ae60] text-white">Mild</Badge>
                <Badge className="bg-[#f59e0b] text-white">Moderate</Badge>
                <Badge className="bg-[#ef4444] text-white">Severe</Badge>
                <Badge variant="outline" className="border-[#0d6efd] text-[#0d6efd]">Active</Badge>
                <Badge variant="outline" className="border-[#6b7280] text-[#6b7280]">Pending</Badge>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Icons */}
        <section className="mb-12">
          <h2 className="text-2xl text-[#1f2937] mb-6">Medical Icons</h2>
          <Card className="border-[#e0e7ff]">
            <CardContent className="pt-6">
              <div className="grid grid-cols-3 md:grid-cols-6 gap-6">
                <div className="text-center">
                  <div className="w-14 h-14 rounded-xl bg-[#e5f1fb] flex items-center justify-center mx-auto mb-2">
                    <Heart className="w-7 h-7 text-[#0d6efd]" />
                  </div>
                  <p className="text-xs text-[#6b7280]">Heart</p>
                </div>
                <div className="text-center">
                  <div className="w-14 h-14 rounded-xl bg-[#e5f1fb] flex items-center justify-center mx-auto mb-2">
                    <Activity className="w-7 h-7 text-[#0d6efd]" />
                  </div>
                  <p className="text-xs text-[#6b7280]">Activity</p>
                </div>
                <div className="text-center">
                  <div className="w-14 h-14 rounded-xl bg-[#dbeafe] flex items-center justify-center mx-auto mb-2">
                    <MapPin className="w-7 h-7 text-[#2d9cdb]" />
                  </div>
                  <p className="text-xs text-[#6b7280]">Location</p>
                </div>
                <div className="text-center">
                  <div className="w-14 h-14 rounded-xl bg-[#dbeafe] flex items-center justify-center mx-auto mb-2">
                    <Calendar className="w-7 h-7 text-[#2d9cdb]" />
                  </div>
                  <p className="text-xs text-[#6b7280]">Calendar</p>
                </div>
                <div className="text-center">
                  <div className="w-14 h-14 rounded-xl bg-[#d4f4e2] flex items-center justify-center mx-auto mb-2">
                    <User className="w-7 h-7 text-[#27ae60]" />
                  </div>
                  <p className="text-xs text-[#6b7280]">User</p>
                </div>
                <div className="text-center">
                  <div className="w-14 h-14 rounded-xl bg-[#fee2e2] flex items-center justify-center mx-auto mb-2">
                    <AlertTriangle className="w-7 h-7 text-[#ef4444]" />
                  </div>
                  <p className="text-xs text-[#6b7280]">Alert</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Alerts */}
        <section className="mb-12">
          <h2 className="text-2xl text-[#1f2937] mb-6">Alerts</h2>
          <div className="space-y-4">
            <Alert className="border-[#0d6efd] bg-[#eff6ff]">
              <Info className="w-5 h-5 text-[#0d6efd]" />
              <AlertTitle className="text-[#0d6efd]">Information</AlertTitle>
              <AlertDescription className="text-[#1f2937]">
                This is an informational message to provide helpful context.
              </AlertDescription>
            </Alert>

            <Alert className="border-[#27ae60] bg-[#f0fdf4]">
              <CheckCircle className="w-5 h-5 text-[#27ae60]" />
              <AlertTitle className="text-[#27ae60]">Success</AlertTitle>
              <AlertDescription className="text-[#1f2937]">
                Your action was completed successfully!
              </AlertDescription>
            </Alert>

            <Alert className="border-[#f59e0b] bg-[#fffbeb]">
              <AlertTriangle className="w-5 h-5 text-[#f59e0b]" />
              <AlertTitle className="text-[#f59e0b]">Warning</AlertTitle>
              <AlertDescription className="text-[#1f2937]">
                Please review this information carefully before proceeding.
              </AlertDescription>
            </Alert>

            <Alert className="border-[#ef4444] bg-[#fef2f2]">
              <AlertTriangle className="w-5 h-5 text-[#ef4444]" />
              <AlertTitle className="text-[#ef4444]">Error</AlertTitle>
              <AlertDescription className="text-[#1f2937]">
                Something went wrong. Please try again or contact support.
              </AlertDescription>
            </Alert>
          </div>
        </section>

        {/* Cards */}
        <section className="mb-12">
          <h2 className="text-2xl text-[#1f2937] mb-6">Cards</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <Card className="border-[#e0e7ff] hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="w-12 h-12 rounded-xl bg-[#0d6efd] flex items-center justify-center mb-3">
                  <Activity className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-[#1f2937]">Standard Card</CardTitle>
                <CardDescription className="text-[#6b7280]">
                  Default card with icon, title, and description
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-[#e0e7ff] bg-gradient-to-br from-[#e5f1fb] to-white">
              <CardHeader>
                <div className="w-12 h-12 rounded-xl bg-[#2d9cdb] flex items-center justify-center mb-3">
                  <Bell className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-[#1f2937]">Gradient Card</CardTitle>
                <CardDescription className="text-[#6b7280]">
                  Card with gradient background for emphasis
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </section>

        {/* Forms */}
        <section className="mb-12">
          <h2 className="text-2xl text-[#1f2937] mb-6">Form Elements</h2>
          <Card className="border-[#e0e7ff]">
            <CardContent className="pt-6 space-y-6">
              <div className="space-y-2">
                <Label htmlFor="example-input" className="text-[#1f2937]">Label</Label>
                <Input 
                  id="example-input" 
                  placeholder="Input field" 
                  className="border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="example-input-filled" className="text-[#1f2937]">Filled Input</Label>
                <Input 
                  id="example-input-filled" 
                  defaultValue="Example value" 
                  className="border-[#e0e7ff] focus-visible:ring-[#0d6efd]"
                />
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Design Principles */}
        <section>
          <h2 className="text-2xl text-[#1f2937] mb-6">Design Principles</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Card className="border-[#e0e7ff]">
              <CardHeader>
                <CardTitle className="text-[#1f2937]">Calm & Trustworthy</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-[#6b7280]">
                  Use soft colors, generous spacing, and rounded corners to create a welcoming, stress-free healthcare experience.
                </p>
              </CardContent>
            </Card>

            <Card className="border-[#e0e7ff]">
              <CardHeader>
                <CardTitle className="text-[#1f2937]">Clear & Accessible</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-[#6b7280]">
                  Maintain high contrast text, use clear iconography, and ensure all interactive elements are easily identifiable.
                </p>
              </CardContent>
            </Card>

            <Card className="border-[#e0e7ff]">
              <CardHeader>
                <CardTitle className="text-[#1f2937]">Consistent & Modular</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-[#6b7280]">
                  Reuse components and maintain consistent spacing, colors, and patterns throughout the application.
                </p>
              </CardContent>
            </Card>
          </div>
        </section>
      </div>
    </div>
  );
}
