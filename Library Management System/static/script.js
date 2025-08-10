document.addEventListener("DOMContentLoaded", () => {
  const pages = document.querySelectorAll(".page");
  const navBtns = document.querySelectorAll(".nav-btn");

  navBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      navBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      pages.forEach(p => p.classList.remove("active"));
      document.getElementById(btn.dataset.page).classList.add("active");

      document.getElementById("page-title").textContent = btn.textContent;
      if (btn.dataset.page === "dashboard") loadStats();
      if (btn.dataset.page === "view") loadBooksTable();
    });
  });

  // Load stats on dashboard
  async function loadStats() {
    const res = await fetch("/api/stats");
    const data = await res.json();
    document.getElementById("totalBooks").textContent = data.total_books;
    document.getElementById("issuedBooks").textContent = data.issued_books;
    document.getElementById("returnedBooks").textContent = data.returned_today;
  }

  // Load books table
  async function loadBooksTable() {
    const res = await fetch("/api/books");
    const books = await res.json();
    const tbody = document.getElementById("booksTable");
    tbody.innerHTML = "";
    books.forEach((b, i) => {
      tbody.innerHTML += `<tr>
        <td>${i+1}</td>
        <td>${b.BOOK_NAME}</td>
        <td>${b.BCODE}</td>
        <td>${b.TOTAL}</td>
        <td>${b.SUBJECT}</td>
      </tr>`;
    });
  }

  // Add book form
  document.getElementById("addForm").addEventListener("submit", async e => {
    e.preventDefault();
    const formData = Object.fromEntries(new FormData(e.target).entries());
    await fetch("/api/add", { method: "POST", body: JSON.stringify(formData), headers: {"Content-Type": "application/json"} });
    alert("Book added!");
    e.target.reset();
  });

  // Issue book form
  document.getElementById("issueForm").addEventListener("submit", async e => {
    e.preventDefault();
    const formData = Object.fromEntries(new FormData(e.target).entries());
    const res = await fetch("/api/issue", { method: "POST", body: JSON.stringify(formData), headers: {"Content-Type": "application/json"} });
    const result = await res.json();
    alert(result.status === "success" ? "Book issued!" : result.message);
    e.target.reset();
  });

  // Return book form
  document.getElementById("returnForm").addEventListener("submit", async e => {
    e.preventDefault();
    const formData = Object.fromEntries(new FormData(e.target).entries());
    await fetch("/api/return", { method: "POST", body: JSON.stringify(formData), headers: {"Content-Type": "application/json"} });
    alert("Book returned!");
    e.target.reset();
  });

  // Delete book form
  document.getElementById("deleteForm").addEventListener("submit", async e => {
    e.preventDefault();
    const formData = Object.fromEntries(new FormData(e.target).entries());
    await fetch("/api/delete", { method: "POST", body: JSON.stringify(formData), headers: {"Content-Type": "application/json"} });
    alert("Book deleted!");
    e.target.reset();
  });

  // Load dashboard initially
  loadStats();
});
pages.forEach(p => p.classList.remove("active"));
document.getElementById(btn.dataset.page).classList.add("active");
