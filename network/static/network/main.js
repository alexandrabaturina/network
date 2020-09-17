document.addEventListener('DOMContentLoaded', function () {

  document.querySelectorAll('.card-body').forEach(div => div.style.display = 'block');
  document.querySelectorAll('.edit-card-body').forEach(div => div.style.display = 'none');

  // Close alert message
  document.querySelectorAll('.alert').forEach((alert) => {
      alert.addEventListener('click', () => alert.remove())
  });

  // Edit post
  document.querySelectorAll('.edit-post-btn').forEach((button) => {
      button.addEventListener('click', function() {

          const card = button.closest(".card");
          const oldPostText = card.querySelector('.card-text').innerText;
          // const oldPostCard = card.querySelector('.card-body').innerHTML;

          card.querySelector('.card-body').style.display = 'none';
          card.querySelector('.edit-card-body').style.display = 'block';

          card.querySelector('.edit-post-textarea').innerHTML = oldPostText;

          card.querySelector('.save-post-btn').addEventListener('click', function() {
              fetch(`edit/${card.id}`, {
                  method: 'POST',
                  body: JSON.stringify ({
                      "edited_post": card.querySelector('.edit-post-textarea').value
                  })
              })
              .then(response => response.json())
              .then(data => {
                  console.log(`Post #${card.id} was edited`);
                  card.querySelector('.edit-card-body').style.display = 'none';
                  card.querySelector('.card-body').style.display = 'block';
                  card.querySelector('.card-text').innerHTML = data["post_content"];

                  const editAlert = document.createElement('div');
                  editAlert.classList.add('alert', 'alert-success', 'alert-dismissible', 'fade', 'show');
                  editAlert.role = "alert";
                  editAlert.innerHTML = "Your post was successfully edited."
                  const closeAlertButton = document.createElement('button');
                  closeAlertButton.type = "button";
                  closeAlertButton.classList.add('close');
                  closeAlertButton["data-dismiss"] = 'alert';
                  closeAlertButton.innerHTML = '&times';
                  document.querySelector('.body').prepend(editAlert);
                  document.querySelector('.alert-success').append(closeAlertButton);
                  closeAlertButton.addEventListener('click', function () {
                      editAlert.remove();
                  })
              });
          });
      });
  });


  // Like/unlike post
  const likeButtons = document.querySelectorAll('.like-post-btn');
  likeButtons.forEach((button) => {
      button.addEventListener('click', function () {
          const card = button.closest(".card");
          if (button.innerHTML === 'Like') {
              fetch(`like/${card.id}`, {
                  method: 'POST',
                  body: JSON.stringify ({
                    "command": 'like'
                  })
              })
              .then(response => response.json())
              .then(data => {
                  console.log(`Post #${card.id} was liked`);
                  button.previousElementSibling.innerHTML = `Likes: ${data.likes}`
                  button.innerHTML = data.button_text;
              })

          } else {
                fetch(`like/${card.id}`, {
                    method: 'POST',
                    body: JSON.stringify ({
                      "command": 'unlike'
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(`Post #${card.id} was unliked`);
                    button.previousElementSibling.innerHTML = `Likes: ${data.likes}`
                    button.innerHTML = data.button_text;
                })
          }
      });
  });
});
