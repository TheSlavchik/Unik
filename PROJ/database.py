import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_name='project_finder.db'):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        """Инициализация таблиц базы данных"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Таблица пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    role TEXT DEFAULT 'участник',
                    skills TEXT,
                    interests TEXT,
                    about TEXT,
                    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица проектов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT,
                    required_skills TEXT,
                    creator_id INTEGER,
                    status TEXT DEFAULT 'активен',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (creator_id) REFERENCES users (user_id)
                )
            ''')
            
            # Таблица участников проектов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project_members (
                    project_id INTEGER,
                    user_id INTEGER,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (project_id),
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    PRIMARY KEY (project_id, user_id)
                )
            ''')
            
            # Таблица заявок в проекты
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project_applications (
                    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    user_id INTEGER,
                    message TEXT,
                    status TEXT DEFAULT 'ожидает',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (project_id),
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Таблица навыков
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skills (
                    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT UNIQUE
                )
            ''')
            
            conn.commit()
    
    # Методы для работы с пользователями
    def add_user(self, user_id: int, username: str, first_name: str, last_name: str = None):
        """Добавление или обновление пользователя"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name))
            conn.commit()
    
    def update_user_profile(self, user_id: int, role: str, skills: str, interests: str, about: str):
        """Обновление профиля пользователя"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET role = ?, skills = ?, interests = ?, about = ?
                WHERE user_id = ?
            ''', (role, skills, interests, about, user_id))
            conn.commit()
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Получение информации о пользователе"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if row:
                columns = ['user_id', 'username', 'first_name', 'last_name', 
                          'role', 'skills', 'interests', 'about', 'registered_at']
                return dict(zip(columns, row))
            return None
    
    # Методы для работы с проектами
    def add_project(self, title: str, description: str, category: str, 
                   required_skills: str, creator_id: int) -> int:
        """Создание нового проекта"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO projects (title, description, category, required_skills, creator_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, description, category, required_skills, creator_id))
            conn.commit()
            return cursor.lastrowid
    
    def get_projects(self, category: str = None, skill: str = None) -> List[Dict]:
        """Получение списка проектов с фильтрацией"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = '''
                SELECT p.*, u.username as creator_username, u.first_name as creator_name
                FROM projects p
                JOIN users u ON p.creator_id = u.user_id
                WHERE p.status = 'активен'
            '''
            params = []
            
            if category:
                query += ' AND p.category = ?'
                params.append(category)
            
            if skill:
                query += ' AND p.required_skills LIKE ?'
                params.append(f'%{skill}%')
            
            query += ' ORDER BY p.created_at DESC'
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            projects = []
            for row in rows:
                columns = ['project_id', 'title', 'description', 'category', 
                          'required_skills', 'creator_id', 'status', 'created_at',
                          'creator_username', 'creator_name']
                projects.append(dict(zip(columns, row)))
            
            return projects
    
    def get_project(self, project_id: int) -> Optional[Dict]:
        """Получение информации о проекте"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.*, u.username as creator_username, u.first_name as creator_name
                FROM projects p
                JOIN users u ON p.creator_id = u.user_id
                WHERE p.project_id = ?
            ''', (project_id,))
            row = cursor.fetchone()
            if row:
                columns = ['project_id', 'title', 'description', 'category', 
                          'required_skills', 'creator_id', 'status', 'created_at',
                          'creator_username', 'creator_name']
                return dict(zip(columns, row))
            return None
    
    def get_user_projects(self, user_id: int) -> List[Dict]:
        """Получение проектов пользователя (созданные и участие)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Проекты, созданные пользователем
            cursor.execute('''
                SELECT p.*, 'создатель' as role
                FROM projects p
                WHERE p.creator_id = ?
                ORDER BY p.created_at DESC
            ''', (user_id,))
            created = cursor.fetchall()
            
            # Проекты, в которых участвует пользователь
            cursor.execute('''
                SELECT p.*, 'участник' as role
                FROM projects p
                JOIN project_members pm ON p.project_id = pm.project_id
                WHERE pm.user_id = ?
                ORDER BY p.created_at DESC
            ''', (user_id,))
            member = cursor.fetchall()
            
            projects = []
            columns = ['project_id', 'title', 'description', 'category', 
                      'required_skills', 'creator_id', 'status', 'created_at', 'role']
            
            for row in created + member:
                projects.append(dict(zip(columns, row)))
            
            return projects
    
    def join_project(self, project_id: int, user_id: int, message: str = None):
        """Подача заявки на участие в проекте"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Проверка, не создатель ли проекта
            cursor.execute('SELECT creator_id FROM projects WHERE project_id = ?', (project_id,))
            creator = cursor.fetchone()
            if creator and creator[0] == user_id:
                return False, "Вы не можете подать заявку в свой собственный проект"
            
            # Проверка, не участник ли уже
            cursor.execute('''
                SELECT 1 FROM project_members 
                WHERE project_id = ? AND user_id = ?
            ''', (project_id, user_id))
            if cursor.fetchone():
                return False, "Вы уже участвуете в этом проекте"
            
            # Проверка, нет ли уже заявки
            cursor.execute('''
                SELECT 1 FROM project_applications 
                WHERE project_id = ? AND user_id = ? AND status = 'ожидает'
            ''', (project_id, user_id))
            if cursor.fetchone():
                return False, "У вас уже есть активная заявка в этот проект"
            
            # Создание заявки
            cursor.execute('''
                INSERT INTO project_applications (project_id, user_id, message)
                VALUES (?, ?, ?)
            ''', (project_id, user_id, message))
            conn.commit()
            return True, "Заявка отправлена"
    
    def get_project_applications(self, project_id: int) -> List[Dict]:
        """Получение заявок в проект"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.*, u.username, u.first_name, u.skills, u.about
                FROM project_applications a
                JOIN users u ON a.user_id = u.user_id
                WHERE a.project_id = ? AND a.status = 'ожидает'
                ORDER BY a.created_at DESC
            ''', (project_id,))
            
            rows = cursor.fetchall()
            applications = []
            for row in rows:
                columns = ['application_id', 'project_id', 'user_id', 'message', 
                          'status', 'created_at', 'username', 'first_name', 'skills', 'about']
                applications.append(dict(zip(columns, row)))
            
            return applications
    
    def process_application(self, application_id: int, decision: str):
        """Обработка заявки (принять/отклонить)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Получаем информацию о заявке
            cursor.execute('''
                SELECT project_id, user_id FROM project_applications 
                WHERE application_id = ?
            ''', (application_id,))
            app = cursor.fetchone()
            
            if not app:
                return False, "Заявка не найдена"
            
            project_id, user_id = app
            
            # Обновляем статус заявки
            cursor.execute('''
                UPDATE project_applications 
                SET status = ? 
                WHERE application_id = ?
            ''', (decision, application_id))
            
            if decision == 'принята':
                # Добавляем пользователя в участники проекта
                cursor.execute('''
                    INSERT OR IGNORE INTO project_members (project_id, user_id)
                    VALUES (?, ?)
                ''', (project_id, user_id))
            
            conn.commit()
            return True, f"Заявка {decision}"
    
    def get_recommendations(self, user_id: int) -> List[Dict]:
        """Получение рекомендаций проектов для пользователя"""
        user = self.get_user(user_id)
        if not user or not user.get('skills'):
            return []
        
        user_skills = set(user['skills'].lower().split(','))
        
        projects = self.get_projects()
        recommendations = []
        
        for project in projects:
            project_skills = set(project['required_skills'].lower().split(','))
            # Считаем совпадение навыков
            matching_skills = user_skills.intersection(project_skills)
            if matching_skills:
                project['match_percent'] = len(matching_skills) / len(project_skills) * 100
                recommendations.append(project)
        
        # Сортируем по проценту совпадения
        recommendations.sort(key=lambda x: x['match_percent'], reverse=True)
        return recommendations[:10]  # Возвращаем топ-10 рекомендаций