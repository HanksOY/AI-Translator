import { sql } from "drizzle-orm";
import { pgTable, text, varchar, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;

export const translationRecords = pgTable("translation_records", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  sourceText: text("source_text").notNull(),
  translatedText: text("translated_text").notNull(),
  sourceLanguage: varchar("source_language", { length: 10 }).notNull(),
  targetLanguage: varchar("target_language", { length: 10 }).notNull(),
  timestamp: timestamp("timestamp").notNull().defaultNow(),
});

export const insertTranslationRecordSchema = createInsertSchema(translationRecords).omit({
  id: true,
  timestamp: true,
});

export type InsertTranslationRecord = z.infer<typeof insertTranslationRecordSchema>;
export type TranslationRecord = typeof translationRecords.$inferSelect;
