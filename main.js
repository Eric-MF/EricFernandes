const menuContainer = document.querySelector(".menu-container");

function definirMenu(aberto){
    menuContainer.classList.toggle("active", aberto);
    menuContainer.setAttribute("aria-expanded", aberto);
}

menuContainer.addEventListener("click", () =>{
    definirMenu(!menuContainer.classList.contains("active"));
})
const menuItem = document.querySelectorAll(".lista-menu_item");

for(let i = 0; i < menuItem.length; i++){
  menuItem[i].addEventListener("click", () =>{
      definirMenu(false);
  })
}

// Link para uma pergunta abre a resposta
function abrirPergunta(){
    const alvo = location.hash && document.getElementById(location.hash.slice(1));
    if (alvo && alvo.tagName === "DETAILS") alvo.open = true;
}
window.addEventListener("hashchange", abrirPergunta);
abrirPergunta();

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
    mensagem.setAttribute('href','https://api.whatsapp.com/send?phone=5522998815479&text=Ol%C3%A1,%20Eric!%20Ser%C3%A1%20que%20voc%C3%AA%20pode%20me%20ajudar%20com%20uma%20quest%C3%A3o?');
    var mensagem = document.getElementById("whatsapp-contato");
    mensagem.setAttribute('href','https://api.whatsapp.com/send?phone=5522998815479&text=Ol%C3%A1,%20Eric!%20Ser%C3%A1%20que%20voc%C3%AA%20pode%20me%20ajudar%20com%20uma%20quest%C3%A3o?');
};