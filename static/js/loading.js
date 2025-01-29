document.addEventListener('DOMContentLoaded', () => {
    const loadingBar = document.getElementById('loading-bar');

    // Function to start the loading bar animation
    const startLoading = () => {
        loadingBar.style.width = '0%';
        loadingBar.style.opacity = '1';
        loadingBar.style.display = 'block';
        setTimeout(() => {
            loadingBar.style.width = '100%';
        }, 50);
    };

    // Function to reset the loading bar
    const resetLoading = () => {
        loadingBar.style.opacity = '0';
        setTimeout(() => {
            loadingBar.style.width = '0%';
            loadingBar.style.display = 'none';
        }, 500);
    };

    // Add event listeners to all links
    const links = document.querySelectorAll('a');
    links.forEach((link) => {
        link.addEventListener('click', (event) => {
            // Skip links with target="_blank" or external links
            if (
                link.target === '_blank' || 
                link.href.startsWith('http') && !link.href.includes(window.location.origin)
            ) {
                return;
            }

            // Prevent default navigation
            event.preventDefault();

            // Start the loading animation
            startLoading();

            // Navigate to the link after a short delay
            setTimeout(() => {
                window.location.href = link.href;
            }, 500);
        });
    });

    // Reset loading bar on page load
    resetLoading();
});
