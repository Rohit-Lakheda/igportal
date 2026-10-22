(function(){
  const navToggle = document.getElementById('navToggle');
  const nav = document.getElementById('mainNav');
  if(navToggle && nav){
    navToggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();
