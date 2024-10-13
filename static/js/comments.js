document.addEventListener("DOMContentLoaded", function() {
    const editButtons = document.querySelectorAll(".btn-custom-edit");
    const commentText = document.getElementById("id_body");
    const commentForm = document.getElementById("commentForm");
    const submitButton = document.getElementById("submitButton");
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    const deleteButtons = document.getElementsByClassName("btn-delete");
    const deleteConfirm = document.getElementById("deleteConfirm");
    
    for (let button of editButtons) {
        button.addEventListener("click", (e) => {
          let commentId = e.currentTarget.getAttribute("comment_id"); 
        //debug console.log("Comment ID:", commentId);
          let commentContent = document.getElementById(`comment${commentId}`).innerText;
        // debug  console.log("Comment Content:", commentContent); 
          commentText.value = commentContent;
          submitButton.innerText = "Update";
          commentForm.setAttribute("action", `edit_comment/${commentId}/`);
        });
    }
    
    for (let button of deleteButtons) {
        button.addEventListener("click", (e) => {
          let commentId = e.target.getAttribute("comment_id");
          deleteConfirm.href = `delete_comment/${commentId}`;
          deleteModal.show();
    });
  }
});