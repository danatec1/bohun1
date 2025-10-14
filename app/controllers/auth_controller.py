"""
Auth Controller
인증 관련 요청을 처리하는 컨트롤러
"""

from flask import render_template, request, redirect, url_for, session, flash
from ..repositories.user_repository import UserRepository


class AuthController:
    def __init__(self):
        self.user_repository = UserRepository()

    def show_login_page(self):
        """로그인 페이지 표시"""
        if 'user_id' in session:
            return redirect(url_for('main.index'))
        return render_template('login.html')

    def login(self):
        """로그인 처리"""
        if request.method == 'GET':
            return self.show_login_page()

        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')

        if not username or not password:
            return render_template('login.html',
                                   error='사용자명과 비밀번호를 입력해주세요.')

        user = self.user_repository.find_by_username(username)

        if user and self.user_repository.verify_password(user, password):
            session['user_id'] = user.user_id
            session['username'] = user.username
            session.permanent = bool(remember)
            flash(f'환영합니다, {user.username}님!', 'success')
            return redirect(url_for('main.index'))
        else:
            return render_template('login.html',
                                   error='사용자명 또는 비밀번호가 올바르지 않습니다.')

    def signup(self):
        """회원가입 처리"""
        if request.method == 'GET':
            return redirect(url_for('main.login'))

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # 유효성 검사
        if not all([username, email, password, password2]):
            return render_template('login.html',
                                   error='모든 필드를 입력해주세요.')

        if password != password2:
            return render_template('login.html',
                                   error='비밀번호가 일치하지 않습니다.')

        if len(password) < 6:
            return render_template('login.html',
                                   error='비밀번호는 최소 6자 이상이어야 합니다.')

        # 사용자 생성
        user_id = self.user_repository.create_user(username, email, password)

        if user_id:
            return render_template('login.html',
                                   success='회원가입이 완료되었습니다! 로그인해주세요.')
        else:
            return render_template('login.html',
                                   error='이미 사용 중인 사용자명 또는 이메일입니다.')

    def logout(self):
        """로그아웃 처리"""
        session.clear()
        flash('로그아웃되었습니다.', 'info')
        return redirect(url_for('main.login'))
