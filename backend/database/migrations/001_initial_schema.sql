-- Initial database schema for Physical AI & Humanoid Robotics Interactive Textbook

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User Profiles Table
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    background TEXT, -- User's educational/professional background
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_email ON user_profiles(email);

-- Textbook Chapters Table
CREATE TABLE textbook_chapters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    urdu_content TEXT, -- Translated content
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Textbook Sections Table
CREATE TABLE textbook_sections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter_id UUID REFERENCES textbook_chapters(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    urdu_content TEXT,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Chapter Interactions Table
CREATE TABLE chapter_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    chapter_id UUID REFERENCES textbook_chapters(id) ON DELETE CASCADE,
    last_accessed TIMESTAMP DEFAULT NOW(),
    progress_percentage DECIMAL(5,2) DEFAULT 0.00,
    personalized_content TEXT, -- Personalized version based on user background
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_chapter_slug ON textbook_chapters(slug);
CREATE INDEX idx_chapter_order ON textbook_chapters(order_index);
CREATE INDEX idx_section_chapter ON textbook_sections(chapter_id);
CREATE INDEX idx_section_order ON textbook_sections(order_index);
CREATE INDEX idx_interaction_user ON chapter_interactions(user_id);
CREATE INDEX idx_interaction_chapter ON chapter_interactions(chapter_id);

-- Insert initial chapters
INSERT INTO textbook_chapters (title, slug, content, order_index) VALUES
('Introduction to Physical AI & Humanoid Robotics', 'introduction', '# Introduction to Physical AI & Humanoid Robotics\n\nThis chapter provides an overview of Physical AI and Humanoid Robotics...', 1),
('Perception Systems in Robotics', 'perception', '# Perception Systems in Robotics\n\nRobots need to perceive their environment to operate effectively...', 2),
('Control Systems for Humanoid Robots', 'control', '# Control Systems for Humanoid Robots\n\nHumanoid robots require sophisticated control systems to maintain balance and perform tasks...', 3),
('Learning in Physical AI', 'learning', '# Learning in Physical AI\n\nPhysical AI systems must learn from interaction with the real world...', 4),
('Locomotion and Movement', 'locomotion', '# Locomotion and Movement\n\nHumanoid robots face unique challenges in locomotion...', 5),
('Manipulation and Dexterity', 'manipulation', '# Manipulation and Dexterity\n\nRobots must be able to manipulate objects with precision...', 6),
('Ethics and Social Impact', 'ethics', '# Ethics and Social Impact\n\nAs humanoid robots become more prevalent, ethical considerations become paramount...', 7);