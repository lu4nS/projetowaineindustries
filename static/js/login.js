document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    const result = await response.json();

    if (result.success) {
        alert("Login successful!");
        window.location.href = "/dashboard"; // Redirect after login
    } else {
        document.getElementById("errorMessage").textContent = result.message;
    }
});
