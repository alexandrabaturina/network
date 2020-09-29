# Project 4: Network
## Overview
The current repo contains project called **network** which is Twitter-like social network website for making posts and following userse built with *Django* framework.

This project is built as Project 4 for [CS50W 2020 course](https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/) provided by edX platform.

## Features
The project meets the following requirements.
* **New Post**  
  Users who are signed in are able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.
  
![image](https://user-images.githubusercontent.com/53233637/94591840-712d8000-023d-11eb-96f4-ea5ae005f8f2.png)
  
* **All Posts**  
  The *"All Posts"* link in the navigation bar takes the user to a page where they can see all posts from all users, with the most recent posts first.
  * Each post includes the username of the poster, the post content itself, the date and time at which the post was made, and the number of "likes" the post has.
  
![image](https://user-images.githubusercontent.com/53233637/94595952-51e42200-0240-11eb-8c1d-43a4ab851a62.png)
  
* **Profile Page**  
  Clicking on a username loads that user’s profile page. This page should:
    * Display the number of followers the user has, as well as the number of people that the user follows.
    * Display all of the posts for that user, in reverse chronological order.
    * For any other user who is signed in, this page should also display a "Follow" or "Unfollow" button that will let the current user toggle whether or not they are following this user’s posts. This only applies to "other" users: a user is not be able to follow themselves.
    
![image](https://user-images.githubusercontent.com/53233637/94592311-cf5a6300-023d-11eb-8afe-c21c41765f34.png)

* **Following**  
  The "Following" link in the navigation bar takes the user to a page where they see all posts made by users that the current user follows.
  * This page behaves just as the "All Posts" page does, just with a more limited set of posts.
  * This page is only available to users who are signed in.
  
 ![image](https://user-images.githubusercontent.com/53233637/94594165-4ee83200-023e-11eb-94d2-9bfa4d2631bc.png)
  
* **Pagination**  
  On any page that displays posts, posts are only displayed 10 on a page. If there are more than ten posts, a "Next" button appears to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a "Previous" button appears to take the user to the previous page of posts as well.

![image](https://user-images.githubusercontent.com/53233637/94595083-2f053e00-023f-11eb-8810-a5fc9aab11d7.png)

* **Edit Post**  
  Users are able to click an "Edit" button or link on any of their own posts to edit that post.
  * When a user clicks "Edit" for one of their own posts, the content of their post is replaced with a textarea where the user can edit the content of their post.
  * The user is then able to "Save" the edited post.
  
![image](https://user-images.githubusercontent.com/53233637/94595512-ca96ae80-023f-11eb-9886-0196bcee023d.png)

![image](https://user-images.githubusercontent.com/53233637/94595608-ec903100-023f-11eb-83c3-c0e13f87e9a8.png)
  
* **"Like" and "Unlike"**  
  Users are able to click a button or link on any post to toggle whether or not they "like" that post.
## Dependencies
The app is built using *Django* framework. To install *Django* via terminal, use the following command.
```sh
$ pip3 install Django
```
## Getting Started
### Running Locally
To run **network** locally,
1. Clone this repo.
2. ```cd``` into project directory.
3. Start the *Django* web server.
```sh
$ python manage.py runserver
```
4. Access ```127.0.0.1:8000``` in your browser.
### Resetting a Database
The repo contains test database. To reset database,
1. Delete *db.sqlite3* file.
2. Run the following command.
```sh
$ python manage.py flush
```
## Authors
Alexandra Baturina
