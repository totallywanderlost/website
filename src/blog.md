---
layout: default
title: Blog
---

<h1>Latest Posts</h1>

<ul class="posts">
  {% for post in site.posts %}
    <li>
      <h3 class="contents"><a href="{{ post.url }}">{{ post.title }}</a></h3>
      <div class="post-list-summary">
        <img src="{{ post.featured_image }}" alt="" class="featuredphoto_sq">
        <div>
          <img src="{{ post.author_image }}" class="circlephoto"> {{ post.author }} on {{ post.date | date_to_string }} in {{ post.location }}
          <p>{{post.summary}}</p>
        </div>
      </div>
    </li>
  {% endfor %}
</ul>
