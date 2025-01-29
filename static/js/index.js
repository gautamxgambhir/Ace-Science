function startLoadingBar() {
    loadingBar.style.width = '0%';
    loadingBar.style.transition = 'none';
    setTimeout(() => {
        loadingBar.style.transition = 'width 0.3s ease-out';
        loadingBar.style.width = '100%';
    }, 50);
}

const links = document.querySelectorAll('.feature-card a');
const loadingBar = document.getElementById('loading-bar');

links.forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        const targetUrl = link.getAttribute('href');

        startLoadingBar();

        setTimeout(() => {
            window.location.href = targetUrl;
        }, 1000);
    });
});
document.addEventListener('DOMContentLoaded', function (event) {
    var dataText = ["Welcome to AceScience!", "Useful Resources.", "AI Quiz Bot."];
    function typeWriter(text, i, fnCallback) {
        if (i < (text.length)) {
            document.querySelector("h1").innerHTML = text.substring(0, i + 1) + '<span aria-hidden="true"></span>';
            setTimeout(function () {
                typeWriter(text, i + 1, fnCallback)
            }, 100);
        }
        else if (typeof fnCallback == 'function') {
            setTimeout(fnCallback, 700);
        }
    }
    function StartTextAnimation(i) {
        if (typeof dataText[i] == 'undefined') {
            setTimeout(function () {
                StartTextAnimation(0);
            }, 2000);
        }
        if (i < dataText[i].length) {
            typeWriter(dataText[i], 0, function () {
                StartTextAnimation(i + 1);
            });
        }
    }
    
    StartTextAnimation(0);
});