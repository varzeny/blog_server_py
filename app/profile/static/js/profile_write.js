// profile_write.js


document.addEventListener("DOMContentLoaded", ()=>{
    console.log

    // 히스토리 폼 가로채기
    document.getElementById("form-history").addEventListener("submit", async(evt)=>{
        evt.preventDefault();

        const form = document.getElementById("form-history");
        const formData = new FormData(form);

        try{
            const resp = await fetch("/profile/write/history", {
                method:"POST",
                body:formData
            });

            if(resp.ok){
                form.reset();
            }else{ throw Error("200 아님"); }

        }catch(err){
            console.log("ERROR from form : ", err);
        }
    });


    // 프로젝트 폼 가로채기
    document.getElementById("form-project").addEventListener("submit", async(evt)=>{
        evt.preventDefault();

        const form = document.getElementById("form-project");
        const formData = new FormData(form);

        try {
            const resp = await fetch("/profile/write/project", {
                method:"POST",
                body:formData
            });

            if(resp.ok){
                form.reset();
            }else{ throw Error("200 아님") }

        } catch(err){
            console.log("ERROR from form : ", err);
        }

    });

})