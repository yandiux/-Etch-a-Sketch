import Database from "better-sqlite3";
import fs from "node:fs";
import path from "node:path";

export class EventStore {
  private db: Database.Database;

  constructor(dbPath: string) {
    fs.mkdirSync(path.dirname(dbPath), { recursive: true });
    this.db = new Database(dbPath);
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS processed_events (
        event_id TEXT PRIMARY KEY,
        event_type TEXT NOT NULL,
        processed_at TEXT NOT NULL
      );
    `);
  }

  hasProcessed(eventId: string): boolean {
    const row = this.db
      .prepare("SELECT 1 FROM processed_events WHERE event_id = ?")
      .get(eventId);
    return Boolean(row);
  }

  markProcessed(eventId: string, eventType: string): void {
    this.db
      .prepare(
        "INSERT INTO processed_events (event_id, event_type, processed_at) VALUES (?, ?, ?)",
      )
      .run(eventId, eventType, new Date().toISOString());
  }
}
