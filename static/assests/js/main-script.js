function rotateIcon(id){
    let icon = document.getElementById(id);
    icon.style.transition = "transform 1s";  // Smooth animation
    icon.style.transform = "rotate(-360deg)";

    // Reset after rotation to allow repeat
    setTimeout(() => {
        icon.style.transition = "none";
        icon.style.transform = "rotate(0deg)";
    }, 1000);
}

// Alert Modal
function showAlert(status, message){
    const alertModal = new bootstrap.Modal(document.getElementById('alertModal'));
    document.getElementById("alertModalMessage").innerText = message
    document.getElementById("alertModalStatus").innerText = status

    alertModal.show()

}


// convert timestamp to YYYY-MM-DD eg: 2025-04-19 
function formatDate(timestamp) {
    const date = new Date(timestamp * 1000);  // convert seconds to milliseconds
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}


// refresh amount_report every 30 seconds
async function fetchAndUpdateBalance() {
    // Grabing all elemnts
    let currentBalance = document.getElementById("currentBalance")
    let totalCollection = document.getElementById("totalCollection")
    let totalPaid = document.getElementById("totalPaid")
    let totalUnpaid = document.getElementById("totalUnpaid")
    let totalExpense = document.getElementById("totalExpense")
    try {
        const response = await fetch('/api/get_balance');
        const data = await response.json();
        // parsing the balance
        currentBalance.innerText = data.current_balance
        totalCollection.innerText = data.total_collection
        totalExpense.innerText = data.total_expense
        totalPaid.innerText = data.total_paid
        totalUnpaid.innerText = data.total_unpaids
    } catch (error) {
        console.error("Error fetching balance:", error);
    }
}

// Run once immediately
fetchAndUpdateBalance();

// Repeat every 30 seconds
setInterval(fetchAndUpdateBalance, 30000);


// create a function that refresh the current balance and total balance
function refreshBalance(e){
    rotateIcon(e.target.id);
    fetchAndUpdateBalance();
}
