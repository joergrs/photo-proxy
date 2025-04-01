def generate_slideshow_page() -> str:
    """Generate a slideshow page that displays random images."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Photo Slideshow</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                margin: 0;
                padding: 0;
                background-color: #000;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                overflow: hidden;
            }
            .slideshow-container {
                position: relative;
                width: 100vw;
                height: 100vh;
            }
            .slide {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                opacity: 0;
                transition: opacity 1s ease-in-out;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .slide.active {
                opacity: 1;
            }
            .slide img {
                max-width: 100%;
                max-height: 100%;
                object-fit: contain;
            }
            #controls {
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background-color: rgba(0, 0, 0, 0.5);
                padding: 10px;
                border-radius: 5px;
                display: flex;
                gap: 10px;
                z-index: 1000;
            }
            button {
                background-color: #fff;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                cursor: pointer;
                font-size: 14px;
            }
            button:hover {
                background-color: #eee;
            }
            #status {
                color: #fff;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="slideshow-container">
            <div class="slide active">
                <img src="/random" alt="Slideshow">
            </div>
            <div class="slide">
                <img src="/random" alt="Slideshow">
            </div>
        </div>
        <div id="controls">
            <button onclick="toggleSlideshow()">Pause</button>
            <button onclick="nextImage()">Next</button>
            <span id="status">Next image in: 10s</span>
        </div>

        <script>
            let isPlaying = true;
            let timer = null;
            let timeLeft = 10;
            let currentSlide = 0;
            let nextSlide = 1;
            const slides = document.querySelectorAll('.slide');
            const status = document.getElementById('status');
            const playButton = document.querySelector('button');

            function updateTimer() {
                if (isPlaying) {
                    timeLeft--;
                    status.textContent = `Next image in: ${timeLeft}s`;
                }
            }

            function preloadImage(url) {
                return new Promise((resolve, reject) => {
                    const img = new Image();
                    img.onload = () => resolve(img);
                    img.onerror = reject;
                    img.src = url;
                });
            }

            async function nextImage() {
                try {
                    // Preload the next image
                    const nextImageUrl = '/random?' + new Date().getTime();
                    await preloadImage(nextImageUrl);

                    // Update the next slide's image
                    slides[nextSlide].querySelector('img').src = nextImageUrl;

                    // Fade out current slide
                    slides[currentSlide].classList.remove('active');

                    // Fade in next slide
                    slides[nextSlide].classList.add('active');

                    // Update slide indices
                    currentSlide = nextSlide;
                    nextSlide = (nextSlide + 1) % slides.length;

                    timeLeft = 10;
                    status.textContent = `Next image in: ${timeLeft}s`;
                } catch (error) {
                    console.error('Error loading image:', error);
                    // Try again immediately
                    setTimeout(nextImage, 100);
                }
            }

            function toggleSlideshow() {
                isPlaying = !isPlaying;
                playButton.textContent = isPlaying ? 'Pause' : 'Play';
                if (isPlaying) {
                    timer = setInterval(updateTimer, 1000);
                } else {
                    clearInterval(timer);
                }
            }

            // Start the slideshow
            timer = setInterval(updateTimer, 1000);
            setInterval(nextImage, 10000);

            // Handle image loading errors
            document.querySelectorAll('.slide img').forEach(img => {
                img.onerror = function() {
                    console.error('Error loading image');
                    nextImage();
                };
            });
        </script>
    </body>
    </html>
    """