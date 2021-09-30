const loginBtn = document.querySelector('#login-btn');

// Display the sign in form when login button is clicked
loginBtn.addEventListener('click', () => {
    console.log('click');
    gsap.fromTo(".sign-in-container", {opacity: 0}, {duration: 0.5, opacity: 1});
    const signInContainer = document.querySelector('.sign-in-container');
    signInContainer.style.pointerEvents = 'auto';
})

const closeLoginContainer = document.querySelector('.btn-cross');

closeLoginContainer.addEventListener('click', () => {
    console.log('close');
    gsap.fromTo(".sign-in-container", {opacity: 1}, {duration: 0.5, opacity: 0});
    const signInContainer = document.querySelector('.sign-in-container');
    signInContainer.style.pointerEvents = 'none';
})