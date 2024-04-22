document.addEventListener("DOMContentLoaded", function() {
    const editButtons = document.querySelectorAll(".btn-edit");
    const commentText = document.getElementById("id_body");
    const commentForm = document.getElementById("commentForm");
    const submitButton = document.getElementById("submitButton");

    for (let button of editButtons) {
        button.addEventListener("click", (e) => {
          let commentId = e.currentTarget.getAttribute("comment_id"); 
        //debug console.log("Comment ID:", commentId);
          let commentContent = document.getElementById(`comment${commentId}`).innerText;
        // debug  console.log("Comment Content:", commentContent); 
          commentText.value = commentContent;
          submitButton.innerText = "Update";
          commentForm.setAttribute("action", `edit_comment/${commentId}`);
        });
    }
});