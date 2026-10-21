'use client';

import React, { useState, useEffect, useRef } from 'react';
import {
  MessageSquare,
  Send,
  Sparkles,
  Bot,
  User,
  ShieldCheck,
  Languages,
  RotateCcw,
  BookOpen,
  Info,
  AlertCircle,
  HelpCircle,
  CheckCircle2,
  Copy,
  ThumbsUp,
  ThumbsDown,
  ChevronRight,
  Sprout,
  Droplet,
  CloudSun,
  TrendingUp,
  Bug,
  MapPin,
  Clock,
  RefreshCw
} from 'lucide-react';
import { sendChatMessage, ChatMessageResponse } from '@/lib/api';
import { useGlobalContext } from '@/components/GlobalContext';

interface MessageItem {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  sources?: string[];
  suggestedFollowups?: string[];
  isError?: boolean;
}

const TELUGU_QUICK_TOPICS = [
  { label: 'వరిలో అగ్గితెగులు నివారణ', query: 'వరిలో అగ్గితెగులు (Blast) లక్షణాలు మరియు సమగ్ర నివారణ పద్ధతులు ఏమిటి?' },
  { label: 'ప్రత్తిలో గులాబీ రంగు పురుగు', query: 'ప్రత్తి పంటలో గులాబీ రంగు కాయతొలుచు పురుగు (Pink Bollworm) నివారణ ఎలా?' },
  { label: 'మొక్కజొన్నలో కత్తెర పురుగు', query: 'మొక్కజొన్న పంటలో కత్తెర పురుగు (Fall Armyworm) నివారణకు ఎలాంటి చర్యలు తీసుకోవాలి?' },
  { label: 'ఎరువుల యాజమాన్యం', query: 'భూసార పరీక్ష ఆధారంగా ఎరువుల వాడకం ఎలా చేయాలి?' },
];

const ENGLISH_QUICK_TOPICS = [
  { label: 'Rice Blast Management', query: 'What are the symptoms and integrated management practices for Rice Blast?' },
  { label: 'Cotton Pink Bollworm', query: 'How to monitor and control Pink Bollworm in Cotton using pheromone traps?' },
  { label: 'Maize Fall Armyworm', query: 'What is the IPM protocol for Fall Armyworm in Maize at the vegetative stage?' },
  { label: 'Banana Sigatoka Protocol', query: 'How to manage Black Sigatoka leaf spot disease in Banana?' },
  { label: 'Irrigation & Water Schedule', query: 'What is the FAO-56 irrigation requirement for crops during dry spells?' },
  { label: 'Market Timing & MSP', query: 'When is the optimal time to sell Kharif paddy with respect to MSP and mandi arrivals?' },
];

export default function AiAssistantPage() {
  const { crop: globalCrop, district: globalDistrict, season } = useGlobalContext();

  const [language, setLanguage] = useState<'en' | 'te'>('en');
  const [messages, setMessages] = useState<MessageItem[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');

  // Contextual inputs
  const [contextCrop, setContextCrop] = useState(globalCrop || 'Rice');
  const [contextLocation, setContextLocation] = useState(globalDistrict || 'Warangal');
  const [contextGrowthStage, setContextGrowthStage] = useState('Vegetative / Development');
  const [showContextDrawer, setShowContextDrawer] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize session and greeting
  useEffect(() => {
    const newSession = 'session_' + Math.random().toString(36).substring(2, 10);
    setSessionId(newSession);

    const greetingEn: MessageItem = {
      id: 'greeting_en',
      role: 'assistant',
      content: `Hello! I am your **AgriFusion AI Agronomist**, specializing in Telangana and Andhra Pradesh agriculture.

I can assist you with:
- **Disease & Pest Diagnosis**: Verified ICAR & State Agriculture University control protocols.
- **Soil & Nutrient Management**: Balanced N-P-K and micronutrient advisories.
- **Irrigation Scheduling**: Evapotranspiration and water stress calculations.
- **Market & Harvest Guidance**: Mandi price benchmarks and official MSP comparisons.

💡 *To provide accurate, responsible recommendations, please specify your crop, growth stage, and district.*`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      sources: ['ICAR / PJTSAU / ANGRAU Agronomy Reference Guidelines'],
      suggestedFollowups: [
        'How to manage Rice Blast disease?',
        'What is the recommended fertilizer schedule for Cotton?',
        'What are the symptoms of Fall Armyworm in Maize?'
      ]
    };

    const greetingTe: MessageItem = {
      id: 'greeting_te',
      role: 'assistant',
      content: `నమస్కారం! నేను మీ **అగ్రిఫ్యూజన్ AI వ్యవసాయ సలహాదారుని**. 

తెలంగాణ మరియు ఆంధ్రప్రదేశ్ ప్రాంత పంటల సమగ్ర యాజమాన్యంపై సహాయం చేయగలను:
- **తెగుళ్లు మరియు పురుగుల నివారణ**: ఆచార్య ఎన్.జి. రంగా మరియు ప్రొఫెసర్ జయశంకర్ వ్యవసాయ విశ్వవిద్యాలయాల ప్రామాణిక సిఫార్సులు.
- **ఎరువులు మరియు పోషక యాజమాన్యం**: సమతుల్య N-P-K మరియు జింక్, బోరాన్ సూచనలు.
- **నీటి యాజమాన్యం**: పంట దశల వారీగా నీటి తడుల షెడ్యూల్.
- **మార్కెట్ ధరలు & మద్దతు ధర (MSP)**: వ్యవసాయ మార్కెట్ యార్డుల తాజా ధరల సమాచారం.

💡 *ఖచ్చితమైన రసాయన లేదా ఎరువుల మోతాదు కొరకు దయచేసి మీ పంట పేరు, ప్రస్తుత దశ మరియు జిల్లా వివరాలు తెలపండి.*`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      sources: ['PJTSAU / ANGRAU శాస్త్రీయ వ్యవసాయ మార్గదర్శకాలు'],
      suggestedFollowups: [
        'వరిలో అగ్గితెగులు నివారణ చర్యలు ఏమిటి?',
        'ప్రత్తిలో గులాబీ రంగు పురుగు నివారణ ఎలా?',
        'మొక్కజొన్నలో కత్తెర పురుగు నివారణ పద్ధతులు ఏమిటి?'
      ]
    };

    setMessages([language === 'te' ? greetingTe : greetingEn]);
  }, [language]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSendMessage = async (queryText?: string) => {
    const textToSend = queryText || inputText;
    if (!textToSend.trim() || loading) return;

    const userMsg: MessageItem = {
      id: 'user_' + Date.now(),
      role: 'user',
      content: textToSend.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setLoading(true);

    try {
      const res: ChatMessageResponse = await sendChatMessage(
        textToSend.trim(),
        sessionId,
        contextCrop,
        undefined,
        language,
        contextLocation,
        contextGrowthStage
      );

      const assistantMsg: MessageItem = {
        id: 'assistant_' + Date.now(),
        role: 'assistant',
        content: res.response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        sources: res.sources,
        suggestedFollowups: res.suggested_followups,
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: unknown) {
      const errorMsg: MessageItem = {
        id: 'err_' + Date.now(),
        role: 'assistant',
        content: language === 'te'
          ? 'క్షమించండి, సర్వర్‌ను సంప్రదించడంలో లోపం ఏర్పడింది. దయచేసి మీ ఇంటర్నెట్ కనెక్షన్‌ను సరిచూసుకొని మళ్లీ ప్రయత్నించండి.'
          : 'Unable to reach the agronomic reasoning engine. Please ensure your backend service is running and retry.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        isError: true,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleResetChat = () => {
    setMessages([]);
    const newSession = 'session_' + Math.random().toString(36).substring(2, 10);
    setSessionId(newSession);
  };

  const quickTopics = language === 'te' ? TELUGU_QUICK_TOPICS : ENGLISH_QUICK_TOPICS;

  return (
    <div className="space-y-4 font-sans max-w-[1300px] mx-auto pb-10">
      {/* 1. TOP CONTROL BAR */}
      <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/80 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-600 to-teal-700 flex items-center justify-center text-white shadow-md shadow-emerald-700/20">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-black text-slate-900 tracking-tight">
                AI Agronomist Assistant
              </h1>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                Grounded RAG
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Multimodal crop intelligence calibrated for Andhra Pradesh & Telangana
            </p>
          </div>
        </div>

        {/* Controls: Language Toggle & Context Controls */}
        <div className="flex items-center gap-2.5">
          {/* Language Toggle */}
          <div className="flex items-center bg-slate-100 p-1 rounded-xl text-xs font-bold border border-slate-200/80">
            <button
              onClick={() => setLanguage('en')}
              className={`px-3 py-1.5 rounded-lg transition flex items-center gap-1.5 ${
                language === 'en'
                  ? 'bg-white text-emerald-800 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <span>🇬🇧 English</span>
            </button>
            <button
              onClick={() => setLanguage('te')}
              className={`px-3 py-1.5 rounded-lg transition flex items-center gap-1.5 ${
                language === 'te'
                  ? 'bg-white text-emerald-800 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <span>🇮🇳 తెలుగు</span>
            </button>
          </div>

          {/* Context Drawer Button */}
          <button
            onClick={() => setShowContextDrawer(!showContextDrawer)}
            className={`px-3 py-2 rounded-xl text-xs font-semibold border transition flex items-center gap-1.5 ${
              showContextDrawer
                ? 'bg-emerald-50 text-emerald-800 border-emerald-300'
                : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
            }`}
          >
            <MapPin className="w-3.5 h-3.5 text-emerald-600" />
            <span className="hidden sm:inline">Field Context:</span>
            <span className="font-bold text-slate-900">{contextCrop} ({contextLocation})</span>
          </button>

          {/* Reset Session */}
          <button
            onClick={handleResetChat}
            title="Reset conversation session"
            className="p-2 rounded-xl border border-slate-200 text-slate-500 hover:text-slate-800 hover:bg-slate-50 transition"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* FIELD CONTEXT DRAWER */}
      {showContextDrawer && (
        <div className="bg-emerald-50/60 rounded-2xl p-4 border border-emerald-200/80 shadow-xs grid grid-cols-1 sm:grid-cols-3 gap-3 animate-in fade-in duration-200">
          <div>
            <label className="text-xs font-bold text-slate-700 block mb-1">Target Crop</label>
            <input
              type="text"
              value={contextCrop}
              onChange={(e) => setContextCrop(e.target.value)}
              placeholder="e.g. Rice, Cotton, Maize, Banana"
              className="w-full px-3 py-2 rounded-xl bg-white border border-emerald-200 text-sm font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
          <div>
            <label className="text-xs font-bold text-slate-700 block mb-1">Growth Stage</label>
            <select
              value={contextGrowthStage}
              onChange={(e) => setContextGrowthStage(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-white border border-emerald-200 text-sm font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="Initial / Seedling">Initial / Seedling</option>
              <option value="Vegetative / Development">Vegetative / Development</option>
              <option value="Flowering / Mid-season">Flowering / Mid-season</option>
              <option value="Maturity / Late-season">Maturity / Late-season</option>
            </select>
          </div>
          <div>
            <label className="text-xs font-bold text-slate-700 block mb-1">District / Mandi Location</label>
            <input
              type="text"
              value={contextLocation}
              onChange={(e) => setContextLocation(e.target.value)}
              placeholder="e.g. Warangal, Guntur, Nizamabad"
              className="w-full px-3 py-2 rounded-xl bg-white border border-emerald-200 text-sm font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
        </div>
      )}

      {/* 2. CHAT THREAD DISPLAY */}
      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-xs flex flex-col h-[650px] overflow-hidden">
        {/* Messages List */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-5 scrollbar-thin">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-3 max-w-3xl ${
                msg.role === 'user' ? 'ml-auto flex-row-reverse' : ''
              }`}
            >
              {/* Avatar */}
              <div
                className={`w-8 h-8 rounded-xl shrink-0 flex items-center justify-center text-xs font-bold ${
                  msg.role === 'user'
                    ? 'bg-slate-900 text-white'
                    : msg.isError
                    ? 'bg-rose-100 text-rose-700'
                    : 'bg-emerald-600 text-white shadow-xs'
                }`}
              >
                {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              {/* Bubble Content */}
              <div className="space-y-2 max-w-[85%]">
                <div
                  className={`p-4 rounded-2xl text-sm leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-emerald-700 text-white font-medium rounded-tr-xs'
                      : msg.isError
                      ? 'bg-rose-50 border border-rose-200 text-rose-900 rounded-tl-xs'
                      : 'bg-slate-50 border border-slate-200/80 text-slate-800 rounded-tl-xs space-y-3'
                  }`}
                >
                  <div className="whitespace-pre-wrap">{msg.content}</div>

                  {/* Sources Accordion */}
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="pt-2 border-t border-slate-200/60 text-xs text-slate-500 space-y-1">
                      <div className="flex items-center gap-1.5 font-bold text-slate-700">
                        <BookOpen className="w-3.5 h-3.5 text-emerald-600" />
                        <span>Verified Citations:</span>
                      </div>
                      <ul className="list-disc list-inside space-y-0.5 text-[11px] text-slate-600 pl-1">
                        {msg.sources.map((src, i) => (
                          <li key={i}>{src}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* Footer metadata & actions */}
                <div className="flex items-center gap-3 text-[11px] text-slate-400 px-1">
                  <span>{msg.timestamp}</span>
                  {msg.role === 'assistant' && !msg.isError && (
                    <>
                      <button
                        onClick={() => handleCopy(msg.id, msg.content)}
                        className="hover:text-slate-700 transition flex items-center gap-1"
                      >
                        {copiedId === msg.id ? (
                          <span className="text-emerald-600 font-bold">Copied!</span>
                        ) : (
                          <>
                            <Copy className="w-3 h-3" />
                            <span>Copy</span>
                          </>
                        )}
                      </button>
                    </>
                  )}
                </div>

                {/* Suggested Follow-up Questions */}
                {msg.suggestedFollowups && msg.suggestedFollowups.length > 0 && (
                  <div className="pt-1 flex flex-wrap gap-1.5">
                    {msg.suggestedFollowups.map((fq, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleSendMessage(fq)}
                        className="text-xs px-2.5 py-1 rounded-full bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border border-emerald-200 transition text-left"
                      >
                        {fq}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Loading indicator */}
          {loading && (
            <div className="flex gap-3 max-w-xl">
              <div className="w-8 h-8 rounded-xl bg-emerald-600 text-white flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 animate-pulse" />
              </div>
              <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 rounded-tl-xs flex items-center gap-2 text-xs text-slate-600">
                <RefreshCw className="w-4 h-4 animate-spin text-emerald-600" />
                <span>
                  {language === 'te'
                    ? 'వ్యవసాయ పరిశోధనా పత్రాల నుండి సమాచారం సేకరిస్తున్నాము...'
                    : 'Searching verified ICAR/SAU agronomic knowledge base...'}
                </span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* 3. QUICK SUGGESTIONS STRIP */}
        <div className="p-3 bg-slate-50 border-t border-slate-100 flex items-center gap-2 overflow-x-auto scrollbar-none text-xs">
          <span className="font-bold text-slate-500 whitespace-nowrap px-1">
            {language === 'te' ? 'ముఖ్యమైన అంశాలు:' : 'Quick Questions:'}
          </span>
          {quickTopics.map((item, idx) => (
            <button
              key={idx}
              onClick={() => handleSendMessage(item.query)}
              disabled={loading}
              className="px-3 py-1 rounded-full bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 whitespace-nowrap transition disabled:opacity-50"
            >
              {item.label}
            </button>
          ))}
        </div>

        {/* 4. INPUT COMPOSER */}
        <div className="p-4 border-t border-slate-200 bg-white">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              disabled={loading}
              placeholder={
                language === 'te'
                  ? 'మీ పంట లేదా తెగులు సమస్యను ఇక్కడ టైప్ చేయండి... (ఉదా: వరిలో అగ్గితెగులు)'
                  : 'Ask a question about crop protection, fertilizers, irrigation, or market prices...'
              }
              className="flex-1 px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white transition"
            />
            <button
              type="submit"
              disabled={loading || !inputText.trim()}
              className="px-5 py-3 rounded-xl bg-emerald-700 hover:bg-emerald-600 text-white font-semibold text-sm transition disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-2 shrink-0 shadow-sm shadow-emerald-700/20"
            >
              <Send className="w-4 h-4" />
              <span className="hidden sm:inline">{language === 'te' ? 'పంపండి' : 'Send'}</span>
            </button>
          </form>
          <div className="flex items-center justify-between text-[11px] text-slate-400 mt-2 px-1">
            <span>
              {language === 'te'
                ? 'ఏఐ సలహాలు సాధారణ మార్గదర్శకాలకు మాత్రమే. రసాయన మోతాదులను లేబుల్ ప్రకారం లేదా ఏఈఓ సూచన మేరకు వాడండి.'
                : 'AI advisory reflects standard agricultural research. Always verify chemical rates with certified extension officers.'}
            </span>
            <span className="font-mono text-slate-500">Session: {sessionId}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
