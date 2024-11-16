document.addEventListener("DOMContentLoaded", () => {



    // 스트롤 세팅 ///////////////////////////////////////////////////////////////
    const projects = document.getElementById("projects");

    let isDragging = false; // 드래그 여부
    let startX;
    let scrollLeft;

    // 마우스 버튼을 눌렀을 때
    projects.addEventListener("mousedown", (e) => {
        e.preventDefault();
        isDragging = false; // 클릭으로 시작
        startX = e.pageX - projects.offsetLeft;
        scrollLeft = projects.scrollLeft;
        projects.classList.add("dragging");
    });

    // 마우스를 움직일 때
    projects.addEventListener("mousemove", (e) => {
        if (!projects.classList.contains("dragging")) return;
        const x = e.pageX - projects.offsetLeft;
        const walk = (x - startX) * 1; // 이동 거리 계산
        projects.scrollLeft = scrollLeft - walk;
        isDragging = true; // 드래그 상태로 전환
    });

    // 마우스 버튼을 떼었을 때
    projects.addEventListener("mouseup", () => {
        projects.classList.remove("dragging");
    });

    // 마우스가 컨테이너를 벗어났을 때
    projects.addEventListener("mouseleave", () => {
        projects.classList.remove("dragging");
    });

    // 링크 클릭 방지
    projects.addEventListener("click", (e) => {
        if (isDragging) {
            e.preventDefault(); // 드래그 중 클릭 방지
        }
    });

    // 드래그 앤 드롭 기본 동작 방지
    projects.addEventListener("dragstart", (e) => {
        e.preventDefault();
    });
    ///////////////////////////////////////////////////////////////////////////////
});
