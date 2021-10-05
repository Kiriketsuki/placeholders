const loginBtn = document.querySelector('#login-btn');
const signInContainer = document.querySelector('.sign-in-container');

// Display the sign in form when login button is clicked
loginBtn.addEventListener('click', () => {
    console.log('click');
    gsap.fromTo(".sign-in-container", {opacity: 0}, {duration: 0.5, opacity: 1});
    signInContainer.style.pointerEvents = 'auto';
})

const closeLoginContainer = document.querySelector('.btn-cross');

// Close the sign in form
closeLoginContainer.addEventListener('click', () => {
    console.log('close');
    gsap.fromTo(".sign-in-container", {opacity: 1}, {duration: 0.5, opacity: 0});
    signInContainer.style.pointerEvents = 'none';
})
