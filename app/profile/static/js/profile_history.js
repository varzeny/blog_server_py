// profile_history.js

const PAGE = {
    timeline:null,
    detail:null,
    init:function(){
        this.timeline = document.getElementById("timeline-ul");
        this.detail = document.getElementById("detail");
    }
}


document.addEventListener("DOMContentLoaded", async()=>{

    // 
    PAGE.init()

    // 
    const histories = document.getElementsByClassName("history");
    for(let h of histories){
        h.addEventListener("click", async(evt)=>{
            const id = evt.currentTarget.dataset.id;
            const respData = await getHistory(id);
            console.log(respData);

            const content = document.createElement("div");
            content.innerHTML = `
                <h3>${respData.title}</h3>
                <p>${respData.summary}</p>
                ${
                    respData.type === "image"
                        ? `<img src="/${respData.url}">`
                        : respData.type === "youtube"
                        ? `<iframe
                            src="https://www.youtube.com/embed/tphH9MOL5aw" 
                            title="YouTube video player" 
                            frameborder="0" 
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                            referrerpolicy="strict-origin-when-cross-origin" 
                            allowfullscreen>
                        </iframe>`
                        : ""
                }
            `;

            PAGE.detail.innerHTML ="";
            PAGE.detail.appendChild(content);
            

        });
    }

});





async function getHistory(id) {
    try{
        const resp = await fetch(`/profile/history/read/${id}`, {
            method:"get"
        });
        if(resp.ok){
            const respDate = await resp.json()
            return respDate.history
        }else{ throw Error("200 아님"); }
    }catch(err){
        console.log("ERROR from getHistory : ", err);
    }
}