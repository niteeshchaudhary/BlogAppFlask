function likeBlog(blogId) {
  // Send an AJAX request to the server to like the blog
  // Update the like count on the page without reloading

  // Example AJAX code using jQuery
  $.post("/like-blog/" + blogId, function (data) {
    // Handle the response from the server
    // Update the like count on the page
    if (data.success) {
      // Update the like count on the page
      $("#like-count").text(data.likes);

      // Toggle the button appearance
      $(".like-button i").toggleClass("fas fa-thumbs-up");
      $(".like-button i").toggleClass("far fa-thumbs-up");
    } else {
      // Show an error message or handle the failure case
    }
  });
}

function dislikeBlog(blogId) {
  // Send an AJAX request to the server to dislike the blog
  // Update the like count on the page without reloading

  // Example AJAX code using jQuery
  $.post("/dislike-blog/" + blogId, function (data) {
    // Handle the response from the server
    // Update the like count on the page
    if (data.success) {
      // Update the like count on the page
      $("#like-count").text(data.likes);

      // Toggle the button appearance
      $(".dislike-button i").toggleClass("fas fa-thumbs-down");
      $(".dislike-button i").toggleClass("far fa-thumbs-down");
    } else {
      // Show an error message or handle the failure case
    }
  });
}
