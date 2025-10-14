// 병원 페이지 JavaScript

let hospitalMap;
let markers = [];

document.addEventListener('DOMContentLoaded', function() {
    console.log('병원 페이지 로드됨');
    
    // 지도가 있으면 초기화
    const mapElement = document.getElementById('hospitalMap');
    if (mapElement) {
        initializeMap();
        loadHospitals();
    }
    
    initializeSearch();
});

/**
 * 지도 초기화
 */
function initializeMap() {
    try {
        // 서울 중심으로 지도 초기화
        hospitalMap = L.map('hospitalMap').setView([37.5665, 126.9780], 11);
        
        // 타일 레이어 추가
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(hospitalMap);
        
        console.log('지도 초기화 완료');
    } catch (error) {
        console.error('지도 초기화 실패:', error);
    }
}

/**
 * 병원 데이터 로드
 */
async function loadHospitals() {
    try {
        console.log('병원 데이터 로드 시작');
        const response = await fetch('/api/hospitals');
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const hospitals = await response.json();
        console.log('로드된 병원 수:', hospitals.length);
        
        if (hospitalMap) {
            displayHospitalsOnMap(hospitals);
        }
        updateHospitalList(hospitals);
        
    } catch (error) {
        console.error('병원 데이터 로드 실패:', error);
        
        // 샘플 데이터로 테스트
        const sampleHospitals = [
            {
                hospital_id: 1,
                name: '서울대학교병원',
                address: '서울특별시 종로구 대학로 101',
                latitude: 37.5800,
                longitude: 127.0017,
                medical_departments: ['내과', '외과', '정형외과']
            },
            {
                hospital_id: 2,
                name: '삼성서울병원',
                address: '서울특별시 강남구 일원로 81',
                latitude: 37.4881,
                longitude: 127.0857,
                medical_departments: ['심장내과', '신경외과', '암센터']
            }
        ];
        
        if (hospitalMap) {
            displayHospitalsOnMap(sampleHospitals);
        }
        updateHospitalList(sampleHospitals);
    }
}

/**
 * 지도에 병원 마커 표시
 */
function displayHospitalsOnMap(hospitals) {
    if (!hospitalMap) return;
    
    // 기존 마커 제거
    markers.forEach(marker => hospitalMap.removeLayer(marker));
    markers = [];
    
    hospitals.forEach(hospital => {
        if (hospital.latitude && hospital.longitude) {
            const marker = L.marker([hospital.latitude, hospital.longitude])
                .addTo(hospitalMap)
                .bindPopup(`
                    <div class="hospital-popup">
                        <h4>${hospital.name}</h4>
                        <p><strong>주소:</strong> ${hospital.address || '주소 없음'}</p>
                        <p><strong>진료과목:</strong> ${hospital.medical_departments?.join(', ') || '정보 없음'}</p>
                    </div>
                `);
            
            markers.push(marker);
        }
    });
    
    console.log('지도에 표시된 마커 수:', markers.length);
}

/**
 * 병원 목록 업데이트
 */
function updateHospitalList(hospitals) {
    const listContainer = document.getElementById('hospitalsList');
    if (!listContainer) return;
    
    listContainer.innerHTML = hospitals.map(hospital => `
        <div class="hospital-card" data-hospital-id="${hospital.hospital_id}">
            <div class="hospital-info">
                <h4>${hospital.name}</h4>
                <p class="address">${hospital.address || '주소 정보 없음'}</p>
                <div class="departments">
                    ${hospital.medical_departments?.map(dept => `<span class="dept-tag">${dept}</span>`).join('') || ''}
                </div>
            </div>
            <div class="hospital-actions">
                <button class="btn-small btn-view" onclick="viewHospital(${hospital.hospital_id})">보기</button>
                <button class="btn-small btn-edit" onclick="editHospital(${hospital.hospital_id})">편집</button>
                <button class="btn-small btn-delete" onclick="deleteHospital(${hospital.hospital_id})">삭제</button>
            </div>
        </div>
    `).join('');
    
    // 병원 수 업데이트
    const countElement = document.querySelector('.hospital-count');
    if (countElement) {
        countElement.textContent = `총 ${hospitals.length}개 병원`;
    }
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
async function handleSearch(event) {
    const query = event.target.value;
    
    try {
        const response = await fetch(`/api/hospitals/search?q=${encodeURIComponent(query)}`);
        const hospitals = await response.json();
        
        if (hospitalMap) {
            displayHospitalsOnMap(hospitals);
        }
        updateHospitalList(hospitals);
    } catch (error) {
        console.error('검색 실패:', error);
    }
}

/**
 * 병원 상세보기
 */
function viewHospital(hospitalId) {
    alert(`병원 ID: ${hospitalId}의 상세 정보를 표시합니다.`);
}

/**
 * 병원 편집
 */
function editHospital(hospitalId) {
    alert(`병원 ID: ${hospitalId}를 편집합니다.`);
}

/**
 * 병원 삭제
 */
function deleteHospital(hospitalId) {
    if (confirm('정말로 이 병원을 삭제하시겠습니까?')) {
        alert(`병원 ID: ${hospitalId}를 삭제합니다.`);
    }
}

/**
 * 새 병원 추가 모달 열기
 */
function openAddModal() {
    alert('새 병원 추가 기능을 구현할 예정입니다.');
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
 * Folium 지도 생성
 */
async function generateFoliumMap() {
    const button = event.target;
    const originalText = button.textContent;
    
    try {
        button.textContent = '🔄 지도 생성 중...';
        button.disabled = true;
        
        const response = await fetch('/api/map/folium', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(`✅ ${result.message}\n📁 파일: ${result.filename}`);
            
            // 생성된 파일 다운로드 링크 제공
            if (confirm('생성된 지도 파일을 열어보시겠습니까?')) {
                // 파일 경로를 브라우저에서 열 수 있는 형태로 변환
                const fileUrl = `file:///${result.filepath.replace(/\\/g, '/')}`;
                window.open(fileUrl, '_blank');
            }
        } else {
            alert(`❌ 지도 생성 실패: ${result.error}`);
        }
    } catch (error) {
        console.error('지도 생성 오류:', error);
        alert(`❌ 지도 생성 중 오류가 발생했습니다: ${error.message}`);
    } finally {
        button.textContent = originalText;
        button.disabled = false;
    }
}

/**
 * Excel 파일 내보내기
 */
async function exportToExcel() {
    const button = event.target;
    const originalText = button.textContent;
    
    try {
        button.textContent = '📊 내보내는 중...';
        button.disabled = true;
        
        const response = await fetch('/api/export/excel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(`✅ ${result.message}\n📁 파일: ${result.filename}`);
            console.log('Excel 파일 경로:', result.filepath);
        } else {
            alert(`❌ Excel 내보내기 실패: ${result.error}`);
        }
    } catch (error) {
        console.error('Excel 내보내기 오류:', error);
        alert(`❌ Excel 내보내기 중 오류가 발생했습니다: ${error.message}`);
    } finally {
        button.textContent = originalText;
        button.disabled = false;
    }
}