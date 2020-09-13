document.addEventListener('DOMContentLoaded', function () {

  // Edit posts

  // const editButtons = document.querySelectorAll('.edit-post');
  // editButtons.forEach((button) => {
  //     button.addEventListener('click', function() {
  //         const card = button.closest(".card");
  //         card.style.backgroundColor = "yellow";
  //         console.log(card.id);
  //     });
  // })


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
              })
              button.previousElementSibling.innerHTML = `Likes: ${Number(likes) + 1}`;
              button.innerHTML = 'Unlike';
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
                })
              button.previousElementSibling.innerHTML = `Likes: ${Number(likes) - 1}`;
              button.innerHTML = 'Like';
          }
      });
  });
});
