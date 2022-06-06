<template>
  <div class="flex items-center">
    <img :src="auth.userData.gravatar + '&s=100'" class="mr-8 rounded-full border-2 border-secondary-light">
    <h2>Hello, {{ auth.userData.name }}!</h2>
  </div>
  <div v-if="auth.userData.todo.length > 0">
    <p>Your account is {{ auth.userData.completion }}% complete.</p>
    <p>Tasks still left to complete:</p>
    <ul>
      <li v-for="task in auth.userData.todo">
        {{ task }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { useAuthStore } from '../../store/auth';

const auth = useAuthStore();
</script>

<style lang="scss">
</style>
