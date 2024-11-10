// post_root.js


const PAGE = {
    post_ul:null,
    pagination:null,
    n_m:null,
    btnPre:null,
    btnNext:null,
    init:function(){
        // 태그 연결
        this.post_ul = document.getElementById("post-ul");
        this.pagination = document.getElementById("pagination");
        this.n_m = document.getElementById("n_m");
        this.btnPre = document.getElementById("btn-pre");
        this.btnNext = document.getElementById("btn-next")

        // a태그 가로채기
        document.querySelectorAll(".search-by").forEach(element => {
            element.addEventListener("click", async(evt)=>{
                evt.preventDefault();

                const target = evt.target.getAttribute("data-target");
                const id = evt.target.getAttribute("data-id");

                await search(target, id);
            })
        });

        // 버튼설정
        this.btnPre.addEventListener("click",async(evt)=>{
            console.log("<<<");
            const target = this.pagination.dataset.target
            const id = this.pagination.dataset.id
            await search(target, id, evt.target.dataset.page)
        });
        this.btnNext.addEventListener("click",async(evt)=>{
            console.log(">>>");
            const target = this.pagination.dataset.target
            const id = this.pagination.dataset.id
            await search(target, id, evt.target.dataset.page)
        });
    }
}


document.addEventListener("DOMContentLoaded", init);

async function init() {
    // 페이지 세팅
    PAGE.init();

    // 일단 포스트들 불러오기
    
}



async function search(target=null, id=null, page=0) {
    try{
        const url = `/post/search?target=${target}&id=${id}&page=${page}`
        const resp = await fetch(url, {method:"GET"});
        if(!resp.ok){ throw Error("서버의 응답 오류"); }
        respData = await resp.json();
        console.log("응답 받음 : ", respData)

        PAGE.post_ul.innerHTML = ""
        respData.post_list.forEach(p=>{
            const li = document.createElement("li")
            li.innerHTML = `
                <article>
                    <div class="col-left">
                        <img src="/${p.thumbnail}">
                    </div>

                    <div class="col-mid">
                        <div class="row-top">
                            <h3>${p.title}</h3>
                        </div>
                        <div class="row-bot">
                            <span>${p.summary}</span>
                        </div>
                    </div>

                    <div class="col-right">
                        <div class="row-top">
                            <span>${p.account_name}</span>
                        </div>
                        <div class="row-bot">
                            <span>${p.created_at}</span>
                        </div>
                    </div>
                </article>
            `
            PAGE.post_ul.appendChild(li)
        });

        // 페이지네이션
        PAGE.pagination.dataset.target=target
        PAGE.pagination.dataset.id = id

        const pg  = respData.page
        const pgs = respData.pages
        console.log(pg, "/", pgs)

        PAGE.n_m.innerHTML = `${pg+1} / ${pgs}`

        if (pg === 0) {
            PAGE.btnPre.style.display = "none";
        } else {
            PAGE.btnPre.style.display = "inline";
            PAGE.btnPre.dataset.page = pg-1
        }
        
        if (pg === pgs - 1) {
            PAGE.btnNext.style.display = "none";
        } else {
            PAGE.btnNext.style.display = "inline";
            PAGE.btnNext.dataset.page = pg+1
        }


    }catch(err){
        console.log("ERROR from search :", err);
    }
}


// function changePagination(page, pages){
//     PAGE.pagination.
// }