const button = document.getElementById("calculate");

function calculateTotal() {
    const amount = Number(document.getElementById("amount").value);
    const quantity = Number(document.getElementById("quantity").value);
    const total = amount * quantity;

    console.log({ amount, quantity, total });

    document.getElementById("message").textContent = `Total: ₹${total.toLocaleString("en-IN")}`;
}

button.addEventListener("click", calculateTotal);
