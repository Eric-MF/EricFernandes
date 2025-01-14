const menuContainer = document.querySelector(".menu-container");

menuContainer.addEventListener("click", () =>{
    menuContainer.classList.toggle("active");
})
const menuItem = document.querySelectorAll(".lista-menu_item");

for(let i = 0; i < menuItem.length; i++){
  menuItem[i].addEventListener("click", () =>{
      menuContainer.classList.toggle("active");
  })
}

function iOS() {
    return [
      'iPad Simulator',
      'iPhone Simulator',
      'iPod Simulator',
      'iPad',
      'iPhone',
      'iPod'
    ].includes(navigator.platform)
    // iPad on iOS 13 detection
    || (navigator.userAgent.includes("Mac") && "ontouchend" in document)
  }

if(iOS()){
    trocar_mensagem()
}// t
// rue or false
function trocar_mensagem(){
    var mensagem = document.getElementById("whatsapp-menu");
    mensagem.setAttribute('href','https://api.whatsapp.com/send?phone=5555229988154&text=Ol%C3%A1,%20Eric!%20Ser%C3%A1%20que%20voc%C3%AA%20pode%20me%20ajudar%20com%20uma%20quest%C3%A3o?');
    var mensagem = document.getElementById("whatsapp-contato");
    mensagem.setAttribute('href','https://api.whatsapp.com/send?phone=5555229988154&text=Ol%C3%A1,%20Eric!%20Ser%C3%A1%20que%20voc%C3%AA%20pode%20me%20ajudar%20com%20uma%20quest%C3%A3o?');
};
