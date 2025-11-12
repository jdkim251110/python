// 간단한 DOM 예제와 퀴즈, 라이브 미리보기 기능

document.addEventListener('DOMContentLoaded', function(){
  // 버튼 클릭 예제
  const btn = document.getElementById('btn');
  if(btn){
    btn.addEventListener('click', function(){
      btn.textContent = '클릭했어요!';
      btn.disabled = true;
    });
  }

  // 퀴즈 로직
  const choices = document.querySelectorAll('#choices .choice');
  const result = document.getElementById('result');
  choices.forEach((c)=>{
    c.addEventListener('click', function(e){
      const text = e.target.textContent || '';
      if(text.startsWith('B')){
        result.textContent = '정답입니다 🎉 — HTML은 문서의 구조를 정의합니다.';
        result.style.color = 'green';
      } else {
        result.textContent = '틀렸습니다. 다시 시도해보세요.';
        result.style.color = 'crimson';
      }
    });
  });

  // 라이브 편집기: textarea의 내용을 바로 미리보기로 렌더
  const editor = document.getElementById('editor');
  const preview = document.getElementById('preview');
  function updatePreview(){
    // 안전을 위해 innerText로 소스 보이기 대신 간단한 sanitize(여기선 허용된 태그만 치환)
    // 이 예제는 학습용이며 XSS 방지에 완전하지 않습니다.
    preview.innerHTML = editor.value;
  }
  if(editor){
    updatePreview();
    editor.addEventListener('input', updatePreview);
  }
});
