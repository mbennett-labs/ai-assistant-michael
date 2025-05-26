# Michael's AI Assistant | Quantum Shield Labs

> **A full-stack AI assistant that integrates with Google Calendar to create real appointments through natural language conversation.**

![AI Assistant Banner](https://img.shields.io/badge/Status-Live%20%26%20Working-brightgreen) ![Google Calendar](https://img.shields.io/badge/Google%20Calendar-Integrated-blue) ![Claude AI](https://img.shields.io/badge/Claude%20AI-Powered-purple) ![Flask](https://img.shields.io/badge/Flask-Web%20Interface-red) ![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)

## 🚀 **Live Demo Screenshots**

### 💬 AI Chat Interface - Natural Language Appointment Creation
![AI Chat Interface](screenshots/ai-chat-interface.png)
*Professional interface where users can request appointments in plain English. The AI understands context and creates real Google Calendar events.*

### 📋 Calendar List View - All Events with AI-Created Appointments  
![Calendar List View](screenshots/calendar-list-view.png)
*Shows all upcoming events including AI-created appointments like "Dentist Appointment" with precise timestamps.*

### 📅 Monthly Calendar Grid - Visual Planning with Event Preview
![Monthly Calendar](screenshots/monthly-calendar-view.png)
*Interactive monthly view with appointments displayed in calendar grid. Shows "Dentist Ap..." created by AI on May 27th.*

## ✨ **Key Features**

### 🤖 **Intelligent Appointment Creation**
- **Natural Language Processing**: "Schedule a dentist appointment tomorrow at 2 PM"
- **Real Google Calendar Integration**: Actually creates events in your Google Calendar (not just mock data)
- **Smart Time Parsing**: Understands relative dates (tomorrow, next week, etc.)
- **Appointment Confirmation**: Provides immediate feedback when appointments are successfully created
- **Context Awareness**: Remembers conversation history and calendar context

### 📅 **Advanced Calendar Management**
- **Dual View System**: Toggle between detailed list view and interactive monthly grid
- **Real-time Sync**: Displays actual Google Calendar events with live updates
- **Interactive Navigation**: Month-by-month browsing with Today button and smooth transitions
- **Event Details Modal**: Click any day to see comprehensive event information
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

### 💬 **Conversational AI Interface**
- **Memory Retention**: Maintains conversation context within sessions
- **Professional Design**: Clean, modern interface suitable for business environments
- **Real-time Responses**: Instant AI feedback and calendar updates
- **Error Handling**: Graceful handling of calendar permissions and connection issues
- **Multi-turn Conversations**: Handles complex appointment scheduling workflows

## 🛠️ **Technical Architecture**

### **Backend Stack**
- **AI Engine**: Anthropic Claude API for advanced natural language processing
- **Calendar API**: Google Calendar API with OAuth2 authentication and write permissions
- **Web Frameworks**: 
  - Flask for AI assistant web interface
  - FastAPI for additional API endpoints (demonstrating framework versatility)
- **Authentication**: Secure Google OAuth flow with automatic token refresh
- **Environment Management**: Secure credential handling with dotenv

### **Frontend Stack**
- **UI Framework**: Modern HTML5 with Tailwind CSS for responsive design
- **JavaScript**: Vanilla JS with async/await for seamless API communication
- **Interactive Components**: Custom calendar widget with dual view modes
- **Icons & Styling**: Font Awesome with custom CSS for professional appearance
- **Real-time Updates**: Dynamic DOM manipulation for instant user feedback

### **Integration Layer**
- **Calendar Service**: Handles Google Calendar CRUD operations with error handling
- **AI Service**: Manages Claude API conversations with context retention
- **Appointment Parser**: Extracts date, time, and appointment details from natural language
- **Business Logic**: Smart appointment type detection and scheduling workflows

## 🏆 **Project Highlights**

This AI assistant represents a complete, production-ready application that demonstrates:

✅ **Real AI Integration** - Not just a chatbot, but functional AI that performs real-world actions  
✅ **Production-Ready Architecture** - Professional code structure with proper error handling  
✅ **Business Value** - Solves actual problems with appointment scheduling automation  
✅ **Technical Excellence** - Clean code, modern frameworks, secure authentication  
✅ **User Experience** - Intuitive interface that works immediately without training  
✅ **Scalability** - Architecture designed for multi-user and enterprise deployment  

**This project showcases the intersection of AI, practical business applications, and professional software development.**

---

*Built with passion and precision by Michael Bennett | Quantum Shield Labs* 🚀

**Ready for enterprise deployment and client customization**
