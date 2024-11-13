// post_read.js





const PAGE = {
    comments:null,
    commentForm:null,
    showCommentForm:function(parent_id){
        
        if(this.commentForm){
            this.commentForm.remove();
            this.commentForm = null;
        }
        this.commentForm = document.createElement("form");
        this.commentForm.action = "/post/write/comment"
        this.commentForm.method = "post"
        this.commentForm.className = "commentForm";
        this.commentForm.innerHTML = `
            <div id="comment-write-top">
                작성자 : ${document.getElementById("meta").dataset.name}
            </div>
            <div id="comment-write-bot">
                <input type="hidden" name="post_id" value="${document.getElementById("meta").dataset.post_id}">
                <input type="hidden" name="parent_id" value="${parent_id}">
                <textarea name="content" required></textarea>
                <input type="submit">
            </div>
        `;
        this.commentForm.addEventListener("submit", async(evt)=>{
            evt.preventDefault();
            try{
                const form = evt.target;
                const formData = new FormData(form);
                const resp = await fetch(form.action, {
                    method:form.method,
                    body:formData
                });
                if(resp.ok){
                    alert("대댓글 등록됨 !");
                    form.reset()
                    this.commentForm.remove();
                    this.commentForm = null;
                    await get_comments();

                }else{ throw Error("전송 과정중 오류 발셍"); }
            }catch(err){ console.log("ERROR from comment form : ", err); }
        });
        document.getElementById(parent_id).insertBefore(this.commentForm, document.getElementById(parent_id).children[2]);
    },
    init:function(){
        // 동적 추가되는 코맨트들에 이벤트 달기
        this.comments = document.getElementById("comments");
        this.comments.addEventListener("click", (evt)=>{
            // 클릭한 요소가 입력창이나 버튼인지 확인하여 상위 이벤트 중지
            if (evt.target.matches("textarea, input, button")) {
                evt.stopPropagation();
                return;
            }
            const comment = evt.target.closest(".comment");
            if(comment){
                console.log(comment.id);
                PAGE.showCommentForm( comment.id );
            }
        });


        // 태그에 이벤트 달기
        document.getElementById("comment-form").addEventListener("submit", async(evt)=>{
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
                    form.reset();
                    await get_comments();
                }else if(resp.status==401){
                    alert("댓글을 작성하려면 로그인 해야 합니다.");
                }else{ throw Error("전송 과정중 오류 발셍"); }
            }catch(err){ console.log("ERROR from comment form : ", err); }
        });

        // 코맨트 보기 버튼
        document.getElementById("btn-view-comment").addEventListener("click", async(evt)=>{
            console.log("댓글보기 눌림")
            evt.target.style.display = "none";
            document.getElementById("container-comment").style.display = "inline";
            await get_comments();
        });
    }
}






document.addEventListener("DOMContentLoaded", init)

async function init() {
    // PAGE
    PAGE.init();
}


async function get_comments() {
    try{
        PAGE.comments.innerHTML="";
        const post_id = document.getElementById("meta").dataset.post_id;
        const resp = await fetch(`/post/read/comment/${post_id}`, {method:"GET"});
        if(!resp.ok){ throw Error("서버 응답 오류") }
        const respData = await resp.json();
        // console.log(respData)

        for(const c of respData.comments){
            // console.log(c);
            const d = document.createElement("div");
            d.className = "comment";
            d.id = c.id;
            d.innerHTML = `
                <input type="hidden" value="0">
                <div class="comment-top">
                    <div class="comment-header">
                        ${c.account_name}
                    </div>

                    <div class="comment-body">
                        <p>${c.content}</p>
                    </div>

                    <div class="comment-footer">
                        <p>${c.created_at}</p>
                        <button class="btn-comment-delete" onclick="deleteComment(${c.id})">X</button>
                    </div>
                </div>
            `;

            if(!c.parent_id){ PAGE.comments.appendChild(d); }
            else{ document.getElementById(c.parent_id).appendChild(d) }
        }

    }catch(err){
        console.log("ERROR from btn-view-comment :", err);
    }
}


async function deleteComment(comment_id) {
    try{
        const resp = await fetch(`/post/delete/comment/${comment_id}`);
        if(resp.ok){
            await get_comments()
        }else if(resp.status==401){
            alert("당신이 쓴 댓글만 지울 수 있습니다.")
        }else{
            throw Error("서버 전송 오류");
        }
    }catch(err){
        console.log("ERROR from deleteComment : ", err);
    }
    
}