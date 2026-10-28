// Speicher: Firebase Realtime Database (eigenes Projekt mosel-planer, Daten unter mosel/)
const FIREBASE_CONFIG = {
  apiKey: "AIzaSyDcR3q9jYCMVFsJPcvbos7fSClzNOxYQqM",
  authDomain: "mosel-planer.firebaseapp.com",
  databaseURL: "https://mosel-planer-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "mosel-planer",
  storageBucket: "mosel-planer.firebasestorage.app",
  messagingSenderId: "748659087509",
  appId: "1:748659087509:web:a24d3ce360941355d0239c"
};
const ROOT = "mosel";
const fbPath = p => ROOT + "/" + (p === "settings/main" ? "settings" : p);
const fbErr = e => ({code: /permission/i.test(String(e && (e.code || e.message) || "")) ? "denied" : "unavailable"});
const STORE = {
  async connect(h){
    if (!window.firebase){ h.status("local","Nur auf diesem Gerät (Datenbank nicht erreichbar)"); return null; }
    let fdb;
    try { firebase.initializeApp(FIREBASE_CONFIG); fdb = firebase.database(); }
    catch(e){ h.status("local","Datenbank-Fehler, nur auf diesem Gerät"); return null; }
    let denied = false;
    fdb.ref(".info/connected").on("value", s => { if (!denied) h.status(s.val() ? "live" : "local", s.val() ? "Geteilt · live" : "Offline · wird nachgeholt"); });
    const lost = e => { denied = fbErr(e).code === "denied"; h.status("local", denied ? "Datenbank-Regeln fehlen noch" : "Keine Verbindung zur Datenbank"); };
    fdb.ref(ROOT + "/marks").on("value", s => h.marks(s.val() || {}), lost);
    fdb.ref(ROOT + "/avail").on("value", s => h.avail(s.val() || {}), lost);
    fdb.ref(ROOT + "/houses").on("value", s => h.houses(Object.entries(s.val() || {}).map(([id, d]) => ({...d, id}))), lost);
    fdb.ref(ROOT + "/settings").on("value", s => h.settings(s.val() || {}), lost);
    this.fdb = fdb;
    return fdb;
  },
  async merge(path, patch){
    // Verschachtelte Felder als Pfade schreiben, damit nur geänderte Werte überschrieben werden
    const flat = {};
    const walk = (o, pre) => { for (const [k, v] of Object.entries(o)){ if (v && typeof v === "object" && !Array.isArray(v)) walk(v, pre + k + "/"); else flat[pre + k] = v === undefined ? null : v; } };
    walk(patch, "");
    try { await this.fdb.ref(fbPath(path)).update(flat); } catch(e){ throw fbErr(e); }
  },
  async add(col, data){
    const ref = this.fdb.ref(ROOT + "/" + col).push();
    try { await ref.set(data); } catch(e){ throw fbErr(e); }
    return ref.key;
  },
  async del(path){ try { await this.fdb.ref(fbPath(path)).remove(); } catch(e){ throw fbErr(e); } }
};
