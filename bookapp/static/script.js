// Get the form element and set the correct username and password
const form = document.getElementById('uservalid');
const  correctName= 'admin';
const correctPass = '123456';
// Get the admin form, the "Continue as admin" button, and the landing page body
const adminForm= document.getElementsByClassName('nameform');
const continueAsAdminbutton = document.getElementById("continueAsAdmin");
const landingBody = document.getElementById('landingbody');
function pass(){
    const adminName= document.getElementById('adminName').value;
    const adminPass= document.getElementById('adminPass').value;
    if(adminName===correctName && adminPass===correctPass){
         // Check if the username and password match the hardcoded values
         let username =adminName;
         //store username in localstorage
         localStorage.setItem('username',username);
         //welcome text modified to admin name
          // If they match, redirect to the admin page
         window.location.href='/admin';
       
    }
    else{
         // If they don't match, display an error message
        alert("Incorrect username or password");
    }
}
function welcome(){
    const welcomeMessage = document.getElementById('welcomeName');

    let username = localStorage.getItem('username');
    
   
    if (!username){
       username= localStorage.setItem('username',document.getElementById('adminName').value);
       welcomeMessage.innerHTML= 'welcome !'+username;
    }
    
    welcomeMessage.innerText= 'welcome ! '+username;
       

}


//displays the form in the landing page 
function displayForm(){
    const adminform= document.getElementById("nameform");
    landingBody.style.cssText='filter: blur(10px); position:relative;';
    adminform.classList.toggle("hideDiv");


}
