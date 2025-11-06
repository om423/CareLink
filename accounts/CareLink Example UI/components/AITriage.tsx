import { useState } from 'react';
import { Send, ArrowLeft, MapPin, AlertTriangle, CheckCircle, Info } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Textarea } from './ui/textarea';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';

interface Message {
  role: 'user' | 'ai';
  content: string;
}

export function AITriage({ onNavigate }: { onNavigate: (page: string) => void }) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'ai',
      content: "Hello! I'm your CareLink AI Health Assistant. I'm here to help assess your symptoms. Please describe what you're experiencing today."
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [severity, setSeverity] = useState<'mild' | 'moderate' | 'severe' | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    const newUserMessage: Message = {
      role: 'user',
      content: inputMessage
    };

    setMessages(prev => [...prev, newUserMessage]);
    setInputMessage('');
    setIsAnalyzing(true);

    // Simulate AI response
    setTimeout(() => {
      let aiResponse = '';
      let detectedSeverity: 'mild' | 'moderate' | 'severe' = 'mild';

      // Simple keyword-based severity detection for demo
      const lowerInput = inputMessage.toLowerCase();
      if (lowerInput.includes('chest pain') || lowerInput.includes('breathing') || lowerInput.includes('severe')) {
        detectedSeverity = 'severe';
        aiResponse = "I understand you're experiencing concerning symptoms. Based on your description, this appears to be a high-priority situation. I recommend seeking immediate medical attention. Would you like me to help you find the nearest emergency facility?";
      } else if (lowerInput.includes('fever') || lowerInput.includes('cough') || lowerInput.includes('moderate')) {
        detectedSeverity = 'moderate';
        aiResponse = "Thank you for sharing that information. Based on your symptoms, I'd recommend scheduling an appointment with a healthcare provider within the next 24-48 hours. Can you tell me more about when these symptoms started?";
      } else {
        detectedSeverity = 'mild';
        aiResponse = "I see. These symptoms seem manageable, but it's good that you're being proactive about your health. For mild symptoms like these, monitoring at home and self-care is often sufficient. However, if symptoms worsen, please seek medical attention. Would you like some self-care recommendations?";
      }

      setSeverity(detectedSeverity);
      setMessages(prev => [...prev, { role: 'ai', content: aiResponse }]);
      setIsAnalyzing(false);
    }, 1500);
  };

  const getSeverityColor = (sev: 'mild' | 'moderate' | 'severe') => {
    switch (sev) {
      case 'mild': return 'bg-[#27ae60]';
      case 'moderate': return 'bg-[#f59e0b]';
      case 'severe': return 'bg-[#ef4444]';
    }
  };

  const getSeverityProgress = (sev: 'mild' | 'moderate' | 'severe') => {
    switch (sev) {
      case 'mild': return 25;
      case 'moderate': return 60;
      case 'severe': return 95;
    }
  };

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
                <h2 className="text-[#1f2937]">AI Health Triage</h2>
                <p className="text-sm text-[#6b7280]">Get instant symptom assessment</p>
              </div>
            </div>
            <Button 
              variant="outline" 
              className="border-[#0d6efd] text-[#0d6efd]"
              onClick={() => onNavigate('patient-dashboard')}
            >
              Save & Exit
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-4 gap-6">
          {/* Chat Interface */}
          <div className="lg:col-span-3">
            <Card className="border-[#e0e7ff] h-[calc(100vh-16rem)]">
              <CardContent className="p-0 h-full flex flex-col">
                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-6 space-y-4">
                  {messages.map((message, index) => (
                    <div
                      key={index}
                      className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                          message.role === 'user'
                            ? 'bg-[#0d6efd] text-white rounded-br-sm'
                            : 'bg-white border border-[#e0e7ff] text-[#1f2937] rounded-bl-sm'
                        }`}
                      >
                        {message.role === 'ai' && (
                          <div className="flex items-center gap-2 mb-2">
                            <div className="w-6 h-6 rounded-full bg-[#0d6efd] flex items-center justify-center">
                              <Info className="w-4 h-4 text-white" />
                            </div>
                            <span className="text-xs text-[#6b7280]">AI Assistant</span>
                          </div>
                        )}
                        <p className="text-sm leading-relaxed">{message.content}</p>
                      </div>
                    </div>
                  ))}
                  {isAnalyzing && (
                    <div className="flex justify-start">
                      <div className="bg-white border border-[#e0e7ff] rounded-2xl rounded-bl-sm px-4 py-3">
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 bg-[#0d6efd] rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-[#0d6efd] rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                          <div className="w-2 h-2 bg-[#0d6efd] rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Input Area */}
                <div className="border-t border-[#e0e7ff] p-4 bg-white">
                  <div className="flex gap-2">
                    <Textarea
                      placeholder="Describe your symptoms..."
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                          e.preventDefault();
                          handleSendMessage();
                        }
                      }}
                      className="min-h-[60px] border-[#e0e7ff] focus-visible:ring-[#0d6efd] resize-none"
                    />
                    <Button
                      onClick={handleSendMessage}
                      className="bg-[#0d6efd] hover:bg-[#0b5ed7] text-white h-[60px] px-6"
                      disabled={!inputMessage.trim() || isAnalyzing}
                    >
                      <Send className="w-5 h-5" />
                    </Button>
                  </div>
                  <p className="text-xs text-[#6b7280] mt-2">
                    Press Enter to send • Shift + Enter for new line
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Severity Panel */}
          <div className="space-y-6">
            {/* Severity Meter */}
            <Card className="border-[#e0e7ff]">
              <CardHeader>
                <CardTitle className="text-[#1f2937] flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-[#f59e0b]" />
                  Severity Assessment
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {severity ? (
                  <>
                    <div className="text-center">
                      <Badge 
                        className={`${getSeverityColor(severity)} text-white text-lg px-4 py-2`}
                      >
                        {severity.charAt(0).toUpperCase() + severity.slice(1)}
                      </Badge>
                    </div>
                    <Progress 
                      value={getSeverityProgress(severity)} 
                      className="h-3"
                    />
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center justify-between">
                        <span className="text-[#6b7280]">Mild</span>
                        <span className="text-[#6b7280]">Moderate</span>
                        <span className="text-[#6b7280]">Severe</span>
                      </div>
                    </div>
                  </>
                ) : (
                  <div className="text-center py-8">
                    <Info className="w-12 h-12 text-[#cbd5e1] mx-auto mb-3" />
                    <p className="text-sm text-[#6b7280]">
                      Severity will be assessed based on your symptoms
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card className="border-[#e0e7ff]">
              <CardHeader>
                <CardTitle className="text-[#1f2937]">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button 
                  className="w-full bg-[#2d9cdb] hover:bg-[#2686b8] text-white justify-start"
                  onClick={() => onNavigate('appointments')}
                >
                  <MapPin className="w-4 h-4 mr-2" />
                  Find Nearby Care
                </Button>
                <Button 
                  variant="outline" 
                  className="w-full border-[#27ae60] text-[#27ae60] justify-start"
                  onClick={() => onNavigate('appointments')}
                >
                  <CheckCircle className="w-4 h-4 mr-2" />
                  Book Appointment
                </Button>
              </CardContent>
            </Card>

            {/* Emergency Notice */}
            <Card className="border-[#ef4444] bg-[#fef2f2]">
              <CardContent className="pt-6">
                <div className="flex gap-3">
                  <AlertTriangle className="w-5 h-5 text-[#ef4444] flex-shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-[#ef4444] mb-2">Emergency?</h4>
                    <p className="text-xs text-[#6b7280] mb-3">
                      If you're experiencing a medical emergency, call 911 immediately.
                    </p>
                    <Button 
                      size="sm" 
                      className="bg-[#ef4444] hover:bg-[#dc2626] text-white w-full"
                    >
                      Call 911
                    </Button>
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
