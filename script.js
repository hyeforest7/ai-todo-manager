document.addEventListener('DOMContentLoaded', () => {
    const todoInput = document.getElementById('todoInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loading = document.getElementById('loading');
    const resultArea = document.getElementById('resultArea');
    const analysisResult = document.getElementById('analysisResult');
    const modelName = document.getElementById('modelName');

    // 분석 버튼 클릭 이벤트
    analyzeBtn.addEventListener('click', async () => {
        const task = todoInput.value.trim();
        
        if (!task) {
            alert('할 일을 입력해주세요!');
            return;
        }

        // 1. 화면 초기화 및 로딩 표시
        loading.classList.remove('hidden');
        resultArea.classList.add('hidden');

        try {
            // 2. 백엔드 API 호출 (데이터 흐름: 프런트엔드 -> 백엔드)
            // 주의: 백엔드 서버가 8001번 포트에서 실행 중이어야 합니다!
            const response = await fetch(`http://127.0.0.1:8001/analyze?task=${encodeURIComponent(task)}`);
            const data = await response.json();

            if (data.error) {
                alert('에러 발생: ' + data.error);
            } else {
                // 3. 결과 화면에 표시 (데이터 흐름: 백엔드 -> 프런트엔드)
                analysisResult.innerText = data.ai_analysis;
                modelName.innerText = data.model_used;
                resultArea.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('서버와 연결할 수 없습니다. 백엔드 서버가 8001번에서 실행 중인지 확인하세요.');
        } finally {
            // 4. 로딩 표시 숨기기
            loading.classList.add('hidden');
        }
    });

    // 엔터 키 지원
    todoInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            analyzeBtn.click();
        }
    });
});
