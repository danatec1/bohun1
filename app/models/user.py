"""
User Model
사용자 정보를 관리하는 데이터 모델
"""

class User:
    def __init__(self, user_id=None, username=None, email=None, 
                 password_hash=None, created_at=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        
    def to_dict(self):
        """객체를 딕셔너리로 변환"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        }
        
    @classmethod
    def from_dict(cls, data):
        """딕셔너리에서 객체 생성"""
        return cls(
            user_id=data.get('user_id'),
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            created_at=data.get('created_at')
        )
