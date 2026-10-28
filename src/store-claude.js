// Speicher: geteilte Datenbank des Claude-Artefakts
const STORE = {
  async connect(h){
    let db = null, user = null;
    try { [db, user] = await Promise.all([window.claude?.use ? claude.use("db") : null, window.claude?.use ? claude.use("user") : null]); }
    catch { db = null; }
    if (!db){ h.status("local","Nur auf diesem Gerät"); return null; }
    const cw = user ? await user.can("data.write") : null;
    if (cw === false) h.readOnly();
    h.status("live", cw === false ? "Geteilt · nur lesen" : "Geteilt · live");
    const lost = e => h.status("local", e && e.code === "revoked" ? "Kein Zugriff mehr" : "Verbindung verloren, bitte neu laden");
    const docs = snap => { const m = {}; snap.docs.forEach(d => { if (d.exists) m[d.id] = d.data(); }); return m; };
    db.collection("marks").onSnapshot(s => h.marks(docs(s)), lost);
    db.collection("avail").onSnapshot(s => h.avail(docs(s)), lost);
    db.collection("houses").onSnapshot(s => h.houses(s.docs.filter(d => d.exists).map(d => ({...d.data(), id:d.id}))), lost);
    db.doc("settings/main").onSnapshot(s => h.settings(s.exists ? s.data() : {}), lost);
    this.db = db;
    return db;
  },
  async merge(path, patch){
    const ref = this.db.doc(path);
    try { await ref.update(patch); }
    catch(e){
      if (e && e.code === "invalid_argument"){ const s = await ref.get(); if (!s.exists){ await ref.set(patch); return; } }
      if (e && e.code === "unavailable"){ await new Promise(r => setTimeout(r, 400 + Math.random()*600)); await ref.update(patch); return; }
      throw e;
    }
  },
  async add(col, data){ return (await this.db.collection(col).add(data)).id; },
  del(path){ return this.db.doc(path).delete(); }
};
