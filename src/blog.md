---
layout: default
title: Blog
---

<h1>Latest Posts</h1>

<ul class="posts">
  {% for post in site.posts %}
    <li>
          <h3 class="contents"><a href="{{ post.url }}">{{ post.title }}</a></h3>
          <p>{{ post.date | date_to_string }} {{post.author}}</p>
          <div style="height:300px;">
            <img src="{{ post.featured_image }}" alt="" class="featuredphoto_sq">
            <p style="height:300px;">{{post.summary}}</p>
        </div>
      </li>
  {% endfor %}
</ul>
