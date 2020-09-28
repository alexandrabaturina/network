document.addEventListener('DOMContentLoaded', function () {

  document.querySelectorAll('.card-body').forEach(div => div.style.display = 'block');
  document.querySelectorAll('.edit-card-body').forEach(div => div.style.display = 'none');

  // Create alert message
  function createAlert(cardId, alertText) {

      // Remove existing alerts before creating a new one
      document.querySelectorAll('.alert').forEach(existingAlert => existingAlert.remove());

      const alertDiv = document.createElement('div');
      alertDiv.classList.add('alert', 'alert-success', 'alert-dismissible', 'fade', 'show');
      alertDiv.role = "alert";
      alertDiv.innerHTML = `${alertText}`;
      const closeAlertButton = document.createElement('button');
      closeAlertButton.type = "button";
      closeAlertButton.classList.add('close');
      closeAlertButton["data-dismiss"] = 'alert';
      closeAlertButton.innerHTML = '&times';

      document.getElementById(`${cardId}`).insertAdjacentElement('beforebegin', alertDiv);
      document.querySelector('.alert-success').append(closeAlertButton);
      closeAlertButton.addEventListener('click', () => alertDiv.remove());
  }

  // Close alert message
  document.querySelectorAll('.alert').forEach((alert) => {
      alert.addEventListener('click', () => alert.remove());
  });


  // Edit post
  document.querySelectorAll('.edit-post-btn').forEach((button) => {
      button.addEventListener('click', function() {

          const card = button.closest(".card");
          const oldPostText = card.querySelector('.card-text').innerText;

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

                  createAlert(card.id, 'Your post was edited.');
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
                  createAlert(`${card.id}`, 'You liked the post.')
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
                    createAlert(`${card.id}`, 'You unliked the post.')
                })
            }
        });
    });

    // Follow user
    const followButton = document.querySelector('.follow-button');
    if (followButton) {
      followButton.addEventListener('click', function() {
          const card = followButton.closest('.card');
          const username = card.querySelector('h2').innerText;
          if (followButton.innerHTML === 'Follow') {
              fetch(`follow/${username}`, {
                  method: 'POST',
                  body: JSON.stringify ({
                      'username': 'username'
                  })
              })
              .then(response => response.json())
              .then(data => {
                  console.log(data);
                  console.log(`Now you follow ${username}.`);
                  document.querySelector('.followers').innerHTML = `Followers: ${data.followers}`;
                  followButton.innerHTML = data.button_text;
              })
          } else {
              fetch(`unfollow/${username}`, {
                  method: 'POST',
                  body: JSON.stringify ({
                      'username': 'username'
                  })
              })
              .then(response => response.json())
              .then(data => {
                  console.log(data);
                  console.log(`You don't follow ${username} anymore.`);
                  document.querySelector('.followers').innerHTML = `Followers: ${data.followers}`;
                  followButton.innerHTML = data.button_text;
              })
            }
      });
    };
  });
