-- Script para configurar banco PostgreSQL
-- Execute como superuser (postgres)

-- Criar banco de dados
CREATE DATABASE twitter_data;

-- Conectar ao banco twitter_data
\c twitter_data;

-- Criar usuário (opcional)
CREATE USER twitter_user WITH PASSWORD 'twitter123';

-- Dar permissões
GRANT ALL PRIVILEGES ON DATABASE twitter_data TO twitter_user;
GRANT ALL ON SCHEMA public TO twitter_user;

-- Criar tabela
CREATE TABLE IF NOT EXISTS twitter_comments (
    id SERIAL PRIMARY KEY,
    post_url TEXT,
    post_content TEXT,
    comment TEXT,
    profile_username VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_profile_username ON twitter_comments(profile_username);
CREATE INDEX IF NOT EXISTS idx_created_at ON twitter_comments(created_at);

-- Mostrar estrutura
\d twitter_comments;