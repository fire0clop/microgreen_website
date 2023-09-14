// cart.js
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("cart-form");
  const totalCartCostElement = document.getElementById("total-cart-cost");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    // Отправляем данные на сервер при каждом изменении
    sendData();
  });

  // Добавляем обработчик изменения количества товаров
  const quantityInputs = document.querySelectorAll(".counter-input");
  quantityInputs.forEach(input => {
    input.addEventListener("change", function () {
      updateTotalCost(input);
      // Отправляем данные на сервер при каждом изменении
      sendData();
    });
  });

  // Функция для обновления итоговой стоимости по продукту
  function updateTotalCost(input) {
    const productId = input.getAttribute("data-product-id");
    const totalCostSpan = document.querySelector(`[data-product-id="${productId}"]`);
    const price = parseFloat(totalCostSpan.textContent);
    const quantity = parseInt(input.value);
    const totalCost = price * quantity;
    totalCostSpan.textContent = totalCost.toFixed(2);
  }

  // Функция для отправки данных на сервер
  function sendData() {
    const formData = new FormData(form);

    fetch(form.action, {
      method: form.method,
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        // Обновляем итоговую стоимость всей корзины
        totalCartCostElement.textContent = data.total_cart_cost;
      })
      .catch(error => {
        console.error("Ошибка при отправке данных на сервер: ", error);
      });
  }
});