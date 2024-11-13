// post_write.js


const PAGE = {
    tab:{
        selected:null,
        category:null,
        tag:null,
        post:null,
        changeTab:function(tab){
            if(this.selected){ this.selected.style.display = "none"; }
            this.selected = tab;
            this.selected.style.display = "flex";
        }
    },
    init:function(){
        this.tab.category = document.getElementById("content-category");
        this.tab.tag = document.getElementById("content-tag");
        this.tab.post = document.getElementById("content-post");
        this.tab.changeTab(this.tab.post);

        // 탭 버튼 세팅
        document.getElementById("btn-category").addEventListener("click",()=>PAGE.tab.changeTab(PAGE.tab.category));
        document.getElementById("btn-tag").addEventListener("click",()=>PAGE.tab.changeTab(PAGE.tab.tag));
        document.getElementById("btn-post").addEventListener("click",()=>PAGE.tab.changeTab(PAGE.tab.post));


        // 폼 전송 세팅
        document.getElementById("form-category").addEventListener("submit",formSend);
        document.getElementById("form-tag").addEventListener("submit",formSend);
        document.getElementById("form-post").addEventListener("submit",formSend);

    }
}



document.addEventListener("DOMContentLoaded", init);

async function init() {
    // 페이지 세팅
    PAGE.init();
    
}

async function formSend(evt) {
    evt.preventDefault();
    try{
        const form = evt.target;
        const formData = new FormData(form);
        const resp = await fetch(form.action, {
            method:form.method,
            body:formData
        });
        if(resp.ok){
            alert("등록됨 !");
            form.reset()
        }else{ throw Error("전송 과정중 오류 발셍"); }
    }catch(err){ alert("문제 발생 : ", err.message); }
}


