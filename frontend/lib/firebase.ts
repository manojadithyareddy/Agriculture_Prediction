import { initializeApp, getApps, getApp } from 'firebase/app';
import { getAnalytics, isSupported } from 'firebase/analytics';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

/* ─────────────────────────────────────────────
   Firebase Configuration — AgriFusion AI
   Project: agritech-c8959
   ───────────────────────────────────────────── */

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY || 'AIzaSyDqsSeAI5itvo4CW2AGttbbum5ezOuAFn0',
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN || 'agritech-c8959.firebaseapp.com',
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID || 'agritech-c8959',
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET || 'agritech-c8959.firebasestorage.app',
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || '166983261220',
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID || '1:166983261220:web:08e27a835293e8fa968cb1',
  measurementId: process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID || 'G-2T70MHHMRZ',
};

/* ─── Singleton Initialization ─── */

const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();

/* ─── Service Exports ─── */

const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);

// Analytics — client-side only (SSR guard)
let analytics: ReturnType<typeof getAnalytics> | null = null;
if (typeof window !== 'undefined') {
  isSupported().then((supported) => {
    if (supported) {
      analytics = getAnalytics(app);
    }
  });
}

export { app, auth, db, storage, analytics };
export default app;
