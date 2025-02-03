document.addEventListener('DOMContentLoaded', () => {
    const loadingBar = document.getElementById('loading-bar');

    const startLoading = () => {
        loadingBar.style.width = '0%';
        loadingBar.style.opacity = '1';
        loadingBar.style.display = 'block';
        setTimeout(() => {
            loadingBar.style.width = '100%';
        }, 50);
    };

    const resetLoading = () => {
        loadingBar.style.opacity = '0';
        setTimeout(() => {
            loadingBar.style.width = '0%';
            loadingBar.style.display = 'none';
        }, 500);
    };

    const links = document.querySelectorAll('a');
    links.forEach((link) => {
        link.addEventListener('click', (event) => {
            if (
                link.target === '_blank' || 
                link.href.startsWith('http') && !link.href.includes(window.location.origin)
            ) {
                return;
            }

            event.preventDefault();

            startLoading();

            setTimeout(() => {
                window.location.href = link.href;
            }, 500);
        });
    });

    resetLoading();
});
