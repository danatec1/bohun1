// 메인 JavaScript 파일

document.addEventListener('DOMContentLoaded', function() {
    console.log('보훈 병원 관리 시스템 로드됨');
    
    // 네비게이션 활성화
    highlightActiveNav();
    
    // 검색 기능 초기화
    initializeSearch();
});

/**
 * 현재 페이지에 해당하는 네비게이션 링크 활성화
 */
function highlightActiveNav() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

/**
 * 검색 기능 초기화
 */
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearch, 300));
    }
}

/**
 * 검색 처리
 */
function handleSearch(event) {
    const query = event.target.value.toLowerCase();
    const hospitalCards = document.querySelectorAll('.hospital-card');
    
    hospitalCards.forEach(card => {
        const hospitalName = card.querySelector('h4').textContent.toLowerCase();
        const hospitalAddress = card.querySelector('.address').textContent.toLowerCase();
        
        if (hospitalName.includes(query) || hospitalAddress.includes(query)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
    
    updateHospitalCount();
}

/**
 * 병원 수 업데이트
 */
function updateHospitalCount() {
    const visibleCards = document.querySelectorAll('.hospital-card[style="display: block"], .hospital-card:not([style])');
    const countElement = document.querySelector('.hospital-count');
    
    if (countElement) {
        countElement.textContent = `총 ${visibleCards.length}개 병원`;
    }
}

/**
 * 디바운스 함수
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * API 호출 헬퍼
 */
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API 호출 오류:', error);
        throw error;
    }
}

/**
 * 토스트 알림 표시
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

/**
 * 로딩 스피너 표시/숨김
 */
function showLoading(show = true) {
    let spinner = document.getElementById('loadingSpinner');
    
    if (show) {
        if (!spinner) {
            spinner = document.createElement('div');
            spinner.id = 'loadingSpinner';
            spinner.className = 'loading-spinner';
            spinner.innerHTML = '<div class="spinner"></div>';
            document.body.appendChild(spinner);
        }
        spinner.style.display = 'flex';
    } else {
        if (spinner) {
            spinner.style.display = 'none';
        }
    }
}