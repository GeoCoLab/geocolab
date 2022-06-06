<template>
  <div class="min-h-screen grid page-grid grid-cols-3">
    <Nav/>
    <div class="w-full px-10 py-1 grid items-center col-span-3" id="header"
         title="Photo by Max van den Oetelaar on Unsplash">
      <div class="flex flex-col container">
        <h1 class="site-title font-display font-bold text-primary-lightest">GeoCoLab</h1>
        <span
            class="site-subtitle text-primary-light">Matching access to analytical facilities with underserved researchers</span>
      </div>
    </div>
    <div class="h-full mx-auto p-10 main-content col-start-2">
      <slot/>
    </div>
  </div>
</template>

<script setup>
import Nav from '../components/Nav.vue';
</script>
