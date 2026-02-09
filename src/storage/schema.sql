-- ============================
-- ArcadeBasketPi - Schema SQL
-- ============================

PRAGMA foreign_keys = ON;

-- ----------------------------
-- Table des matchs
-- ----------------------------
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL DEFAULT 0,
    duration_seconds INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------
-- Table des records (optionnel)
-- ----------------------------
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    best_score INTEGER NOT NULL,
    achieved_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
