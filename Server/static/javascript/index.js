function refreshPage() {
    window.location.reload();
}

function chatbotAnswer(customInput) {
    var userInput = customInput || document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    // 사용자 채팅창 생성
    var chatContainer = document.querySelector(".messages");
    var userMessage = document.createElement("div");
    userMessage.classList.add("message", "user-message");
    userMessage.innerHTML = `${userInput}`;
    chatContainer.appendChild(userMessage);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    // 입력창 비활성화
    document.getElementById("user-input").disabled = true;

    // 챗봇 프로필 이미지 생성
    var botProfile = document.createElement("div");
    botProfile.classList.add("bot_prof");
    botProfile.innerHTML = '<img src="static/images/induk.jpg" height="45" width="45" style="cursor: pointer;" onclick="refreshPage()">';
    chatContainer.appendChild(botProfile); // 챗봇 프로필 이미지를 메시지 컨테이너에 추가

    var botName = document.createElement("div"); // 챗봇 이름 요소 생성
    botName.classList.add("message-author", "bot"); // 챗봇 이름 클래스 추가
    botName.innerText = "기계인덕"; // 챗봇 이름 설정
    chatContainer.appendChild(botName); // 챗봇 이름 요소를 챗봇 메시지 컨테이너에 추가

    // "답변 생성 중" 메시지 추가
    var loadingMessage = document.createElement("div");
    loadingMessage.classList.add("message", "bot-message");
    loadingMessage.innerHTML = `답변 생성 중<span id="loading-dots">.</span>`;
    chatContainer.appendChild(loadingMessage);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    // 점 애니메이션 시작
    var dots = 1;
    var loadingDots = document.getElementById("loading-dots");
    var interval = setInterval(() => {
        dots = (dots % 3) + 1;
        loadingDots.textContent = '.'.repeat(dots);
    }, 500);

    // 질문을 서버로 보냅니다.
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: userInput })
    })
    .then(response => response.json())
    .then(data => {
        text = data.answer;

        // "답변 생성 중" 메시지 제거
        clearInterval(interval);
        chatContainer.removeChild(loadingMessage);
        
        // 챗봇 채팅창 생성
        var botMessage = document.createElement("div");
        botMessage.classList.add("message", "bot-message");
        botMessage.innerHTML = `${text}`;
        chatContainer.appendChild(botMessage);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        // 입력창 활성화
        document.getElementById("user-input").disabled = false;
        // 입력창에 포커스 설정
        document.getElementById("user-input").focus();
    });
        
    document.getElementById("user-input").value = "";
}

// 엔터 키 누를 때 전송되도록 설정
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        chatbotAnswer();
    }
});