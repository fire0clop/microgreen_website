const mainImage = document.querySelector('.main-image img');
const smallImages = document.querySelectorAll('.small-images img');
const prevArrow = document.querySelector('.prev-arrow');
const nextArrow = document.querySelector('.next-arrow');

let currentIndex = 0;

// Функция для обновления главной картинки и текущего индекса
function updateMainImage() {
    mainImage.src = smallImages[currentIndex].src;
}

// Обработчик для стрелочки влево
prevArrow.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
    } else {
        currentIndex = smallImages.length - 1;
    }
    updateMainImage();
});

// Обработчик для стрелочки вправо
nextArrow.addEventListener('click', () => {
    if (currentIndex < smallImages.length - 1) {
        currentIndex++;
    } else {
        currentIndex = 0;
    }
    updateMainImage();
});

// Инициализация главной картинки
updateMainImage();