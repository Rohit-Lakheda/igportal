/* SEARCH */
$("#searchInput").on("keyup", function () {
  const value = $(this).val().toLowerCase();
  $("#eventsTable tbody tr").filter(function () {
    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
  });
});

/* SORT */
function sortTable(col) {
  const table = document.getElementById("eventsTable");
  let switching = true, dir = "asc";

  while (switching) {
    switching = false;
    let rows = table.rows;
    for (let i = 1; i < rows.length - 1; i++) {
      let x = rows[i].cells[col].innerText.toLowerCase();
      let y = rows[i + 1].cells[col].innerText.toLowerCase();
      if ((dir === "asc" && x > y) || (dir === "desc" && x < y)) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        break;
      }
    }
    if (!switching && dir === "asc") {
      dir = "desc";
      switching = true;
    }
  }
}

/* MODALS */
function showDescription(text){
  $("#descBody").text(text);
  new bootstrap.Modal("#descModal").show();
}

function openDeleteModal(id){
  $("#delete_id").val(id);
  new bootstrap.Modal("#deleteModal").show();
}

function openUpdateModal(id, desc, link, date){
  $("#edit_id").val(id);
  $("#edit_desc").val(desc);
  $("#edit_link").val(link);
  $("#edit_date").val(date);
  new bootstrap.Modal("#updateEventModal").show();
}
