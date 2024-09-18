let toggled=true;
const toggleElem=document.querySelector('.toggle-div');
const passwordInElem=document.querySelector('.password-in');
toggleElem.addEventListener('click',()=>toggleLock());
function toggleLock() {
  if(toggled) {
    passwordInElem.type="text";
    toggled=false;
    toggleElem.textContent='Hide';
  }
  else{
    passwordInElem.type="password";
    toggled=true;
    toggleElem.textContent='Show';
  }
}