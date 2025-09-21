function initializeBMSSeatSelection() {
  const seatMapContainer = document.querySelector(".seat-map");
  if (!seatMapContainer) return;

  const seats = document.querySelectorAll(".seat");
  const selectedSeatsContainer = document.getElementById("selected-seats");
  const seatsInput = document.getElementById("seats-input");
  const seatsCount = document.getElementById("seats-count");
  const totalPrice = document.getElementById("total-price");
  const bookBtn = document.getElementById("book-btn");

  // ✅ Fix: safer price extraction
  const seatLayoutContainer = document.querySelector(".seat-layout-container");
  const pricePerSeat =
    seatLayoutContainer && seatLayoutContainer.getAttribute("data-price")
      ? parseInt(seatLayoutContainer.getAttribute("data-price"))
      : 200;

  let selectedSeats = [];

  seats.forEach((seat) => {
    if (seat.classList.contains("occupied")) {
      seat.style.cursor = "not-allowed";
      return;
    }

    if (seat.classList.contains("available")) {
      seat.addEventListener("click", function () {
        const seatId = this.getAttribute("data-seat-id");
        const seatNumber = this.getAttribute("data-seat-number");

        if (this.classList.contains("selected")) {
          this.classList.remove("selected");
          selectedSeats = selectedSeats.filter((item) => item.id !== seatId);
        } else {
          this.classList.add("selected");
          selectedSeats.push({ id: seatId, number: seatNumber });
        }

        updateBookingSummary();
      });
    }
  });

  function updateBookingSummary() {
    if (selectedSeatsContainer) {
      selectedSeatsContainer.innerHTML = "";
      if (selectedSeats.length === 0) {
        selectedSeatsContainer.innerHTML =
          '<span class="text-muted">No seats selected</span>';
      } else {
        selectedSeats.forEach((seat) => {
          const span = document.createElement("span");
          span.className = "summary-seat-item";
          span.textContent = seat.number;
          selectedSeatsContainer.appendChild(span);
        });
      }
    }

    const count = selectedSeats.length;
    if (seatsCount) {
      seatsCount.textContent = count;
    }

    // ✅ Fix: prevent NaN
    const total = isNaN(pricePerSeat) ? 0 : count * pricePerSeat;
    if (totalPrice) {
      totalPrice.textContent = "₹" + total.toFixed(2);
    }

    if (seatsInput) {
      seatsInput.value = selectedSeats.map((seat) => seat.id).join(",");
    }

    if (bookBtn) {
      bookBtn.disabled = count === 0;
    }
  }

  if (
    !seatsInput ||
    !selectedSeatsContainer ||
    !seatsCount ||
    !totalPrice ||
    !bookBtn
  ) {
    console.error("One or more required elements not found");
  }
}

document.addEventListener("DOMContentLoaded", initializeBMSSeatSelection);
