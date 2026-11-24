document.addEventListener("click", function (event) {
  const btn = event.target.closest("#sidebar-toggle-btn");
  if (!btn) {
    return;
  }
  const sidebar = document.querySelector(".sidebar");
  if (sidebar) {
    sidebar.classList.toggle("hidden");
  }
});
