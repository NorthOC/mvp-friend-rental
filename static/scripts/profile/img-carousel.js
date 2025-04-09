//Displays img in avatar (also changes highlight on preview imgs)
let carousel = document.getElementById("carousel")
let images = carousel.getElementsByClassName("img-preview");

for (let img_shell of images){
    img_shell.addEventListener('click', ()=>{
        let avatar = document.getElementById("avatar-image");
        let image = img_shell.getElementsByTagName("img").item(0);

        if (image != null){
            avatar.src = image.src

            let nextlist = carousel.getElementsByTagName("img");
            for(let i = 0; i < nextlist.length; i++){
                nextlist[i].classList.remove("img-selected");
            }

            image.className = "img-selected"
        }
    })
}