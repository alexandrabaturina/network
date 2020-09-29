# Project 4: Network
## Overview
The current repo contains project called **network** which is Twitter-like social network website for making posts and following userse built with *Django* framework.

This project is built as Project 4 for [CS50W 2020 course](https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/) provided by edX platform.

## Features
The project meets the following requirements.
* **New Post**  
  Users who are signed in are able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.
  * The *"New Post"* box is at the top of the *"All Posts"* page.
  
* **All Posts**  
  The *"All Posts"* link in the navigation bar takes the user to a page where they can see all posts from all users, with the most recent posts first.
  * Each post includes the username of the poster, the post content itself, the date and time at which the post was made, and the number of "likes" the post has.
  
* **Profile Page**  
  Clicking on a username loads that user’s profile page. This page should:
    * Display the number of followers the user has, as well as the number of people that the user follows.
    * Display all of the posts for that user, in reverse chronological order.
    * For any other user who is signed in, this page should also display a "Follow" or "Unfollow" button that will let the current user toggle whether or not they are following this user’s posts. This only applies to "other" users: a user is not be able to follow themselves.

* **Following**  
  The "Following" link in the navigation bar takes the user to a page where they see all posts made by users that the current user follows.
  * This page behaves just as the "All Posts" page does, just with a more limited set of posts.
  * This page is only available to users who are signed in.
  
* **Pagination**  
  On any page that displays posts, posts are only displayed 10 on a page. If there are more than ten posts, a "Next" button appears to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a "Previous" button appears to take the user to the previous page of posts as well.

* **Edit Post**  
  Users are able to click an "Edit" button or link on any of their own posts to edit that post.
  * When a user clicks "Edit" for one of their own posts, the content of their post is replaced with a textarea where the user can edit the content of their post.
  * The user is then able to "Save" the edited post.
  
* **"Like" and "Unlike"**  
  Users are able to click a button or link on any post to toggle whether or not they "like" that post.
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
