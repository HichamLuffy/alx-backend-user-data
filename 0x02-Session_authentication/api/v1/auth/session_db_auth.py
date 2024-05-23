#!/usr/bin/env python3
"""SessionAuth module"""
from datetime import datetime
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""
    def create_session(self, user_id=None):
        """Creates and stores new instance"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user ID based on a session ID"""
        if session_id is None:
            return None
        try:
            user_session = UserSession.search({'session_id': session_id})
            if not user_session:
                return None
            user_session = user_session[0]
        except Exception:
            return None
        if self.session_duration <= 0:
            return user_session.user_id
        if user_session.created_at is None:
            return None
        if datetime.now() > user_session.created_at + timedelta(seconds=self.session_duration):
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """Deletes the user session / logs out"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        try:
            user_sessions = UserSession.search({'session_id': session_id})
            if not user_sessions:
                return False
            user_session = user_sessions[0]
            user_session.remove()
            return True
        except Exception:
            return False
