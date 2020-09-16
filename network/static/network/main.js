document.addEventListener('DOMContentLoaded', function () {

  // Close alert messages
  const alertMessages = document.querySelectorAll('.alert');
  alertMessages.forEach((alert) => {
      alert.addEventListener('click', () => alert.remove())
  });

  // Edit posts
  const editButtons = document.querySelectorAll('.edit-post');
  editButtons.forEach((button) => {
      button.addEventListener('click', function() {
          const card = button.closest(".card");
          const post_id = card.id;
          const card_content = card.querySelector('.card-body');
          const old_card_content = card_content.innerHTML;
          const post_to_edit = card_content.querySelector('.card-text').innerHTML;

          const textarea = document.createElement("textarea");
          const save_button = document.createElement("button");
          save_button.type = "button";
          save_button.classList.add("btn");
          save_button.classList.add("btn-primary");
          save_button.innerHTML = "Save";
          textarea.placeholder = post_to_edit;
          card_content.innerHTML = '';
          card_content.append(textarea);
          card_content.append(save_button);

          save_button.addEventListener('click', function() {
              fetch(`edit/${post_id}`, {
                  method: 'POST',
                  body: JSON.stringify ({
                      "edited_post": textarea.value
                  })
              })
              .then(response => response.json())
              .then(data => {
                  console.log(`Post #${post_id} was edited`);
                  textarea.remove();
                  save_button.remove();
                  card_content.innerHTML = old_card_content;
                  card_content.querySelector('.card-text').innerHTML = data["post_content"];

                  const edit_alert = document.createElement('div');
                  edit_alert.classList.add('alert');
                  edit_alert.classList.add('alert-success');
                  edit_alert.classList.add('alert-dismissible');
                  edit_alert.classList.add('fade');
                  edit_alert.classList.add('show');
                  edit_alert.role = "alert";
                  edit_alert.innerHTML = "Your post was successfully edited."
                  const close_alert = document.createElement('button');
                  close_alert.type = "button";
                  close_alert.classList.add('close');
                  close_alert["data-dismiss"] = 'alert';
                  close_alert.innerHTML = '&times';
                  document.querySelector('.body').prepend(edit_alert);
                  document.querySelector('.alert-success').append(close_alert);
              });
          });
      });
  })


  // Like/Unlike posts
  const likeButtons = document.querySelectorAll('.like');
  likeButtons.forEach((button) => {
      button.addEventListener('click', function () {
          const post_id = button.closest(".card").id;
          const likes = button.previousElementSibling.innerHTML.slice(7);
          if (button.innerHTML === 'Like') {
              fetch(`like/${post_id}`, {
                  method: 'POST',
                  body: JSON.stringify ({
                    "command": 'like'
                  })
              })
              .then(response => response.json())
              .then(data => {
                  console.log(`Post #${post_id} was liked`);
                  button.previousElementSibling.innerHTML = `Likes: ${data.likes}`
                  button.innerHTML = data.button_text;
              })

          } else {
                fetch(`like/${post_id}`, {
                    method: 'POST',
                    body: JSON.stringify ({
                      "command": 'unlike'
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(`Post #${post_id} was unliked`);
                    button.previousElementSibling.innerHTML = `Likes: ${data.likes}`
                    button.innerHTML = data.button_text;
                })
          }
      });
  });
});
