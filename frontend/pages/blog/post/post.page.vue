<template>
  <h2 class="page-title">{{ post.title }}</h2>
  <div><a :href="`/blog?author=${post.author.id}`">{{ post.author.name }}</a></div>
  <small>{{ post.posted }}</small>
  <div>
    {{ post.body }}
  </div>
</template>

<script setup>
defineProps(['post'])
</script>
